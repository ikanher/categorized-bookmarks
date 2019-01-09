import os
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_wtf.csrf import CSRFProtect
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from functools import wraps

app = Flask(__name__)
if app.config['ENV'] == 'production':
    app.config.from_object('config.ProductionConfig')
else:
    app.config.from_object('config.DevelopmentConfig')

bcrypt = Bcrypt(app)
csrf = CSRFProtect(app)
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)

# login handler
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth_login'
login_manager.login_message = 'Please login to use this functionality'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

# role authorization decorator
def role_required(role_name):
    def decorator(func):
        @wraps(func)

        def authorize(*args, **kwargs):
            if not current_user.has_role(role_name):
                return login_manager.unauthorized();
            else:
                return func(*args, **kwargs)

        return authorize

    return decorator


from application import views
from application import schemas
from application.categories import models, views
from application.bookmarks import models, views
from application.users import views
from application.auth import models, views
from application.auth.models import User, Role

db.create_all()
