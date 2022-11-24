from crypt import methods
from flask import Blueprint
from src.api.auth import RegisterAPI, LoginAPI, TokenCheckAPI, GetAccessTokenAPI
from src.api.quote import AddQuoteAPI
from src.api.todo import ToDoAPI
from src.api.content import ContentManagement
from src.api.wtf_form import WTFFormAPI


class AuthBlueprint(Blueprint):
    def __init__(self):
        super(AuthBlueprint, self).__init__("auth", __name__, url_prefix="/auth/v1/")
        self.add_url_rule('register/', view_func=RegisterAPI.as_view("register"))
        self.add_url_rule('login/', view_func=LoginAPI.as_view("login"))
        self.add_url_rule('tokenCheck/', view_func=TokenCheckAPI.as_view("tokenCheck"))
        self.add_url_rule('getAccessToken/', view_func=GetAccessTokenAPI.as_view("getAccessToken"))


class QuoteBlueprint(Blueprint):
    def __init__(self):
        super(QuoteBlueprint, self).__init__("quote", __name__, url_prefix="/quote/")
        self.add_url_rule('', view_func=AddQuoteAPI.as_view("quote"))


class ToDoBluprint(Blueprint):
    def __init__(self):
        super(ToDoBluprint, self).__init__("todo", __name__, url_prefix="/todo/")
        self.add_url_rule('', view_func=ToDoAPI.as_view("todo"))
        # self.add_url_rule('/<id>/', view_func=ToDoAPI.as_view("todo_delete"), methods=['PATCH', 'DELETE'])
        # self.add_url_rule('upd/<int:id>/', view_func=ToDoAPI.as_view("todo_update"))
        
        
class WTFFormBlueprint(Blueprint):
    def __init__(self):
        super().__init__('wtf', __name__, url_prefix="/wtf")
        self.add_url_rule('/', view_func=WTFFormAPI.as_view("wtf"))
        # self.add_url_rule('/post/', view_func=WTFFormAPI.as_view("wtf_post"), methods=['POST'])
        
        