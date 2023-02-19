# -- Import section --
from flask import Flask
from flask import render_template
from flask import request
from flask_pymongo import PyMongo
from flask import redirect
from flask import session
from datetime import datetime
import random 

# import requests
import os


# -- Initialization section --
app = Flask(__name__)

# name of database
app.secret_key = os.getenv("SECRET_KEY")
# uri_password = os.getenv("PASSWORD")
# app.config['MONGO_DBNAME'] = 'database-name'
app.config['MONGO_DBNAME'] = 'database'

# URI of database
app.config['MONGO_URI'] = 'mongodb+srv://admin:g8hzd9cNnFfOOTPk@cluster0.qzsdfn5.mongodb.net/?retryWrites=true&w=majority'

mongo = PyMongo(app)

# -- Routes section --
# INDEX

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', time=datetime.now())

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == "GET":
        return render_template("signup.html", message = message)

        # this stores form data into a user's dictionary
    else:
        users = mongo.db.users
        user = {
            "username": request.form["username"],
            "password": request.form["password"],
        }

        # checks if user already exists in the database
        existing_user = users.find_one({'username': user['username']})
        # make condition to check if user already exists in mongo
        if existing_user is None:
            session["username"] = request.form["username"]
            render_template('login.html')
            users.insert(user)  # add our user data into mongo
        else:
            return "Unfortunately, this username is taken. Please try again." + render_template('signup.html')


@app.route('/login.html', methods=['GET', 'POST'])
def login():
    users = mongo.db.users
    if request.method == "GET":
        return redirect("login.html")
    else:
        # this creates a user's database in mongo db if it doesn't already exist

        # this stores form data into a user's dictionary
        user = {
            "username": request.form["username"],
            "password": request.form["password"]
        }

        # checks if user already exists in the database
        existing_user = users.find_one({'username': user['username']})
        # make condition to check if user already exists in mongo
        if existing_user:
            # if it does exists, we are checking if the password matches
            if user['password'] == existing_user['password']:
                session['username'] = user['username']
                return redirect('/Home')
            else:
                error = "Incorrect password. Please try again. If you haven't registered, please make an account."
                return render_template('login.html', error=error)
        else:
            return redirect('/signup')


@app.route('/logoff')
def logoff():
    # removes session
    session.clear()
    return redirect('/Home')





