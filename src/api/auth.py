import os
from flask import jsonify, request, Response
from flask.views import MethodView
from psycopg2 import IntegrityError
from src.database.auth_reg_model import User
from src.database import db
from http import HTTPStatus as status
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import create_access_token, create_refresh_token
from flask_jwt_extended import decode_token
from src.service.mail_service import send_mail
from src.config import get_fernet_key
import threading    



class RegisterAPI(MethodView):
    def post(self):
        try:
            fernet = get_fernet_key()
            data = request.json
            username = data.get("username")
            password = data.get("password")
            email = data.get("email")
            if len(password) < 6:
                return Response("Password length is too short"), status.BAD_REQUEST
            encrypted_password = fernet.encrypt(password.encode())
            user = User(username=username, password=str(encrypted_password), email=email)
            db.session.add(user)
            db.session.commit()
            response_data = dict(message='User Created Successfully',
                                status= 'success',
                                statusCode= status.CREATED
                                )
            return jsonify(response_data), 201
        except IntegrityError as e:
            response_data = dict(message='Email Already Exists',
                                status= 'failure',
                                statusCode= 400
                                )
            return jsonify(response_data), status.BAD_REQUEST
        except Exception as e:
            return jsonify(str(e)), status.BAD_REQUEST



class LoginAPI(MethodView):
    def post(self):
        try:
            fernet = get_fernet_key()
            data = request.json
            email = data.get('email')
            password = data.get('password')
            user = User.query.filter_by(email=email).first()
            passwd = eval(user.password)
            if fernet.decrypt(passwd).decode() == password:
                mail_content = dict(
                    subject='Logged In',
                    text='You just logged in'
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
                    user_id = str(encrypted_user_id),
                    email=str(encrypted_email),
                    token=dict(
                        refresh_token=str(encrypted_refresh_token),
                        access_token=str(encrypted_access_token),
                    )
                )
                return jsonify(response_data), status.OK
            else:
                return jsonify("Email and password are not matching"), status.BAD_REQUEST
        except Exception as e:
            return jsonify(str(e)), status.BAD_REQUEST

    
class TokenCheckAPI(MethodView):
    def get(self):
        payload = request.environ['payload']
        user = User.query.filter_by(email=payload.get('sub')).first()
        if user:
            return jsonify('User verified successfully'), status.OK
        else:
            return jsonify('User Not Found'), status.BAD_REQUEST


class GetAccessTokenAPI(MethodView):
    def get(self):
        try:
            refresh_token = request.args['token']
            payload = decode_token(refresh_token)
            user = User.query.filter_by(email=payload.get('sub')).first()
            if user:
                access_token = create_access_token(identity=user.email)
                response_data = {
                    'statusCode': 200,
                    'status': "success",
                    'message': "Access Token Generated Successfully",
                    'token': {
                        'access': access_token
                        }
                    }
                return jsonify(response_data), status.OK
            else:
                return jsonify('User Not found'), status.BAD_REQUEST

        except Exception as e:
            return jsonify(str(e)), status.BAD_REQUEST
