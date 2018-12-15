import os
from os import urandom

class Config():
    if os.environ.get('HEROKU'):
        SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    else:
        SQLALCHEMY_DATABASE_URI = 'sqlite:///bookmarks.db'
        SQLALCHEMY_ECHO = True

    SECRET_KEY = urandom(32)

    BOOKMARKS_PER_PAGE = 100
