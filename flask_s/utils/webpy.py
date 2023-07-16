from flask_login import login_user, logout_user, login_required, current_user
import time


class WebFunc:
    def __init__(self, app):
        self.app = app
        app.jinja_env.filters["islogin1"] = self.islogin1
        app.jinja_env.filters["get_y1"] = self.get_y1

    def islogin1(self, request1):
        if current_user.is_authenticated:
            return current_user.id
        return ""

    def get_y1(self, request1):
        return time.strftime("%H%m%d")
