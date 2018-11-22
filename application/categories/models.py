from application import db
from application.models import Base, categorybookmark
from application.bookmarks.models import Bookmark

class Category(Base):
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(500))
    bookmarks = db.relationship('Bookmark', backref='category', lazy='dynamic')
    user_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)

    bookmarks = db.relationship(
        'Bookmark',
        secondary=categorybookmark,
        back_populates='categories')

    def __init__(self, name, description, user_id):
        self.name = name
        self.description = description
        self.user_id = user_id
