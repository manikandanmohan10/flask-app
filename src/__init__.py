import os
import logging
from datetime import timedelta
from flask import Flask, jsonify
from flask_migrate import Migrate
from src.database import db
# from src.blueprint import blueprints
from flask_swagger import swagger 
# from src.api.auth import RegisterAPI
from src.database.auth_reg_model import User
from src.database.quote_model import Quote
from flask_jwt_extended.jwt_manager import JWTManager
from src.config.middleware import CustomMiddleWare
from celery import Celery
from flask import Flask
from sentry_sdk.integrations.flask import FlaskIntegration
# from raven.contrib.flask import Sentry
# sentry = Sentry(
#     dsn=os.getenv('SENTRY_URL')
#     )
postgres_username = os.getenv('POSTGRES_USER')
postgres_password = os.getenv('POSTGRES_PASSWORD')

debug_mode = True if os.getenv('DEBUG_MODE') == '1' else False

if debug_mode:
    logging.basicConfig(level=logging.DEBUG)


# class APIBlueprintRegister(Flask):
#     def __init__(self):
#         super(APIBlueprintRegister, self).__init__(__name__)
#         for bp in blueprints:
#             self.register_blueprint(bp())

#     class ContextTask(celery.Task):
#         def __call__(self, *args, **kwargs):
#             with app.app_context():
#                 return self.run(*args, **kwargs)

#     celery.Task = ContextTask
#     return celery

def create_app(test_config=None):
    # sentry_sdk.init(
    # dsn=os.getenv('SENTRY_URL'), integrations=[FlaskIntegration()]
    # )
    app = Flask(__name__,
                instance_relative_config=True
                )
    swag = swagger(app)
    # app = APIBlueprintRegister()
    JWTManager(app)
    # celery = make_celery(app)
    # sentry.init_app(app)
    if test_config is None:
        app.config.from_mapping(
           SECRET_KEY='dev',
           SQLALCHEMY_DATABASE_URI=f'postgresql://{postgres_username}:{postgres_password}@localhost/flask_test_db',
           SQLALCHEMY_TRACK_MODIFICATIONS=False,
           JWT_SECRET_KEY='secret',
           CELERY_BROKER_URL='redis://localhost:6379/0',
           CELERY_RESULT_BACKEND='redis://localhost:6379/0',
           JWT_ACCESS_TOKEN_EXPIRES=timedelta(hours=1),
           JWT_REFRESH_TOKEN_EXPIRES=timedelta(hours=5)
        )  
    else:
        app.config.from_mapping(test_config)
    # app.wsgi_app = MiddlewareManager(app)
    # app.add_middleware(SimpleMiddleWare)

    # celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
    # celery.conf.update(app.config)

    # for bp in blueprints:
    #     app.register_blueprint(bp)
    
    app.wsgi_app = CustomMiddleWare(app.wsgi_app)
    Migrate(app, db)
    db.init_app(app)
    with app.app_context():
        db.create_all()

    return app


# @app.errorhandler(InternalServerError)
# def process_exception(app, exception):
#     a = 10
#     return app

# # @app.after_request
# # def process_exception(response):
# #     a = 10
# #     return response

# if __name__ == '__main__':
#     app.run('0.0.0.0', '5000', debug=debug_mode)

# def get_celery():
#     return celery