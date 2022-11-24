# from flask_serialize import FlaskSerialize
# from src.models import db

# fs_mixin = FlaskSerialize(db)

# class RegisterSerializer(db.Model, fs_mixin):
#     username = db.Column(db.String(200))
#     password = db.Column(db.String(255))
#     email = db.Column(db.Text())

from marshmallow import fields, Schema, validate 

class RegisterSerializer(Schema):
    username = fields.Str(validate=validate.Length(min=1), required=True)
    password = fields.Str(required=True)
    email = fields.Email(required=True, error_messages={"required": "Email is required."})

class LoginSerializer(Schema):
    email = fields.Str(required=True)
    password = fields.Str(required=True)