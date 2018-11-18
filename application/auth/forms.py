from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, validators

class LoginForm(FlaskForm):
    username = StringField('Username', [validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired()])

    class Meta:
        csrf = False

class RegisterForm(FlaskForm):
    fullname = StringField('Full name',
            [validators.DataRequired(), validators.Length(min=3, max=200)])
    username = StringField('Username',
            [validators.DataRequired(), validators.Length(min=3, max=200)])
    password = PasswordField('Password',
            [validators.DataRequired(), validators.Length(min=8)])
    password_confirm = PasswordField('Confirm password',
            [validators.DataRequired(), validators.Length(min=8)])

    class Meta:
        csrf = False
