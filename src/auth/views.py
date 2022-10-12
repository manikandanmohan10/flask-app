from flask import jsonify, request, Response
from flask.views import MethodView
from psycopg2 import IntegrityError
from werkzeug.security import check_password_hash, generate_password_hash
from src.database.auth_reg_model import User
from src.database import db
from http import HTTPStatus
from sqlalchemy.exc import IntegrityError
from jwt.api_jwt import PyJWT
from src.auth.utils import token_required
from flask_jwt_extended import create_access_token, create_refresh_token
from flask_jwt_extended.tokens import _decode_jwt
from flask_jwt_extended import get_current_user,JWTManager
from jwt import decode
JWTManager.decode_key_loader


class RegisterAPI(MethodView):
    def post(self):
        try:
            data = request.json
            username = data.get("username")
            password = data.get("password")
            email = data.get("email")
            if len(password) < 6:
                return Response("Password length is too short"), HTTPStatus.BAD_REQUEST
            pw_hash = generate_password_hash(password)
            user = User(user_name=username, password=pw_hash, email=email)
            db.session.add(user)
            db.session.commit()
            response_data = dict(message='User Created Successfully',
                                status= 'success',
                                statusCode= HTTPStatus.CREATED
                                )
            return jsonify(response_data), 201
        except IntegrityError as e:
            response_data = dict(message='Email Already Exists',
                                status= 'failure',
                                statusCode= 400
                                )
            return jsonify(response_data), HTTPStatus.BAD_REQUEST
        except Exception as e:
            return jsonify(str(e)), HTTPStatus.BAD_REQUEST



class LoginAPI(MethodView):
    def post(self):
        try:
            data = request.json
            email = data.get('email')
            password = data.get('password')
            pw_hash = User.query.get(email).password
            if check_password_hash(pw_hash, password):
                refresh_token = create_refresh_token(identity=email)
                access_token = create_access_token(identity=email)
                response_data = dict(
                    message = 'Login verfied successfully',
                    status = 'success',
                    statusCode = 200,
                    token = dict(
                        reaccess_token=refresh_token,
                        access_token=access_token,
                    )
                )
                return jsonify(response_data), HTTPStatus.OK
            else:
                return jsonify("Email and password are not matching"), HTTPStatus.BAD_REQUEST
        except Exception as e:
            pass