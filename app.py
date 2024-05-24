from flask import Flask, jsonify, render_template, request, redirect, flash , session, url_for
from flask_pymongo import PyMongo
from pymongo import MongoClient
import numpy as np
from recommendation import RecommendationModel

app = Flask(__name__)
app.secret_key = 'your_secret_key'  
recommendation_model = RecommendationModel()

app.config['MONGO_URI'] = 'mongodb://localhost:27017/mydatabase'
client = MongoClient('mongodb://localhost:27017/')
db = client['mydatabase']
users = db['users']
products = db['products']

user_search_history_collection = db['user_search_history']

users_collection = db['users']  
products_collection = db['products']

mongo = PyMongo(app)


User = mongo.db.users


Product = mongo.db.products

def log_user_search(user_id, search_query):
    
    user_search_history_collection.insert_one({'user_id': user_id, 'search_query': search_query})



@app.route('/')
def home():
    products = Product.find()
    return render_template('home.html', products=products)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.find_one({'email': email})
        if user and user['password'] == password:
            session['email'] = email
            flash('Login successful!', 'success')
            return redirect('/')
        else:
            flash('Invalid email or password', 'danger')
            return redirect('/login')
    return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        existing_user = User.find_one({'email': email})
        if existing_user:
            flash('Email already exists. Please use a different email.', 'danger')
            return redirect('/signup')
        else:
            new_user = {'email': email, 'password': password}
            User.insert_one(new_user)
            flash('Account created successfully!', 'success')
            return redirect('/login')
    return render_template('signup.html')

def log_user_search(user_id, query):
    
    user_search_history_collection.insert_one({'user_id': user_id, 'search_query': query})

@app.route('/search', methods=['GET', 'POST'])
def search():
    search_query = request.form.get('search_query')
    user_id = session.get('user_id')
    
    query = request.args.get('query')
    
    if query:
        
        search_results = Product.find({'$or': [{'Name': {'$regex': query, '$options': 'i'}}]})
        
        recommended_products = recommendation_model.recommend_products(query)

        return render_template('search.html', search_results=search_results, recommended_products=recommended_products)
    else:
        
        return render_template('search.html')


def log_user_search(user_id, search_query):
    user_id = session.get('user_id')
    
    user_search_history_collection.insert_one({'user_id': user_id, 'search_query': search_query})

    

def recommend_products_based_on_search_history(user_id, search_query):
    
    user_search_history_collection.insert_one({'user_id': user_id, 'search_query': search_query})



if __name__ == '__main__':
    app.run(debug=True)
