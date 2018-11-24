from sqlalchemy.sql import text

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

    def bookmark_count(self):
        stmt = text("SELECT COUNT(bookmark.id) FROM bookmark"
                + " JOIN categorybookmark ON bookmark.id = categorybookmark.bookmark_id"
                + " WHERE categorybookmark.category_id = :category_id"
                + " GROUP BY categorybookmark.category_id").params(category_id=self.id)

        res = db.engine.execute(stmt)
        row = res.fetchone()

        if row:
            return row[0]

        return 0

