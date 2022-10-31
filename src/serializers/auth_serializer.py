from flask_serialize import FlaskSerialize
from src.models import db

fs_mixin = FlaskSerialize(db)

class RegisterSerializer(db.Model, fs_mixin):
    username = db.Column(db.String(200))
    password = db.Column(db.String(255))
    email = db.Column(db.Text())