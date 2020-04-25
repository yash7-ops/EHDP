from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import data_required, input_required, Email



class Loginf(FlaskForm):
    uname = StringField("Username", validators= [input_required()])
    pwd = PasswordField("Password", validators= [input_required()])
    remember = BooleanField("remember me")
    submit = SubmitField("Submit")

class Reginf(FlaskForm):
    uname = StringField("Username", validators= [input_required()])
    email = StringField("Email", validators=[input_required(), Email(message="Invalid EMail")])
    pwd = PasswordField("Password", validators= [input_required()])
    submit = SubmitField("Submit")
