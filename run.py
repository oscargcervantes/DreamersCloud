#!env/bin/python
# -*- coding: utf-8 -*-
from flask import Flask, render_template, json, request,redirect,session
from import_file import import_file
from datetime import datetime
import os, pprint as p
import re
from flask import abort, jsonify, g, url_for
from flask_httpauth import HTTPBasicAuth
import unicodedata

rootdir = os.path.dirname(os.path.abspath(__file__))
import_file(rootdir + '/definitions/User.py')
import_file(rootdir + '/definitions/Parser.py')
import_file(rootdir + '/definitions/MongoDB.py')
import_file(rootdir + '/definitions/Password.py')

from User import user
from Parser import parser
from MongoDB import connect
from Password import generate_auth_token, verify_auth_token, verify_password

#Get configuration DB parameters
filename = "config.cfg"
ini = parser(filename)
db_host = ini['mongodb']['host']
db_user = ini['mongodb']['user']
db_password = ini['mongodb']['passwd']
db_database = ini['mongodb']['db']
db_collection = ini['mongodb']['collection']
db_port = ini['mongodb']['port']

#MongoDB connection
#conn = connect(db_host,db_port,db_user,db_password,db_database,db_collection) 

#Initialization
app = Flask(__name__)
app.config['SECRET_KEY'] = ini['app']['secret_key'] 
app.jinja_env.add_extension('jinja2.ext.do')
app.config['THREADS_PER_PAGE'] = 2

# Enable protection agains *Cross-site Request Forgery (CSRF)*
app.config['CSRF_ENABLED'] = True

# Use a secure, unique and absolutely secret key for
# signing the data. 
app.config['CSRF_SESSION_KEY'] = ini['app']['secret_key']

# extensions
auth = HTTPBasicAuth()

@app.route("/")
def start():
    if session.get('user'):
        data = session['messages']
        return redirect('/dashboard')
    else:
        return render_template('login.html')

@app.route("/login",methods=['POST'])
def login():
    try:
        data = {}
        username = request.form['username']
        password = request.form['password']
        conn = connect(db_host, db_port, db_user, db_password, db_database, db_collection)
        l = list(conn.find({"username": { "$in": [str(username)] }}))        
        if l:
            if verify_password(password,l[0]['password']):
                session['user'] = l[0]['username']
                data['email'] = l[0]['email']
                data['name'] = l[0]['name']
                data['role'] =  l[0]['role']
                session['messages'] = data             
                return redirect('/dashboard')
            else:
                return render_template('login.html',error='Wrong username or password')
        else:
            return render_template('login.html',error='Username not found, please Signup instead')
    except Exception as e:
        return render_template('page_404.html',error=str(e))    

@app.route("/signup",methods=['POST'])
def signup():
    try:
        data = {}
        username = request.form['username']
        password = request.form['password']
        repassword = request.form['re-password']
        email = request.form['email']
        name = request.form['name']
        u = user(name,email,username,password)
        conn = connect(db_host, db_port, db_user, db_password, db_database, db_collection)
        _u = list(conn.find({"username": { "$in": [str(username)] }}))
        _e = list(conn.find({"email": { "$in": [str(email)] }}))
        if password == repassword:
            if _u:
                return render_template('login.html',error='User already exist in our DB')
            elif _e:
                return render_template('login.html',error='Email already exist in our DB')
            else:
                conn.insert(u.record())
                return render_template('login.html',error='Succesfully added, please login')
        else:
            print('Passwords does not match')
            #return redirect(url_for('', _anchor='signup', code=307))
            return render_template('login.html',error='Passwords does not match')
            #return redirect(flask.url_for(''), code=307)				
    except Exception as e:
        return render_template('page_404.html',error=str(e)) 

@app.route('/logout')
def logout():
    session.pop('user',None)
    return redirect('/')

@app.route('/dashboard')
def dashboard():
    if session.get('user'):
        data = session['messages']
        return render_template('index.html', data=data)
    else:
        return render_template('page_404.html',error = 'Unauthorized Access')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port='9080')
