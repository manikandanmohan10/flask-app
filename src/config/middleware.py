from flask import Response
from werkzeug.wrappers import Request
from flask_jwt_extended import decode_token
from jwt.exceptions import ExpiredSignatureError
from src.config import excluded_endpoints
from http import HTTPStatus as status
import logging
import src


class CustomMiddleWare(object):
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        request = Request(environ)
        try:
            app = src.create_app()
            with app.app_context():
                if request.path not in excluded_endpoints:
                    tok = request.headers.get('Authorization', False)
                    if not tok:
                        res = Response("Token Required", mimetype="application/json", status=status.BAD_REQUEST)
                        logging.info('Token Required')
                        return res(environ, start_response)
                    tok = tok.split(' ')[1]
                    payload = decode_token(tok)
                    environ['payload'] = payload
                return self.app(environ, start_response)
        except ExpiredSignatureError as e:
            res = Response("Token expired", mimetype="application/json", status=status.UNAUTHORIZED)
            logging.info('Token Required')
            return res(environ, start_response)
        except Exception as e:
            logging.critical(f'Exception -> {str(e)}')
            res = Response(str(e), mimetype="application/json", status=status.INTERNAL_SERVER_ERROR)
            return res(environ, start_response)
