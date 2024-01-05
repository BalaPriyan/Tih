import pymongo
from aiohttp import web
import aiohttp_jinja2
from aiohttp_session import new_session
from .base import BaseView

# Establish a connection to MongoDB
client = pymongo.MongoClient("mongodb+srv://DataBase:DataBase@cluster0.uxw4hon.mongodb.net/?retryWrites=true&w=majority")
db = client["user_db"]
users_collection = db["users"]

class LoginView(BaseView):
    @aiohttp_jinja2.template("login.html")
    async def login_get(self, req: web.Request) -> web.Response:
        return web.Response(text="Render your login form here")  # Replace with your form rendering logic

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

        # Retrieve user from MongoDB
        user = users_collection.find_one({"username": post_data["username"]})

        if not user or user["password"] != post_data["password"]:
            loc = location.update_query({"error": "Wrong Username or Password"})
            return web.HTTPFound(location=loc)

        session = await new_session(req)
        session["logged_in"] = True
        session["logged_in_at"] = time.time()
        return web.HTTPFound(location=redirect_to)
