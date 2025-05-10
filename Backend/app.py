# app.py (updated for new DB structure)
from flask import Flask, request, jsonify
from flask_jwt_extended import (
    JWTManager, create_access_token, create_refresh_token,
    jwt_required, get_jwt_identity, set_access_cookies,
    set_refresh_cookies, unset_jwt_cookies
)
from flask_cors import CORS
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta
from bson import ObjectId
import re
import pickle
import pandas as pd
import numpy as np

app = Flask(__name__)
app.secret_key = 'secret_key_my'

# JWT Configurationapp = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "your_jwt_secret_key"
app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
app.config["JWT_ACCESS_COOKIE_PATH"] = "/"
app.config["JWT_REFRESH_COOKIE_PATH"] = "/refresh"
app.config["JWT_COOKIE_CSRF_PROTECT"] = False
app.config["JWT_COOKIE_SECURE"] = False  # For development (HTTP)
app.config["JWT_COOKIE_SAMESITE"] = "Lax"
app.config["JWT_SESSION_COOKIE"] = False  # 👈 Critical change for persistent cookies
jwt = JWTManager(app)
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}}, supports_credentials=True)
# MongoDB Setup
client = MongoClient("mongodb://localhost:27017/")
db = client['car_database']
users_collection = db['users']
cars_collection = db['cars']

def extract_numeric(s):
    try:
        m = re.search(r"[\d.]+", str(s))
        return float(m.group(0)) if m else np.nan
    except Exception:
        return np.nan

def convert_price(price):
    try:
        if isinstance(price, (int, float)):
            return float(price)
        s = str(price).lower().replace(',', '').strip()  # Remove commas
        if "lakh" in s:
            num = float(re.sub(r"[^\d.]", "", s))
            return num
        elif "cr" in s or "crore" in s:
            num = float(re.sub(r"[^\d.]", "", s))
            return num * 100  # Convert crore to lakhs
        else:
            # Assume user input without unit is in lakhs
            return float(s)
    except:
        return np.nan

def extract_brand(car_doc):
    model = car_doc.get('base_specs', {}).get('model') or \
            car_doc.get('specs', {}).get('Model', '')
    return model.split()[0].lower() if model else "unknown"

def get_nested_value(specs, section, key):
    if not isinstance(specs, dict):
        return ""
    if section:
        return specs.get(section, {}).get(key, "")
    return specs.get(key, "")

def load_latest_model(category: str):
    model_doc = db.model_versions.find_one(
        {"type": category},
        sort=[("trained_at", -1)]
    )
    if not model_doc:
        raise ValueError(f"No {category} model found")
    return {
        "model": pickle.loads(model_doc["model"]),
        "encoder": pickle.loads(model_doc["encoder"]),
        "features": model_doc["features"],
        "meta": model_doc.get("meta", {})
    }

# Load models
try:
    fuel_data = load_latest_model("fuel")
    ev_data = load_latest_model("ev")
    fuel_model = fuel_data["model"]
    fuel_encoder = fuel_data["encoder"]
    fuel_features = fuel_data["features"]
    ev_model = ev_data["model"]
    ev_encoder = ev_data["encoder"]
    ev_features = ev_data["features"]
except Exception as e:
    app.logger.error(f"Model loading failed: {str(e)}")
    fuel_model = ev_model = None
    fuel_encoder = ev_encoder = None
@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    phone = data.get('phone')
    name = data.get('name')
    if not username or not password or not phone or not name:
        return jsonify({'success': False, 'error': 'All fields are required'}), 400
    if users_collection.find_one({'username': username}):
        return jsonify({'success': False, 'error': 'User already exists'}), 400
    hashed_password = generate_password_hash(password)
    result = users_collection.insert_one({
        'username': username,
        'password': hashed_password,
        'phone': phone,
        'name': name
    })
    response = jsonify({
        'success': True,
        'message': 'User registered successfully'
    })
    return response, 201

@app.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    current_user = get_jwt_identity()
    new_token = create_access_token(identity=current_user)
    response = jsonify({'success': True})
    set_access_cookies(response, new_token)
    return response

@app.route('/checkAuth', methods=['GET'])
@jwt_required()
def check_auth():
    current_user = get_jwt_identity()
    user = users_collection.find_one({'username': current_user})

    if not user:
        return jsonify({'isAuthenticated': False}), 200  # Ensure consistent status

    return jsonify({
        'isAuthenticated': True,
        'user': {
            'id': str(user['_id']),
            'username': user['username'],
            'name': user['name']
        }
    }), 200

# @jwt.unauthorized_loader
# def unauthorized_callback(error):
#     return jsonify({'success': False, 'error': 'Missing or invalid token'}), 401

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({'success': False, 'error': 'Username and password are required'}), 400
    user = users_collection.find_one({'username': username})
    if not user or not check_password_hash(user['password'], password):
        return jsonify({'success': False, 'error': 'Invalid credentials'}), 401

    # Create tokens
    access_token = create_access_token(identity=user['username'], expires_delta=timedelta(hours=1))
    refresh_token = create_refresh_token(identity=user['username'], expires_delta=timedelta(days=30))

    response = jsonify({
        'success': True,
        'message': 'Logged in successfully',
        'user': {
            'id': str(user['_id']),
            'username': user['username'],
            'name': user['name']
        }
    })

    # Set the JWTs in cookies
    set_access_cookies(response, access_token)
    set_refresh_cookies(response, refresh_token)
    return response, 200

# @app.route('/protected', methods=['GET'])
# @jwt_required()
# def protected():
#     current_user_id = get_jwt_identity()
#     user = users_collection.find_one({'_id': ObjectId(current_user_id)})
#     return jsonify({
#         'user': {
#             'id': str(user['_id']),
#             'username': user['username'],
#             'name': user['name']
#         }
#     }), 200

@app.route('/logout', methods=['POST'])
def logout():
    response = jsonify({'success': True, 'message': 'Logged out'})
    # Clear the JWT cookies
    unset_jwt_cookies(response)
    return response

@app.route("/recommend", methods=["POST"])
def recommend():
    try:
        user_input = request.json
        query = {}
        is_ev = user_input.get("ev", False)
        
        # (If EV, look for Range; if fuel, look for Mileage)
        if is_ev:
            query["specs.Key Specifications.Range"] = {"$exists": True}
        else:
            query["specs.Key Specifications.Mileage"] = {"$exists": True}


        # Price filter using $expr to convert base_specs.price to a number on the fly
        # min_price = user_input.get("min_price")
        # max_price = user_input.get("max_price")
        # price_filters = []
        # price_expr = {
        #     "$toDouble": {
        #         "$replaceAll": {  # 👈 Add this to remove commas
        #             "input": {
        #                 "$arrayElemAt": [
        #                     { "$split": ["$base_specs.price", " "] },
        #                     0
        #                 ]
        #             },
        #             "find": ",",
        #             "replacement": ""
        #         }
        #     }
        # }
        # if min_price:
        #     # Convert the incoming string (e.g., "20") to a float
        #     min_value = convert_price(min_price)
        #     price_filters.append({ "$gte": [ price_expr, min_value ] })
        # if max_price:
        #     max_value = convert_price(max_price)
        #     price_filters.append({ "$lte": [ price_expr, max_value ] })
        # if price_filters:
        #     query["$expr"] = { "$and": price_filters }

        # Transmission filter (assuming the field is in "Engine & Transmission")
        transmission = user_input.get("transmission")
        if transmission:
            query["specs.Engine & Transmission.Transmission Type"] = {
                "$regex": f"^{transmission.strip()}",
                "$options": "i"
            }

        # Brand filter: first word in model can appear in base_specs.model or specs.Model
        brand = user_input.get("brand")
        if brand:
            query["$or"] = [
                {"base_specs.model": {"$regex": f"^{brand}", "$options": "i"}},
                {"specs.Model": {"$regex": f"^{brand}", "$options": "i"}}
            ]

        # Drivetrain filter (from "Engine & Transmission")
        drivetrain = user_input.get("drivetrain")
        if drivetrain:
            query["specs.Engine & Transmission.Drive Type"] = {
                "$regex": f"^{drivetrain.strip()}",
                "$options": "i"
            }

        # Fuel-type filter (if the car is fuel-powered and a type is specified)
        fuel_type = user_input.get("fuel_type")
        if fuel_type and fuel_type.lower() != "any":
            query["specs.Fuel & Performance.Fuel Type"] = {
                "$regex": f"^{fuel_type.strip()}",
                "$options": "i"
            }

        # safety_rating = user_input.get("safety_rating")
        # if safety_rating:
        #     # If stored as a string, we could use $toDouble conversion similarly.
        #     query["$expr"] = query.get("$expr", {"$and": []})
        #     query["$expr"]["$and"].append({
        #         "$gte": [
        #             { "$toDouble": { "$arrayElemAt": [ { "$split": [ "$specs.Rating", " " ] }, 0 ] } },
        #             float(safety_rating)
        #         ]
        #     })

        # (Other numeric filters such as mileage, power, battery_capacity, and range could be handled similarly.)
        # For example, if a mileage filter is provided for fuel cars:
        mileage = user_input.get("mileage")
        if mileage and not is_ev:
            query["$expr"] = query.get("$expr", {"$and": []})
            query["$expr"]["$and"].append({
                "$gte": [
                    {
                        "$toDouble": {
                            "$arrayElemAt": [
                                { "$split": [ "$specs.Fuel & Performance.Diesel Mileage ARAI", " " ] },
                                0
                            ]
                        }
                    },
                    float(mileage)
                ]
            })

        # Retrieve initial candidate documents (limit for performance)
        print("Final Query:", query)
        candidates = list(cars_collection.find(query, limit=2000))
        min_lakhs = convert_price(user_input.get("min_price")) if user_input.get("min_price") else 0
        max_lakhs = convert_price(user_input.get("max_price")) if user_input.get("max_price") else float('inf')
        filtered_candidates = []
        for car in candidates:
            car_price_str = car.get('base_specs', {}).get('price', '')
            car_price_lakhs = convert_price(car_price_str)
            if not np.isnan(car_price_lakhs) and (min_lakhs <= car_price_lakhs <= max_lakhs):
                filtered_candidates.append(car)
        candidates = filtered_candidates
        # Seat filter: check in "Dimensions & Capacity"; if not available, try "Key Specifications"
        seats = user_input.get("seats")
        if seats is not None:
            seats = int(seats)
            filtered_candidates = []
            for car in candidates:
                specs = car.get("specs", {})
                seating_str = get_nested_value(specs, "Dimensions & Capacity", "Seating Capacity")
                if not seating_str:
                    seating_str = get_nested_value(specs, "Key Specifications", "Seating Capacity")
                if seating_str:
                    numbers = re.findall(r'\d+', seating_str)
                    if numbers and int(numbers[0]) >= seats:
                        filtered_candidates.append(car)
            candidates = filtered_candidates

        # If no candidates found, return message
        if not candidates:
            return jsonify({"message": "No cars match your criteria."})

        # Process features and predictions (feature extraction, normalization, and model prediction)
        processed_data = []
        for car in candidates:
            specs = car.get('specs', {})
            base_specs = car.get('base_specs', {})
            
            # Extract features
            price = convert_price(base_specs.get('price', np.nan))
            power = extract_numeric(
                get_nested_value(specs, 'Key Specifications', 'Power') or
                get_nested_value(specs, 'Engine & Transmission', 'Max Power')
            )
            
            if is_ev:
                mileage = np.nan
                car_range = extract_numeric(
                    get_nested_value(specs, 'Key Specifications', 'Range')
                )
            else:
                car_range = np.nan
                mileage = extract_numeric(
                    get_nested_value(specs, 'Fuel & Performance', 'Diesel Mileage ARAI') or
                    get_nested_value(specs, 'Key Specifications', 'Mileage')
                )

            car_brand = extract_brand(car)
            
            # Normalization (based on loaded model metadata)
            features = {}
            model_meta = ev_data['meta'] if is_ev else fuel_data['meta']
            for col in ['price', 'power']:
                try:
                    features[f'{col}_normalized'] = (
                        (locals()[col] - model_meta[col]['min']) / 
                        (model_meta[col]['max'] - model_meta[col]['min'])
                    )
                except Exception:
                    features[f'{col}_normalized'] = 0.0
            
            if is_ev:
                try:
                    features['range_normalized'] = (
                        (car_range - model_meta['range']['min']) /
                        (model_meta['range']['max'] - model_meta['range']['min'])
                    )
                except Exception:
                    features['range_normalized'] = 0.0
            else:
                try:
                    features['mileage_normalized'] = (
                        (mileage - model_meta['mileage']['min']) /
                        (model_meta['mileage']['max'] - model_meta['mileage']['min'])
                    )
                except Exception:
                    features['mileage_normalized'] = 0.0

            # Brand encoding
            try:
                brand_encoded = ev_encoder.transform([car_brand])[0] if is_ev else \
                                fuel_encoder.transform([car_brand])[0]
            except Exception:
                brand_encoded = 0

            # Create feature vector
            vector = [
                features['price_normalized'],
                features['power_normalized'],
                features['range_normalized' if is_ev else 'mileage_normalized'],
                brand_encoded
            ]
            processed_data.append(vector)

        # Model prediction
        feature_cols = ev_features if is_ev else fuel_features
        df_features = pd.DataFrame(processed_data, columns=feature_cols)
        scores = ev_model.predict(df_features) if is_ev else fuel_model.predict(df_features)
        
        # Prepare and return the response sorted by score
        results = sorted(zip(candidates, scores), key=lambda x: x[1], reverse=True)
        response_data = []
        for car, score in results:
            car['_id'] = str(car['_id'])
            car["score"] = float(score)
            response_data.append(car)

        return jsonify({"cars": response_data})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
