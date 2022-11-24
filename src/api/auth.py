import os
import threading
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
from zerobounce import ZeroBounceAPI
import logging


class RegisterAPI(MethodView):
    def __init__(self):
        self.serializer_class = auth_serializer.RegisterSerializer()

    def post(self):
        """
        Create a new user
        ---
        tags:
          - users
        definitions:
          - schema:
              id: Group
              properties:
                name:
                 type: string
                 description: the group's name
        parameters:
          - in: body
            name: body
            schema:
              id: User
              required:
                - email
                - name
              properties:
                email:
                  type: string
                  description: email for user
                name:
                  type: string
                  description: name for user
                address:
                  description: address for user
                  schema:
                    id: Address
                    properties:
                      street:
                        type: string
                      state:
                        type: string
                      country:
                        type: string
                      postalcode:
                        type: string
                groups:
                  type: array
                  description: list of groups
                  items:
                    $ref: "#/definitions/Group"
        responses:
          201:
            description: User created
        """
        try:
            data = request.json
            try:
                self.serializer_class.load(data)
            except ValidationError as e:
                raise Exception(str(e))
            username = data.get("username")
            password = data.get("password")
            email = data.get("email")
            if len(password) < 6:
                logging.error('Password length must have above 8 char')
                return Response("Password length is too short"), status.BAD_REQUEST
            encrypted_password = fernet.encrypt(password.encode())
            user = User(username=username, password=str(encrypted_password), email=email)
            db.session.add(user)
            db.session.commit()
            response_data = dict(
                message='User Created Successfully',
                status='success',
                statusCode=status.CREATED
            )
            logging.info('Registered successfully')
            return jsonify(response_data), 201
        except IntegrityError as e:
            response_data = dict(message='Email Already Exists',
                                 status='failure',
                                 statusCode=400
                                 )
            logging.error('Email already exists')
            return jsonify(response_data), status.BAD_REQUEST

    def get(self):
        return render_template("login.html")

class LoginAPI(MethodView):
    def post(self):
        
        serializer_class = auth_serializer.LoginSerializer()
        data = request.json
        try:
            serializer_class.load(data)
        except ValidationError as e:
            raise Exception(str(e))
        email = data.get('email')
        password = data.get('password')
        user = User.query.filter_by(email=email).first()
        if not user:
            raise Exception('user not found')
        passwd = eval(user.password)
        if not fernet.decrypt(passwd).decode() == password:
            raise Exception("Invalid Credentials")
        mail_content = dict(
            subject='Logged In',
            html='You just logged in'
        )
        mail_id = os.getenv('MY_MAIL_ID')
        t1 = threading.Thread(target=send_mail, args=[mail_id, mail_content])
        t1.start()
        refresh_token = create_refresh_token(identity=user.id)
        access_token = create_access_token(identity=user.id)
        encrypted_refresh_token = fernet.encrypt(refresh_token.encode())
        encrypted_access_token = fernet.encrypt(access_token.encode())
        encrypted_email = fernet.encrypt(email.encode())
        encrypted_user_id = fernet.encrypt(str(user.id).encode())
        response_data = dict(
            message='Login verified successfully',
            status='success',
            statusCode=200,
            user_id=str(encrypted_user_id),
            email=str(encrypted_email),
            token=dict(
                refresh_token=str(encrypted_refresh_token),
                access_token=str(encrypted_access_token),
            )
        )
        logging.info('Login verified successfully')
        return jsonify(response_data), status.OK 

    
class TokenCheckAPI(MethodView):
    def get(self):
        payload = request.environ['payload']
        user = User.query.filter_by(email=payload.get('sub')).first()
        if not user:
            logging.error('user not found')
            return jsonify('User Not Found'), status.BAD_REQUEST
        logging.info('verified successfully')
        return jsonify('User verified successfully'), status.OK


class GetAccessTokenAPI(MethodView):
    def get(self):
        try:
            refresh_token = request.args['token']
            payload = decode_token(refresh_token)
            user = User.query.filter_by(email=payload.get('sub')).first()
            if not user:
                logging.error('user not found')
                return jsonify('User Not found'), status.BAD_REQUEST
            access_token = create_access_token(identity=user.id)
            encrypted_access_token = fernet.encrypt(access_token.encode())
            response_data = {
                'statusCode': 200,
                'status': "success",
                'message': "Access Token Generated Successfully",
                'token': {
                    'access': str(encrypted_access_token)
                    }
                }
            logging.info('Access token generated successfully')
            return jsonify(response_data), status.OK
        except ExpiredSignatureError as e:
            logging.warning(f'Exception -> {str(e)}')
            return jsonify('Refresh Token Expired'), status.FORBIDDEN
