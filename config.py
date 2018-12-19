import os
from os import urandom

class Config():
    SECRET_KEY = urandom(32)
    BOOKMARKS_PER_PAGE = 100

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///bookmarks.db'
    SQLALCHEMY_ECHO = True
