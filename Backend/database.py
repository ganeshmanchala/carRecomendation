# database.py
from pymongo import MongoClient
from datetime import datetime, timezone

class CarDatabase:
    def __init__(self, mongo_uri='mongodb://localhost:27017/', db_name='car_database'):
        self.client = MongoClient(mongo_uri)
        self.db = self.client[db_name]
        self.collection = self.db['cars']

    def upsert_car(self, car_data):
        """
        Upsert car data based on the unique 'spec_url'.
        Also sets a 'last_updated' timestamp.
        """
        if 'spec_url' not in car_data:
            return False
        car_data['last_updated'] = datetime.now(timezone.utc)
        return self.collection.update_one(
            {'spec_url': car_data['spec_url']},
            {'$set': car_data},
            upsert=True
        ).acknowledged

    def prune_old_models(self):
        """
        Keep only the latest model version for each type (ev and fuel).
        Delete all older versions from the model_versions collection.
        """
        for model_type in ['ev', 'fuel']:
            latest = list(self.db.model_versions.find({"type": model_type}).sort("trained_at", -1).limit(1))
            if latest:
                self.db.model_versions.delete_many({
                    "type": model_type,
                    "_id": {"$nin": [latest[0]['_id']]}
                })

    def prune_old_cars(self):
        """
        Delete all car documents from the collection.
        (This frees up space so that only the most recent scrape data remains.)
        """
        self.collection.delete_many({})

    def close(self):
        self.client.close()
