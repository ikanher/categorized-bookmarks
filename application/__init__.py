import os
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_wtf.csrf import CSRFProtect
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

bcrypt = Bcrypt(app)
csrf = CSRFProtect(app)
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)

from application import views
from application.categories import models, views
from application.bookmarks import models, views
from application.auth import models
from application.auth import views
from application.auth.models import User

# login handler
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth_login'
login_manager.login_message = 'Please login to use this functionality'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

db.create_all()
