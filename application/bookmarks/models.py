from flask_login import current_user
from sqlalchemy import func, or_, or_, or_, or_

from application import db
from application.models import Base, categorybookmark
from application.categories.models import categoryinheritance

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

        # subquery for child categories for all wanted categories
        child_category_ids = db.session().query(categoryinheritance.c.child_id)\
                .filter(categoryinheritance.c.parent_id.in_(category_ids))\

        # query for bookmarks in these categories and subcategories
        bookmarks = db.session().query(Bookmark)\
                .filter(Bookmark.user_id == current_user.id)\
                .join(categorybookmark)\
                .filter(or_(categorybookmark.c.category_id.in_(category_ids), categorybookmark.c.category_id.in_(child_category_ids)))\
                .group_by(Bookmark.id)\
                .having(func.count(Bookmark.id) >= len(categories))

        return bookmarks

    @staticmethod
    def get_uncategorized_bookmarks():
        # subquery for ids of uncategorized bookmarks
        bookmark_ids = db.session().query(categorybookmark.c.bookmark_id)

        # query for bookmarks that do not belong to a category
        bookmarks = db.session().query(Bookmark)\
                .filter(Bookmark.user_id == current_user.id)\
                .filter(Bookmark.id.notin_(bookmark_ids))\
                .all()

        return bookmarks
