from os import access
from flask import Flask, jsonify, request, Response
from werkzeug.wrappers import Request
from jwt import decode
from flask_jwt_extended import get_jwt_identity


class SimpleMiddleWare(object):
    """
        Simple WSGI middleware
    """
    def __init__(self, app):
        self.app = app
    def __call__(self, environ, start_response):
        req = Request(environ)
        if 'Authorization' in req.headers:
            token = req.headers.get('Authorization').split(' ')[1]
        print('something you want done in every http request')
        a = 10
        if a == 10:
            res = Response(u'Authorization failed', mimetype='text/plain',
                       status=401)
            return res(environ, start_response)
        return self.app(environ, start_response)