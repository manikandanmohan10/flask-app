import os
from flask import jsonify, render_template, request, Response
from flask.views import MethodView
from marshmallow import ValidationError
from psycopg2 import IntegrityError
from yaml import serialize
from src.models.auth_reg_model import User
from src.models import db
from http import HTTPStatus as status
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import create_access_token, create_refresh_token
from flask_jwt_extended import decode_token
from src.service.mail_service import send_mail
from src.api import fernet
from src.serializers import auth_serializer
from jwt.exceptions import ExpiredSignatureError
import logging


class ContentManagement(MethodView):
    def get(self):
        content = object()
        a = 10

        return Response(a), status.OK
