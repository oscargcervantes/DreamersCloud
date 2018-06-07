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
from werkzeug.utils import secure_filename
from datetime import datetime
import pyqrcode
#from io import StringIO
import StringIO

rootdir = os.path.dirname(os.path.abspath('__file__'))
#rootdir = os.path.join(os.path.abspath(__file__))
#print(rootdir)
import_file(rootdir + '/definitions/User.py')
import_file(rootdir + '/definitions/Parser.py')
import_file(rootdir + '/definitions/MongoDB.py')
import_file(rootdir + '/definitions/Password.py')
import_file(rootdir + '/definitions/Containers.py')
import_file(rootdir + '/definitions/Validator.py')

from User import user
from Parser import parser
from MongoDB import connect
from Password import generate_auth_token, verify_auth_token, verify_password
from Containers import total_container_number
from Validator import generate_token, validate_token, is_valid_password, is_valid_email

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
conn = connect(db_host,db_port,db_user,db_password,db_database,db_collection) 

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
app.config['UPLOAD_FOLDER'] = ini['profile']['UPLOAD_FOLDER']

# extensions
auth = HTTPBasicAuth()

@app.route('/')
def start():
    if session.get('user'):
        data = session['messages']
        return redirect('/dashboard')
    else:
        session.clear()
        return render_template('login.html')

@app.route('/login',methods=['POST'])
def login():
    try:
        data = {}
        username = request.form['username']
        password = request.form['password']
        #conn = connect(db_host, db_port, db_user, db_password, db_database, db_collection)
        l = list(conn.find({"username": { "$in": [str(username)] }}))
        #Pending to add token field if 2FA was enabled        
        if l:
            if verify_password(password,l[0]['password']):
                session['user'] = l[0]['username']
                data['email'] = l[0]['email']
                data['name'] = l[0]['name']
                data['role'] =  l[0]['role']
                session['messages'] = data
                if l[0]['two_fa']:
                    if not l[0]['two_fa_configured']:
                        print("To setup 2FA")
                        #conn.insert() #Change the two_fa_configured to Enabled
                        conn.update({"username":{"$in":[str(session.get('user'))]}},{"$set":{"two_fa_configured":str('Enabled')}})
                        return redirect('/twofactor')
                    else:
						return redirect('/two_factor_login') #To write only the token created by freeOTP                
                return redirect('/dashboard')
            else:
                session.clear()
                return render_template('login.html',error='Wrong username or password')
        else:
            session.clear()
            return render_template('login.html',error='Username not found, please Signup instead')
    except Exception as e:
        session.clear()
        return render_template('page_404.html',error=str(e))    

@app.route('/twofactor')
def two_factor_setup():
    if session.get('user'):
        data = session['messages']
        # since this page contains the sensitive qrcode, make sure the browser
        # does not cache it
        return render_template('two_factor_setup.html'), 200, {
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        'Pragma': 'no-cache',
        'Expires': '0'}
        #return render_template('index_dev.html', data=data, ct_number=ct_number)
    else:
        session.clear()
        return render_template('page_404.html',error = 'Unauthorized Access')

@app.route('/two_factor_login')
def two_factor_login():
    if session.get('user'):
        print("return template for token only")
        return render_template('token.html')		
    else:
        session.clear()
        return render_template('page_404.html',error = 'Unauthorized Access')

@app.route('/login_2fa',methods=['POST'])
def login_2fa():		
    if session.get('user'):
        token = request.form['token']
        l = list(conn.find({"username": { "$in": [str(session.get('user'))] }}))
        valid = validate_token(token, l[0]['token_secret'])
        if valid:		
            return redirect('/dashboard')
        else:
            #Delete session			
            session.clear()
            return render_template('page_404.html',error = 'Bad Token')    		
    else:
        session.clear()
        return render_template('page_404.html',error = 'Unauthorized Access')

@app.route('/qrcode')
def qrcode():
    if session.get('user'):
        data = session['messages']
        # render qrcode for FreeTOTP
        token_secret = generate_token()
        conn.update({"username":{"$in":[str(session.get('user'))]}},{"$set":{"token_secret":str(token_secret)}})
        url = pyqrcode.create('otpauth://totp/2FA-Demo:'+session.get('user')+'?secret='+token_secret+'&issuer=2FA-Demo')
        stream = StringIO.StringIO()
        url.svg(stream, scale=3)
        return stream.getvalue().encode('utf-8'), 200, {
        'Content-Type': 'image/svg+xml',
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        'Pragma': 'no-cache',
        'Expires': '0'}
    else:#New user
        session.clear()
        return render_template('page_404.html',error = 'Unauthorized Access')


@app.route('/signup',methods=['POST'])
def signup():
    try:
        data = {}
        username = request.form['username']
        password = request.form['password']
        repassword = request.form['re-password']
        email = request.form['email']
        name = request.form['name']
        two_factor_auth = request.form.get('2fa') #None or Enabled
        profile_photo = request.form.get('profile_photo')
        sdate = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        u = user(name,email,username,password,sdate,two_factor_auth)
        #conn = connect(db_host, db_port, db_user, db_password, db_database, db_collection)
        _u = list(conn.find({"username": { "$in": [str(username)] }}))
        _e = list(conn.find({"email": { "$in": [str(email)] }}))
        if not is_valid_email(email):
            return render_template('login.html',error='Invalid email, please type a valid one, example@dreamerscloud.mx')
        if not is_valid_password(password):
            return render_template('login.html',error='Invalid password, please type a valid one, include Uppercase, lowercase, digits and special characters')
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
            session.clear()
            return render_template('login.html',error='Passwords does not match')
            #return redirect(flask.url_for(''), code=307)				
    except Exception as e:
        print(str(e))
        session.clear()
        return render_template('page_404.html',error=str(e)) 

@app.route('/logout')
def logout():
    session.pop('user',None)
    session.clear()
    return redirect('/')

@app.route('/dashboard')
def dashboard():
    if session.get('user'):
        data = session['messages']
        ct_number = total_container_number() #To add vms and ct databases to get number by user
        return render_template('index_dev.html', data=data, ct_number=ct_number)
    else:
        session.clear()
        return render_template('page_404.html',error = 'Unauthorized Access')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=9080)
