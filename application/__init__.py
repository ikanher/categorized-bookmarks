from flask import Flask
app = Flask(__name__)

from flask_sqlalchemy import SQLAlchemy

# SQLAlchemy configuration, is this the best place?
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///discgolfstats.db"
app.config["SQLALCHEMY_ECHO"] = True

db = SQLAlchemy(app)

from application import views
from application.courses import models, views

db.create_all()
