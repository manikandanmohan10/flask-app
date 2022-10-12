from crypt import methods
from flask import Blueprint
from src.auth.views import RegisterAPI, LoginAPI, TokenCheckAPI, GetAccessTokenAPI

class APIBlueprint(Blueprint):
    def __init__(self):
        super(APIBlueprint, self).__init__("auth", __name__, url_prefix="/auth/v1")
        self.add_url_rule('/register', view_func=RegisterAPI.as_view("register"), methods=['POST',])
        self.add_url_rule('/login', view_func=LoginAPI.as_view("login"), methods=['POST',])
        self.add_url_rule('/tokenCheck', view_func=TokenCheckAPI.as_view("tokenCheck"), methods=['GET',])
        self.add_url_rule('/getAccessToken', view_func=GetAccessTokenAPI.as_view("getAccessToken"), methods=['GET',])
