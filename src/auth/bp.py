from crypt import methods
from flask import Blueprint
from .views import RegisterAPI, LoginAPI

class APIBlueprint(Blueprint):
    def __init__(self):
        super(APIBlueprint, self).__init__("auth", __name__, url_prefix="/auth/v1")
        self.add_url_rule('/register', view_func=RegisterAPI.as_view("register"), methods=['POST',])
        self.add_url_rule('/login', view_func=LoginAPI.as_view("login"), methods=['POST',])
