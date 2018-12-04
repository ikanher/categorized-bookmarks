from flask_login import current_user

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

    @staticmethod
    def get_bookmarks_in_categories(categories):
        # collect user's bookmarks that are in all wanted categories
        bookmarks = []
        for bookmark in current_user.bookmarks:
            is_in_all_categories = True

            # loop through selected categories and check that bookmark is there
            for category in categories:
                if bookmark not in category.bookmarks:
                    is_in_all_categories = False
                    break

            if is_in_all_categories:
                bookmarks.append(bookmark)

        return bookmarks

