from os import access
from flask import Flask, jsonify, Response
from werkzeug.wrappers import Request
from flask_jwt_extended import decode_token
from jwt.exceptions import ExpiredSignatureError
import src
app = src


class SimpleMiddleWare(object):
    """
        Simple WSGI middleware
    """
    def __init__(self, app):
        self.app = app
    def __call__(self, environ, start_response):
        request = Request(environ)
        try:
            if 'Authorization' in request.headers:
                token = request.headers.get('Authorization').split(' ')[1]
                with app.create_app().app_context():
                    payload = decode_token(token)
                environ['payload'] = payload
            return self.app(environ, start_response)
        except ExpiredSignatureError as e:
            res = Response("Token expired", mimetype="application/json", status=401)
            return res(environ, start_response) 

        