from aiohttp import web
import time
import aiohttp_jinja2
from aiohttp_session import new_session
import pymongo
from email.message import EmailMessage
import smtplib
from .base import BaseView

client = pymongo.MongoClient("mongodb+srv://DataBase:DataBase@cluster0.uxw4hon.mongodb.net/?retryWrites=true&w=majority")
db = client["user_db"]
users_collection = db["users"]

async def send_email(recipient, subject, message):
    # Fill in your valid SMTP server details
    smtp_server = 'smtp.google.com'
    smtp_port = 587
    sender_email = 'alantunemusic@gmail.com'
    sender_password = 'hvxggzbubxvhabtd'
    
    msg = EmailMessage()
    msg['From'] = sender_email
    msg['To'] = recipient
    msg['Subject'] = subject
    msg.set_content(message)

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
    except smtplib.SMTPException as e:
        print(f"Failed to send email: {e}")

class SignupView(BaseView):
    @aiohttp_jinja2.template("signup.html")
    async def signup_get(self, req: web.Request) -> web.Response:
        return dict(authenticated=False, **req.query)

    async def signup_post(self, req: web.Request) -> web.Response:
        post_data = await req.post()
        redirect_to = post_data.get("redirect_to") or "/login"
        location = req.app.router["signup_page"].url_for()
        if redirect_to != "/login":
            location = location.update_query({"redirect_to": redirect_to})

        email = post_data.get("email")
        username = post_data.get("username")
        password = post_data.get("password")

        # Check for missing fields
        if not email:
            loc = location.update_query({"error": "email missing"})
            return web.HTTPFound(location=loc)

        if not username:
            loc = location.update_query({"error": "Username missing"})
            return web.HTTPFound(location=loc)

        if not password:
            loc = location.update_query({"error": "Password missing"})
            return web.HTTPFound(location=loc)

        # User creation and related actions
        user = {"username": username, "password": password, "email": email}
        users_collection.insert_one(user)

        # Notify user about successful signup
        await send_email(email, "Signup Successful", "You have successfully signed up!")

        # Redirect to the login page after successful signup
        session = await new_session(req)
        session["signed_in"] = True
        session["signed_in_at"] = time.time()

        # Redirect to a success page or another route after signup
        return web.HTTPFound(location=redirect_to)  # Redirect to the appropriate endpoint
