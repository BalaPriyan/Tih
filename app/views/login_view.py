import time
import firebase_admin
from firebase_admin import credentials, auth
from aiohttp import web
import aiohttp_jinja2
from aiohttp_session import new_session
from .base import BaseView
<<<<<<< HEAD

# Initialize Firebase Admin SDK with your service account credentials
cred = credentials.Certificate('app/views/serviceAccountKey.json')  # Replace with your service account key
firebase_admin.initialize_app(cred)
=======
import pyrebase
from flask import render_template, request, redirect, session
from app import app
import os
>>>>>>> f48458df6c94c8aaffd1702096105a8b70c61072

config = {
    "apiKey": "",
    "authDomain": "",
    "databaseURL": "",
    "projectId": "",
    "storageBucket": "",
    "messagingSenderId": "",
    "appId": ""
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

<<<<<<< HEAD
        if "email" not in post_data:
            loc = location.update_query({"error": "Email missing"})
            return web.HTTPFound(location=loc)

        if "password" not in post_data:
            loc = location.update_query({"error": "Password missing"})
            return web.HTTPFound(location=loc)

        try:
            user = auth.get_user_by_email(post_data["email"])
            # Check if the entered password matches the Firebase user's password
            auth_user = auth.verify_password(user.uid, post_data["password"])
            if not auth_user:
                loc = location.update_query({"error": "Wrong email or Password"})
                return web.HTTPFound(location=loc)
        except auth.UserNotFoundError:
            loc = location.update_query({"error": "User not found"})
            return web.HTTPFound(location=loc)
        except auth.InvalidPasswordError:
            loc = location.update_query({"error": "Wrong email or Password"})
            return web.HTTPFound(location=loc)

        session = await new_session(req)
        session["logged_in"] = True
        session["logged_in_at"] = time.time()
        return web.HTTPFound(location=redirect_to)

    @aiohttp_jinja2.template("signup.html")
    async def signup_get(self, req: web.Request) -> web.Response:
        return dict(authenticated=False, **req.query)

    async def signup_post(self, req: web.Request) -> web.Response:
        post_data = await req.post()
        redirect_to = post_data.get("redirect_to") or "/"
        location = req.app.router["signup_page"].url_for()
        if redirect_to != "/":
            location = location.update_query({"redirect_to": redirect_to})

        # Extracting fields from signup form
        first_name = post_data.get("first_name")
        last_name = post_data.get("last_name")
        email = post_data.get("email")
        password = post_data.get("password")

        if not all([first_name, last_name, email, password]):
            loc = location.update_query({"error": "All fields are required"})
            return web.HTTPFound(location=loc)

        try:
            user = auth.create_user(
                email=email,
                password=password,
                display_name=f"{first_name} {last_name}"
            )
        except ValueError as e:
            loc = location.update_query({"error": str(e)})
            return web.HTTPFound(location=loc)
        except auth.EmailAlreadyExistsError:
            loc = location.update_query({"error": "Email already exists"})
            return web.HTTPFound(location=loc)
=======

@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def index():
    if (request.method == 'POST'):
            email = request.form['name']
            password = request.form['password']
            try:
                auth.sign_in_with_email_and_password(email, password)
                #user_id = auth.get_account_info(user['idToken'])
                #session['usr'] = user_id
                return render_template('home.html')
            except:
                unsuccessful = 'Please check your credentials'
                return render_template('login.html', umessage=unsuccessful)
    return render_template('login.html')

@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    if (request.method == 'POST'):
            email = request.form['name']
            password = request.form['password']
            auth.create_user_with_email_and_password(email, password)
            return render_template('login.html')
    return render_template('create_account.html')
>>>>>>> f48458df6c94c8aaffd1702096105a8b70c61072

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if (request.method == 'POST'):
            email = request.form['name']
            auth.send_password_reset_email(email)
            return render_template('login.html')
    return render_template('forgot_password.html')

@app.route('/home', methods=['GET', 'POST'])
def home():
    return render_template('home.html')


if __name__ == '__main__':
    app.run()
