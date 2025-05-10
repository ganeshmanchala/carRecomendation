# trainer.py
import pandas as pd
import numpy as np
from lightgbm import LGBMRanker
import pickle
from datetime import datetime, timezone
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import GroupKFold
import re
from pymongo import MongoClient

def extract_numeric(s):
    try:
        m = re.search(r"[\d.]+", str(s))
        return float(m.group(0)) if m else np.nan
    except Exception:
        return np.nan

def get_nested_value(specs, section, key):
    """
    Retrieve values from the flat specs structure
    """
    if not isinstance(specs, dict):
        return ""
    if section:
        section_dict = specs.get(section, {})
    else:
        section_dict = specs
    return section_dict.get(key, "")

class CarModelTrainer:
    def __init__(self, mongo_uri='mongodb://localhost:27017/', db_name='car_database'):
        self.client = MongoClient(mongo_uri)
        self.db = self.client[db_name]
        self.collection = self.db['cars']

    def get_training_data(self):
        print("Fetching training data from MongoDB...")
        # Project only needed fields
        cars = list(self.collection.find({}, {
            "specs": 1,
            "base_specs": 1,
            "_id": 0
        }))
        return pd.DataFrame(cars)

    def preprocess_data(self, df):
        print("Preprocessing data...")
        # Extract features from new structure
        df['price'] = df['specs'].apply(lambda x: extract_numeric(
            get_nested_value(x, '', 'Price') or
            x.get('base_specs', {}).get('price', '')
        ))
        
        df['mileage'] = df['specs'].apply(lambda x: extract_numeric(
            get_nested_value(x, 'Key Specifications', 'Mileage')
        ))
        
        df['power'] = df['specs'].apply(lambda x: extract_numeric(
            get_nested_value(x, 'Key Specifications', 'Power') or
            get_nested_value(x, 'Engine & Transmission', 'Max Power')
        ))
        
        df['range'] = df['specs'].apply(lambda x: extract_numeric(
            get_nested_value(x, 'Key Specifications', 'Range')
        ))

        # Extract brand from name
        df['model_name'] = df.apply(
            lambda row: row.get('base_specs', {}).get('model') 
            or row.get('specs', {}).get('Model', ''),
            axis=1
        )
        df['brand'] = df['model_name'].str.split().str[0].str.lower()
        self.brand_encoder = LabelEncoder()
        df['brand_encoded'] = self.brand_encoder.fit_transform(df['brand'])
        
        # Normalize numeric columns
        for col in ['price', 'power', 'mileage', 'range']:
            valid_values = df[col].dropna()
            if not valid_values.empty:
                col_min = valid_values.min()
                col_max = valid_values.max()
                if col_max != col_min:
                    df[f'{col}_normalized'] = (df[col] - col_min) / (col_max - col_min)
                else:
                    df[f'{col}_normalized'] = 0.0
            else:
                df[f'{col}_normalized'] = 0.0
                
        return df

    def calculate_relevance(self, row):
        try:
            price_norm = 1 - row['price_normalized'] if pd.notna(row['price_normalized']) else 0.4
            power_norm = row['power_normalized'] if pd.notna(row['power_normalized']) else 0.3
            mileage_norm = row['mileage_normalized'] if pd.notna(row['mileage_normalized']) else 0.1
            range_norm = row['range_normalized'] if pd.notna(row['range_normalized']) else 0
            return (0.4 * price_norm + 0.3 * power_norm + 0.2 * mileage_norm + 0.1 * range_norm)
        except Exception as e:
            print(f"Error calculating relevance: {str(e)}")
            return 0

    def train_model(self, df, model_type):
        print(f"Training {model_type} model...")
        features = ['price_normalized', 'power_normalized', 'mileage_normalized', 'brand_encoded']
        df = df.copy().dropna(subset=['brand_encoded'])
        if df.empty:
            print(f"No valid data for {model_type} model")
            return
            
        df['rank'] = df.groupby('brand_encoded')['relevance'].rank(method='dense', ascending=False).fillna(1).astype(int)
        max_rank = df['rank'].max()
        label_gain = list(range(max_rank + 2))
        
        model = LGBMRanker(
            objective="lambdarank",
            metric="ndcg",
            n_estimators=200,
            verbose=-1,
            label_gain=label_gain
        )
        
        df['query_id'] = df['brand_encoded']
        valid_groups = df.groupby('query_id').size()
        groups = valid_groups[valid_groups > 0].values
        
        if len(groups) == 0:
            print(f"No valid groups for {model_type} model")
            return
            
        model.fit(df[features], df['rank'], group=groups)
        
        model_data = {
            "type": model_type,
            "model": pickle.dumps(model),
            "features": features,
            "encoder": pickle.dumps(self.brand_encoder),
            "trained_at": datetime.now(timezone.utc),
            "meta": {
                "price": {"min": df.price.min(), "max": df.price.max()},
                "power": {"min": df.power.min(), "max": df.power.max()},
                "mileage": {"min": df.mileage.min(), "max": df.mileage.max()}
            }
        }
        
        self.db.model_versions.delete_many({"type": model_type})
        self.db.model_versions.insert_one(model_data)

    def run_training(self):
        try:
            df = self.get_training_data()
            df = self.preprocess_data(df)
            df['relevance'] = df.apply(self.calculate_relevance, axis=1).fillna(0)
            
            # Split into EV and Fuel based on actual specs
            ev_df = df[(df['range'].notna()) & (df['range'] != 0)].copy()
            fuel_df = df[(df['mileage'].notna()) & (df['mileage'] != 0)].copy()
            
            if not ev_df.empty:
                self.train_model(ev_df, 'ev')
            else:
                print("Skipping EV model - no valid data")
                
            if not fuel_df.empty:
                self.train_model(fuel_df, 'fuel')
            else:
                print("Skipping Fuel model - no valid data")
                
            print("Training process completed!")
        except Exception as e:
            print(f"Training failed: {str(e)}")
            raise

if __name__ == "__main__":
    print("Starting car recommendation model training...")
    trainer = CarModelTrainer()
    trainer.run_training()
    print("Models saved to MongoDB!")