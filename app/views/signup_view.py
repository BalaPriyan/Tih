from aiohttp_session import new_session
from firebase_admin import auth
from aiohttp import web
from aiohttp_jinja2 import template
import time

class SignupView(BaseView):
    @template("signup.html")
    async def signup_get(self, req: web.Request) -> web.Response:
        return dict(**req.query)

    async def signup_post(self, req: web.Request) -> web.Response:
        post_data = await req.post()
        redirect_to = post_data.get("redirect_to") or "/"
        location = req.app.router["signup_page"].url_for()
        if redirect_to != "/":
            location = location.update_query({"redirect_to": redirect_to})

        required_fields = ["firstname", "lastname", "email", "password"]
        if not all(field in post_data for field in required_fields):
            loc = location.update_query({"error": "Missing required fields"})
            return web.HTTPFound(location=loc)

        try:
            user = auth.create_user(
                email=post_data["email"],
                password=post_data["password"],
                display_name=f"{post_data['firstname']} {post_data['lastname']}",
            )
        except auth.EmailAlreadyExistsError:
            loc = location.update_query({"error": "Email already exists"})
            return web.HTTPFound(location=loc)

        session = await new_session(req)
        session["logged_in"] = True
        session["logged_in_at"] = time.time()
        return web.HTTPFound(location=redirect_to)
