from flask import request, jsonify
from functools import wraps
import jwt
from src.database.auth_reg_model import User
import src 


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        app = src.create_app()
        token = None
        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']

        if not token:
            return jsonify({'message': 'a valid token is missing'})
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = User.query.filter_by(public_id=data['public_id']).first()
        except:
            return jsonify({'message': 'token is invalid'})

        return f(current_user, *args, **kwargs)
    return decorator