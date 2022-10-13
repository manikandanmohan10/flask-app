from crypt import methods
from flask import Blueprint
from src.api.auth import RegisterAPI, LoginAPI, TokenCheckAPI, GetAccessTokenAPI
from src.api.quote import AddQuoteAPI


class AuthBlueprint(Blueprint):
    def __init__(self):
        super(AuthBlueprint, self).__init__("auth", __name__, url_prefix="/auth/v1/")
        self.add_url_rule('register/', view_func=RegisterAPI.as_view("register"), methods=['POST',])
        self.add_url_rule('login/', view_func=LoginAPI.as_view("login"), methods=['POST',])
        self.add_url_rule('tokenCheck/', view_func=TokenCheckAPI.as_view("tokenCheck"), methods=['GET',])
        self.add_url_rule('getAccessToken/', view_func=GetAccessTokenAPI.as_view("getAccessToken"), methods=['GET',])


class QuoteBlueprint(Blueprint):
    def __init__(self):
        super(QuoteBlueprint, self).__init__("quote", __name__, url_prefix="/quote/")
        self.add_url_rule('', view_func=AddQuoteAPI.as_view("quote"), methods=['POST',])
