from flask_login import current_user
from sqlalchemy import func, or_, text
from sqlalchemy.sql import text

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
        # collect ids from categories
        category_ids = [c.id for c in categories]

        # load all child category ids
        child_category_ids = Bookmark.get_child_categories(category_ids);

        # append them for querying all categories
        category_ids.extend(child_category_ids)

        # query for bookmarks in these categories and subcategories
        bookmarks = db.session().query(Bookmark)\
                .filter(Bookmark.user_id == current_user.id)\
                .join(categorybookmark)\
                .filter(categorybookmark.c.category_id.in_(category_ids))\
                .group_by(Bookmark.id)\
                .having(func.count(Bookmark.id) >= len(categories))\
                .all()

        return bookmarks

    @staticmethod
    def get_child_categories(category_ids):
        sql = """
WITH RECURSIVE children (parent_id, child_id) AS (
    SELECT parent_id, child_id
    FROM categoryinheritance WHERE parent_id IN (__PLACEHOLDER__)
UNION
    SELECT ci.parent_id, ci.child_id
    FROM categoryinheritance ci
    JOIN children c ON ci.parent_id = c.child_id
)
SELECT child_id FROM children
        """

        # create string to hold placeholder names for SQL
        placeholder_str = ', '.join([':p'+str(i) for i in range(len(category_ids))])

        # replace the placeholder placeholder in SQL with actual placeholder
        sql = sql.replace('__PLACEHOLDER__', placeholder_str)

        # map params to their values
        params = {k: v for (k, v) in [('p'+str(i), category_ids[i]) for i in range(len(category_ids))]}

        # now we are ready to execute the sql
        stmt = text(sql).params(**params)

        # done, fetch result
        res = db.engine.execute(stmt)

        # and collect values
        child_ids = []
        for row in res:
            child_ids.append(row[0])

        return child_ids


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
