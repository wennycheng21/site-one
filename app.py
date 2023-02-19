# -- Import section --
from flask import Flask
from flask import render_template
from flask import request
from flask_pymongo import PyMongo
from flask import redirect
from flask import session
from datetime import datetime
from model import getShelter
from model import womenShelter
from model import menShelter
from model import youthShelter
from model import lgbtqShelter
from model import formResult
import random 
from model import mapTableCategories

# import requests
import os
from model import womenShelter


# -- Initialization section --
app = Flask(__name__)

# name of database
app.secret_key = os.getenv("SECRET_KEY")
uri_password = os.getenv("PASSWORD")
# app.config['MONGO_DBNAME'] = 'database-name'
app.config['MONGO_DBNAME'] = 'database'

# URI of database
app.config['MONGO_URI'] = 'mongodb+srv://admin:' + uri_password + \
    '@cluster0.lndrp.mongodb.net/database?retryWrites=true&w=majority'

mongo = PyMongo(app)

id_number = random.randrange(1000, 9999)


# URI of database
# app.config['MONGO_URI'] = 'mongo-uri'

# mongo = PyMongo(app)

# -- Routes section --
# INDEX

@app.route('/')
@app.route('/index')
def index():
    return render_template('index_copy.html', time=datetime.now())

@app.route('/map', methods = ["GET", "POST"])
def locations():
    if request.method == "GET":
        return render_template("map.html")
    else:
        # state = request.form["state"]
        gender = request.form["gender"]
        age = request.form["age"]
        dMap = mapTableCategories(gender,age)
        print(dMap)
        return render_template('map.html',
                        dMap = dMap)

# CONNECT TO DB, ADD DATA

@app.route('/yourShelter', methods=['GET', 'POST'])
def yourShelter():
    # users = mongo.db.users

    shelter_info = getShelter()
    print(shelter_info)

    return render_template('shelter.html', time=datetime.now(), shelter_info = shelter_info)


@app.route('/women', methods=['GET', 'POST'])
def women():
    users = mongo.db.users
    womenShelter_info = womenShelter(users)
    print(womenShelter_info)
    return render_template('women18+.html', time=datetime.now(), womenShelter_info=womenShelter_info)


@app.route('/men', methods=['GET', 'POST'])
def men():
    users = mongo.db.users
    menShelter_info = menShelter(users)
    print(menShelter_info)
    return render_template('men18+.html', time=datetime.now(), menShelter_info=menShelter_info)


@app.route('/youth', methods=['GET', 'POST'])
def youth():
    users = mongo.db.users
    youthShelter_info = youthShelter(users)
    print(youthShelter_info)
    return render_template('youth.html', time=datetime.now(), youthShelter_info=youthShelter_info)


@app.route('/lgbtq', methods=['GET', 'POST'])
def lgbtq():
    users = mongo.db.users
    lgbtqShelter_info = lgbtqShelter(users)
    print(lgbtqShelter_info)
    return render_template('lgbtq.html', time=datetime.now(), lgbtqShelter_info=lgbtqShelter_info)


@app.route('/donatevolunteer', methods=['GET', 'POST'])
def donatevolunteer():
    return render_template('donatevolunteer.html', time=datetime.now())

@app.route('/reference', methods=['GET', 'POST'])
def reference():
    return render_template('reference.html', time=datetime.now())

# @app.route('/map', methods=['GET', 'POST'])
# def map():
#     mapTableCategories()
#     return render_template('map.html', time=datetime.now())

@app.route('/transportation', methods=['GET', 'POST'])
def transportation():
    return render_template('transporation.html', time=datetime.now())

# def womenShelter():
#     shelter_request_link = "https://maps2.dcgis.dc.gov/dcgis/rest/services/DCGIS_DATA/Public_Service_WebMercator/MapServer/25/query?where=1%3D1&outFields=*&outSR=4326&f=json"
#     women = requests.get(shelter_request_link).json()
#     if users.find({"gender": "Women"}) :
#         return women['features'][0]['attributes']['ADDRESS']
#         return women['features'][7]['attributes']['ADDRESS']
#         return women['features'][9]['attributes']['ADDRESS']
#         return women['features'][12]['attributes']['ADDDRESS']
#         return women['features'][14]['attributes']['ADDRESS']

    # connect to the database
    # events = mongo.db.events

    # insert new data
   # events.insert({"event": "First Day of Classes",
    # "date": "2021-09-13"})

    # events.insert({"event": "birthday",
    # "date": "2003-04-24"})

    # return a message to the user
    # Ro uncommented this because she was not sure what it did and it brought up an error.
    # return render_template("shelter.html", time=datetime.now()) #shelter_info = shelter_info)


@app.route('/resource', methods=['GET', 'POST'])
def resource():
    users = mongo.db.users
   # form_info = formResult(users)
   # print(form_info)

    if users.find({"age": "Under 11"}):
        return render_template("resource.html", time=datetime.now())
    elif users.find({"reside": "No"}):
        return render_template("resource.html", time=datetime.now())
    else:
        return redirect('/yourShelter')
        # return render_template("resource.html", time=datetime.now())
# login page
# @app.route('/form', methods = ['GET', 'POST'])
# def form():
#     if request.method == "GET":
#         return render_template("form.html")
#     else:
#         form = mongo.db.forms


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == "GET":
        message = "Your ID will be DC" + str(id_number)
        return render_template("signup.html", message = message)

        # this stores form data into a user's dictionary
    else:
        users = mongo.db.users
        user = {
            "username": request.form["username"],
            "password": request.form["password"],
            "reside": request.form["reside"],
            "age": request.form["age"],
            "gender": request.form["gender"],
            # "type_assistance": request.form["type_assistance"]
        }

        # checks if user already exists in the database
        existing_user = users.find_one({'username': user['username']})
        user_age = request.form["age"]
        user_gender = request.form["gender"]
        user_reside = request.form["reside"]
        # make condition to check if user already exists in mongo
        if existing_user is None:
            users.insert(user)  # add our user data into mongo

       # tell the browser session who the user is
            session["username"] = request.form["username"]
            
            if user_reside == "NO" and user_age == "11-17":
                return redirect('/resource')
            elif user_age == "11-17" and user_reside == "YES":
                return redirect ('/youth')
            elif user_age == "Under 11":
                return redirect ('/resource')
            elif user_age == "18+" and user_gender == "Female" and user_reside == "NO":
                return redirect('/resource')
            elif user_age == "18+" and user_gender == "Male" and user_reside == "NO":
                return redirect('/resource')
            elif user_age == "18+" and user_gender == "Female":
                return redirect('/women')
            elif user_age == "18+" and user_gender == "Male":
                return redirect('/men')
            elif user_age == "18+" and user_gender == "lgbtq":
                return redirect('/lgbtq')
            elif user_age == "18+" and user_gender == "lgbtq" and user_reside == "NO":
                return redirect('/resource')
            
            # elif user_age == "Under 11" and user_reside == "Yes" :
            #     return redirect ('/resource')
            # elif user_age == "Under 11" and user_reside == "No" :
            #     return redirect ('/resource')
            # elif user_age == "11-17" and user_reside == "No" :
            #     return redirect ('/resource')
            # elif user_age == "11-17" and user_reside == "Yes":
            #     return redirect ('/youth')

            # elif user_reside == "No" :
            #     return redirect ('/resource')

            # elif user_age == "18+" and user_gender == "Women" and user_reside == "No":
            #     return redirect('/resource')
            
            # elif user_gender == "Women" and user_reside == "No":
            #     return redirect('/women')
            
            # elif user_gender == "Men":
            #     return redirect('/men')

            # elif user_gender == "lgbtq":
            #     return redirect('/lgbtq')

            # elif user_age == "18+" and user_gender == "Men" and user_reside == "No":
            #     return redirect('/resource')

            #return "Congratulations, you made an account: @" + request.form["username"]
            # if user_age == "11-17":
            #     return redirect ('/youth')

            # elif user_age == "Under 11":
            #     return render_template("resource.html")

            # else:
            #     return render_template("women18+.html")

            # return render_template('/')
        else:
            return "Unfortunately, this username is taken. Please try again." + render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    users = mongo.db.users
    if request.method == "GET":
        return render_template("login.html")
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
                return redirect('/')
            else:
                error = "Incorrect password. Please try again. If you haven't registered, please make an account."
                return render_template('login.html', error=error)

        else:
            return redirect('/signup')


@app.route('/logout')
def logout():
    # removes session
    session.clear()
    return redirect('/')

# @app.route('/locations/table')
# def locations():
#     return render_template('locations_table.html')





