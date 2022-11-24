import wtforms
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from flask.views import MethodView
from flask import render_template, Response, request
from http import HTTPStatus as status


class MyForm(FlaskForm):
    username = wtforms.StringField("username", validators=[DataRequired()])
    password = wtforms.PasswordField("password", validators=[DataRequired()])
    submit = wtforms.SubmitField("submit")
    
    
class WTFFormAPI(MethodView):
    def get(self):
        form = MyForm() 
        return render_template('wtf.html', form=form)
    
    def post(self):
        uname = request.form.get('username')
        password = request.form.get('password')
        
        return Response(f'<h3> Hi {uname}, Your password is {password}<h3>'), status.OK