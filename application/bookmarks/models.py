from flask_login import current_user
from sqlalchemy import func

from application import db
from application.models import Base, categorybookmark

class Bookmark(Base):
    link = db.Column(db.String(2000), nullable=False)
    text = db.Column(db.String(2000))
    description = db.Column(db.String(2000))
    user_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)

    categories = db.relationship(
            'Category',
            secondary=categorybookmark,
            back_populates='bookmarks')

    def __init__(self, link, text, description, user_id):
        self.link = link
        self.text = text
        self.description = description
        self.user_id = user_id

    def category_count(self):
        count = db.session.query(func.count(Bookmark.id))\
                .join((categorybookmark, Bookmark.id == categorybookmark.c.bookmark_id))\
                .filter(Bookmark.id == self.id)\
                .scalar()

        return count or 0

    @staticmethod
    def get_bookmarks_in_categories(categories):
        category_ids = [c.id for c in categories]

        # query for bookmarks in these categories
        bookmarks = db.session().query(Bookmark)\
                .filter(Bookmark.user_id == current_user.id)\
                .join(categorybookmark)\
                .filter(categorybookmark.c.category_id.in_(category_ids))\
                .group_by(Bookmark.id)\
                .having(func.count(Bookmark.id) >= len(categories))

        return bookmarks
