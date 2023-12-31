import time
import firebase_admin
from firebase_admin import credentials, auth
from aiohttp import web
import aiohttp_jinja2
from aiohttp_session import new_session
from .base import BaseView

# Initialize Firebase Admin SDK with your service account credentials
cred = credentials.Certificate('/serviceAccountKey.json')  # Replace with your service account key
firebase_admin.initialize_app(cred)

class LoginView(BaseView):
    @aiohttp_jinja2.template("login.html")
    async def login_get(self, req: web.Request) -> web.Response:
        return dict(authenticated=False, **req.query)

    async def login_post(self, req: web.Request) -> web.Response:
        post_data = await req.post()
        redirect_to = post_data.get("redirect_to") or "/"
        location = req.app.router["login_page"].url_for()
        if redirect_to != "/":
            location = location.update_query({"redirect_to": redirect_to})

        if "username" not in post_data:
            loc = location.update_query({"error": "Username missing"})
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

        if "email" not in post_data:
            loc = location.update_query({"error": "Email missing"})
            return web.HTTPFound(location=loc)

        if "password" not in post_data:
            loc = location.update_query({"error": "Password missing"})
            return web.HTTPFound(location=loc)

        try:
            user = auth.create_user(
                email=post_data["email"],
                password=post_data["password"]
            )
        except ValueError as e:
            loc = location.update_query({"error": str(e)})
            return web.HTTPFound(location=loc)
        except auth.EmailAlreadyExistsError:
            loc = location.update_query({"error": "Email already exists"})
            return web.HTTPFound(location=loc)

        session = await new_session(req)
        session["logged_in"] = True
        session["logged_in_at"] = time.time()
        return web.HTTPFound(location=redirect_to)
