import pymongo
import secrets
import smtplib
from email.message import EmailMessage
from aiohttp import web
from aiohttp_session import new_session
import aiohttp_jinja2
from .base import BaseView

# Establish a connection to MongoDB
client = pymongo.MongoClient("mongodb+srv://DataBase:DataBase@cluster0.uxw4hon.mongodb.net/?retryWrites=true&w=majority")
db = client["user_db"]
users_collection = db["users"]

class ForgotPasswordView(BaseView):
    @aiohttp_jinja2.template("forgot_password.html")
    async def forgot_password_get(self, req: web.Request) -> web.Response:
        return dict(authenticated=False, **req.query)

    async def forgot_password_post(self, req: web.Request) -> web.Response:
        post_data = await req.post()
        redirect_to = post_data.get("redirect_to") or "/login"
        location = req.app.router["forget_page"].url_for()
        if redirect_to != "/login":
            location = location.update_query({"redirect_to": redirect_to})
        email = post_data.get("email")  # Assuming you collect email for password reset
        
        if not email:
            # Handle error if email is missing
            return web.Response(text="Email is required for password reset")

        # Check if the email exists in the database
        user = users_collection.find_one({"email": email})
        
        if not user:
            # Handle case when the email is not found in the database
            return web.Response(text="Email not found in records")

        # Generate a unique token for password reset (use a more secure token generation method in production)
        reset_token = secrets.token_urlsafe(32)

        # Store the reset token in the user's document in the database
        users_collection.update_one({"email": email}, {"$set": {"reset_token": reset_token}})

        # Send password reset link to the user's email
        reset_link = f"http://yourdomain.com/reset-password?token={reset_token}"
        await send_reset_email(email, reset_link)

        return web.Response(text="Password reset instructions sent to your email")

class ResetPasswordView(BaseView):
    @aiohttp_jinja2.template("reset_password.html")
    async def reset_password_get(self, req: web.Request) -> web.Response:
        token = req.query.get("token")

        # Validate the reset token
        user = users_collection.find_one({"reset_token": token})

        if not user:
            return web.Response(text="Invalid or expired token")

        # Render the password reset form with token as a hidden field
        return web.Response(text="Render your password reset form here")

    async def reset_password_post(self, req: web.Request) -> web.Response:
        post_data = await req.post()
        redirect_to = post_data.get("redirect_to") or "/login"
        location = req.app.router["reset_page"].url_for()
        if redirect_to != "/login":
            location = location.update_query({"redirect_to": redirect_to})
        token = post_data.get("token")
        new_password = post_data.get("new_password")

        # Validate the reset token
        user = users_collection.find_one({"reset_token": token})

        if not user:
            return web.Response(text="Invalid or expired token")

        # Update user's password with the new password
        users_collection.update_one({"reset_token": token}, {"$set": {"password": new_password}})

        return web.Response(text="Password updated successfully")

async def send_reset_email(email, reset_link):
    smtp_server = 'smtp.google.com'  # Replace with your SMTP server details
    sender_email = 'alantunemusic@gmail.com'  # Replace with your sender email
    sender_password = 'hvxggzbubxvhabtd'  # Replace with your sender email password

    msg = EmailMessage()
    msg['From'] = sender_email
    msg['To'] = email
    msg['Subject'] = "Password Reset"
    msg.set_content(f"Click the link to reset your password: {reset_link}")

    try:
        with smtplib.SMTP(smtp_server) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
    except smtplib.SMTPException as e:
        print(f"Failed to send email: {e}")



        session = await new_session(req)
        session["forget_in"] = True
        session["forget_in_at"] = time.time()
        return web.HTTPFound(location=redirect_to)
