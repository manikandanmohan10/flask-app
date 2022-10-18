# from abc import ABC
#
# class FileConfig(ABC):
#     def __init__(self):
#         super(FileConfig, self).__init__()
import os
from datetime import timedelta
postgres_username = os.getenv('POSTGRES_USER')
postgres_password = os.getenv('POSTGRES_PASSWORD')


def create_app_config(app):
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI=f'postgresql://{postgres_username}:{postgres_password}@localhost/flask_test_db',
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        JWT_SECRET_KEY='secret',
        JWT_ACCESS_TOKEN_EXPIRES=timedelta(hours=1),
        JWT_REFRESH_TOKEN_EXPIRES=timedelta(hours=5)
    )
