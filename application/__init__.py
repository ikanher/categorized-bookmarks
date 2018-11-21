import os
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
bcrypt = Bcrypt(app)
csrf = CSRFProtect(app)

from flask_sqlalchemy import SQLAlchemy

# SQLAlchemy configuration, is this the best place?
if os.environ.get("HEROKU"):
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///discgolfstats.db'
    app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

from application import views
from application.courses import models, views

from application.auth import models
from application.auth import views

# login handler
from application.auth.models import User
from os import urandom
app.config["SECRET_KEY"] = urandom(32)

from flask_login import LoginManager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth_login'
login_manager.login_message = 'Please login to use this functionality'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

db.create_all()
