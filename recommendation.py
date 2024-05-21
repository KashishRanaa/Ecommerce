import re
from pymongo import MongoClient
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

client = MongoClient('mongodb://localhost:27017/')
db = client['mydatabase']
users_collection = db['users']
products_collection = db['products']

class RecommendationModel:
    def __init__(self, db_name='mydatabase', user_collection='users', product_collection='products'):
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client[db_name]
        self.users_collection = self.db[user_collection]
        self.products_collection = self.db[product_collection]

    def recommend_products(self, search_query, num_results=5):
        search_regex = re.compile(re.escape(search_query), re.IGNORECASE)
        query = {"$or": [{"Name": {"$regex": search_regex}}, {"Short_description": {"$regex": search_regex}}]}
        recommended_products = list(self.products_collection.find(query).limit(num_results))
        return recommended_products