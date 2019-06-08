#!/usr/bin/env python
# Laptop Service
from flask import Flask, request, session
import flask
from flask import request
import pymongo
from pymongo import MongoClient
from flask_restful import Resource, Api
import os
import time
from flask import Flask, request, session, render_template, redirect, url_for, flash
from flask_login import (LoginManager, current_user, login_required,
                            login_user, logout_user, UserMixin,
                            confirm_login, fresh_login_required)
from flask_wtf.csrf import CSRFProtect
from random import randint
from wtforms import Form, BooleanField, StringField, validators, PasswordField
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer \
                                  as Serializer, BadSignature, \
                                  SignatureExpired)

app = Flask(__name__)
#csrf = CSRFProtect(app)
api = Api(app)

client = MongoClient("172.18.0.2", 27017)

db = client.tododb

users = db.userdb

login_manager = LoginManager()

login_manager.init_app(app)

login_manager.login_view = ('/api/login')

app.config['SECRET_KEY'] = "When all else fails"

#session['token'] = None

class RegisterForm(Form):

    username = StringField('Username', validators=[validators.DataRequired(message=u'Enter username')])

    password = StringField('Password', validators=[validators.DataRequired(message=u'Enter password')])

class LoginForm(Form):

    username = StringField('Username', validators=[validators.DataRequired(message=u'Enter username')])

    password = StringField('Password', validators=[validators.DataRequired(message=u'Enter password')])

    remember = BooleanField('Remember Me')

class UserInfo(UserMixin):

    def __init__(self, user_id):

        self.id = str(user_id)

@app.route("/api/register", methods=["GET", "POST"])
def register():

    session['token'] = None

    form = RegisterForm(request.form)

    username = form.username.data

    password = form.password.data

    new_ID = ""

    if form.validate():

        item = db.tododb.find_one({"username":username})

        new_ID = randint(1,50000)

        if (username == None) or (password == None):

            return 'no username or password given', 400

        if item != None:

            return 'try a different username', 400

        hVal = hash_password(password)

        new = {"_id": new_ID, 'username': username, 'password': hVal}

        users.insert_one(new)

        result = {'location': new_ID, 'username': username, 'password': hVal}

        return flask.jsonify(result=result), 201

    return flask.render_template('register.html', form=form)

@login_manager.user_loader
def load_user(user_id):

    userInfo = users.find({"_id": int(user_id)})

    if (userInfo == None): return None

    return UserInfo(user_id)

def hash_password(password):

    return pwd_context.encrypt(password)

def verify_password(password, hashVal):

    return pwd_context.verify(password, hashVal)

def generate_auth_token(user_id, expiration=600):

    s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)

    token = s.dumps({'id': user_id})

    session['token'] = token

    return {'token': token, 'duration': expiration}

def verify_auth_token(token):

    s = Serializer(app.config['SECRET_KEY'])

    try:

        data = s.loads(token)

    except SignatureExpired:

        return None

    except BadSignature:

        return None

    return "Success"

@app.route("/api/login", methods=["GET", "POST"])
def login():

    form = LoginForm(request.form)

    if (request.method == "POST") and (form.validate()):

        username = form.username.data

        password = form.password.data

        rememberl = form.remember.data

        userInfo = users.find({"username":username})

        try:

            userInfo[0]

        except IndexError:

            return redirect(url_for("register"))

        entry = userInfo[0]

        hVal = entry['password']

        if verify_password(password, hVal) is True:

            acting_iden = entry['_id']

            session['user_id'] = acting_iden

            user = UserInfo(acting_iden)

            login_user(user, remember = rememberl)

            return redirect(request.args.get("next") or url_for("token"))

        else: return redirect(url_for("register"))

    return flask.render_template('login.html', form=form)

@app.route("/api/logout")
@login_required
def logout():

    session['token'] = None

    logout_user()

    return "You've been Logged out"

@app.route("/")
def index():

    return flask.render_template("index.html")

@app.route("/api/token", methods=['GET'])
@login_required

def token():

    user_id = session.get('user_id')

    tokenInfo = generate_auth_token(user_id, 600)

    retToken = tokenInfo['token']

    retToken = retToken.decode('utf-8')

    result = {'token': retToken, 'duration': 60}

    return flask.jsonify(result=result)

class all(Resource):

    def get(self):

        if 'token' in session:

            if session['token'] == None: return 'No token', 401

        else:

            token = request.args.get('token')

            if token == None: return 'No token', 401

        verify = verify_auth_token(session['token'])

        if verify == None: return 'token could not be verified', 401

        top = request.args.get("top")

        if (top == None): top = 20

        _items = db.tododb.find().sort("openTime", pymongo.ASCENDING).limit(int(top))

        items = [item for item in _items]

        return {

            'openTime': [item['open_time'] for item in items],

            'closeTime': [item['close_time'] for item in items]
        }


class allJson(Resource):

    def get(self):

        if 'token' in session:

            if session['token'] == None: return 'No token', 401

        else:

            token = request.args.get('token')

            if token == None: return 'No token', 401

        verify = verify_auth_token(session['token'])

        if verify == None: return 'token could not be verified', 401

        top = request.args.get("top")

        if (top == None): top = 20

        _items = db.tododb.find().sort("openTime", pymongo.ASCENDING).limit(int(top))

        items = [item for item in _items]

        return {

            'openTime': [item['open_time'] for item in items],

            'closeTime': [item['close_time'] for item in items]
        }

class allCSV(Resource):

    def get(self):

        if 'token' in session:

            if session['token'] == None: return 'No token', 401

        else:

            token = request.args.get('token')

            if token == None: return 'No token', 401

        verify = verify_auth_token(session['token'])

        if verify == None: return 'token could not be verified', 401

        top = request.args.get("top")

        if (top == None): top = 20

        _items = db.tododb.find().sort("openTime", pymongo.ASCENDING).limit(int(top))

        items = [item for item in _items]

        csv = ""

        for item in items:

            csv += item['open_time'] + ', ' + item['close_time'] + ', '

        return csv

class open(Resource):

    def get(self):

        if 'token' in session:

            if session['token'] == None: return 'No token', 401

        else:
            token = request.args.get('token')

            if token == None: return 'No token', 401

        verify = verify_auth_token(session['token'])

        if verify == None: return 'token could not be verified', 401

        top = request.args.get("top")

        if (top == None): top = 20

        _items = db.tododb.find().sort("openTime", pymongo.ASCENDING).limit(int(top))

        return {

            'openTime': [item['open_time'] for item in _items]
        }

class openJson(Resource):

    def get(self):

        if 'token' in session:

            if session['token'] == None: return 'No token', 401

        else:

            token = request.args.get('token')

            if token == None: return 'No token', 401

        verify = verify_auth_token(session['token'])

        if verify == None: return 'token could not be verified', 401


        top = request.args.get("top")

        if (top == None): top = 20

        _items = db.tododb.find().sort("openTime", pymongo.ASCENDING).limit(int(top))

        return {

            'openTime': [item['open_time'] for item in _items]
        }

class openCSV(Resource):

    def get(self):

        if 'token' in session:

            if session['token'] == None: return 'No token', 401

        else:

            token = request.args.get('token')

            if token == None: return 'No token', 401

        verify = verify_auth_token(session['token'])

        if verify == None: return 'token could not be verified', 401

        top = request.args.get("top")

        if (top == None): top = 20

        _items = db.tododb.find().sort("openTime", pymongo.ASCENDING).limit(int(top))

        items = [item for item in _items]

        csv = ""

        for item in items:

            csv += item['open_time'] + ', '

        return csv

class close(Resource):

    def get(self):

        if 'token' in session:

            if session['token'] == None: return 'No token', 401

        else:

            token = request.args.get('token')

            if token == None: return 'No token', 401

        verify = verify_auth_token(session['token'])

        if verify == None: return 'token could not be verified', 401

        top = request.args.get("top")

        if (top == None): top = 20

        _items = db.tododb.find().sort("closeTime", pymongo.ASCENDING).limit(int(top))

        return {

            'closeTime': [item['close_time'] for item in _items]
        }

class closeJson(Resource):

    def get(self):

        if 'token' in session:

            if session['token'] == None: return 'No token', 401

        else:

            token = request.args.get('token')

            if token == None: return 'No token', 401

        verify = verify_auth_token(session['token'])

        if verify == None: return 'token could not be verified', 401


        top = request.args.get("top")

        if (top == None): top = 20

        _items = db.tododb.find().sort("closeTime", pymongo.ASCENDING).limit(int(top))

        return {

            'closeTime': [item['close_time'] for item in _items]
        }

class closeCSV(Resource):

    def get(self):

        if 'token' in session:

            if session['token'] == None: return 'No token', 401

        else:

            token = request.args.get('token')

            if token == None: return 'No token', 401

        verify = verify_auth_token(session['token'])

        if verify == None: return 'token could not be verified', 401

        top = request.args.get("top")

        if (top == None): top = 20

        _items = db.tododb.find().sort("closeTime", pymongo.ASCENDING).limit(int(top))

        items = [item for item in _items]

        csv = ""

        for item in items:

            csv += item['close_time'] + ', '

        return csv

api.add_resource(all, '/listAll')

api.add_resource(allJson, '/listAll/json')

api.add_resource(allCSV, '/listAll/csv')

api.add_resource(open, '/listOpenOnly')

api.add_resource(openJson, '/listOpenOnly/json')

api.add_resource(openCSV, '/listOpenOnly/csv')

api.add_resource(close, '/listCloseOnly')

api.add_resource(closeJson, '/listCloseOnly/json')

api.add_resource(closeCSV, '/listCloseOnly/csv')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
    #csrf.init_app(app)
