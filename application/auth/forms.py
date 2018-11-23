from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, validators

class LoginForm(FlaskForm):
    username = StringField('Username', [validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired()])
    login = SubmitField('Let me in!')

class RegisterForm(FlaskForm):
    fullname = StringField('Full name',
            [validators.DataRequired(), validators.Length(min=3, max=200)])
    username = StringField('Username',
            [validators.DataRequired(), validators.Length(min=3, max=200)])
    password_confirm = PasswordField('Confirm password',
            [validators.DataRequired(), validators.Length(min=6)])
    password = PasswordField('Password', [
        validators.Length(min=6),
        validators.DataRequired(),
        validators.EqualTo('password_confirm', message='Passwords do not match')
    ])

    register = SubmitField('Register')
