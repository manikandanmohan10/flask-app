from flask import Flask, jsonify
from flask_migrate import Migrate
from src.database import db
from src.auth.bp import APIBlueprint
from flask_swagger import swagger 
from src.auth.views import RegisterAPI
from src.database.auth_reg_model import User
from flask_jwt_extended.jwt_manager import JWTManager
from src.middleware import SimpleMiddleWare


class APIBlueprintRegister(Flask):
    def __init__(self):
        super(APIBlueprintRegister, self).__init__(__name__)
        self.register_blueprint(APIBlueprint())

def create_app(test_config=None):
    app = Flask(__name__,
                instance_relative_config=True
            )
    swag = swagger(app)
    app = APIBlueprintRegister()
    JWTManager(app)
    
    if test_config is None:
        app.config.from_mapping(
           SECRET_KEY='dev',
           SQLALCHEMY_DATABASE_URI='postgresql://postgres:postgres@localhost/flask_test_db',
           SQLALCHEMY_TRACK_MODIFICATIONS=False,
        )  
    else:
        app.config.from_mapping(test_config)
    # app.wsgi_app = MiddlewareManager(app)
    # app.add_middleware(SimpleMiddleWare)
    app.wsgi_app = SimpleMiddleWare(app.wsgi_app)
    Migrate(app, db)
    db.init_app(app)
    with app.app_context():
        db.create_all()

    return app