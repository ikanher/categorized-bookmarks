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
        # fetch bookmarks that belong to all these categories

        # first build all required queries and collect them
        queries = []
        for c in categories:
            # get the ids of child categories recursively
            category_ids = Bookmark.get_child_category_ids(c.id)

            # add id of the root category
            category_ids.append(c.id)

            # query for bookmark ids in these categories
            query = db.session.query(categorybookmark.c.bookmark_id)\
                    .filter(categorybookmark.c.category_id.in_(category_ids))

            # collect query for the next step
            queries.append(query)

        # now intersect all the collected queries to find
        # bookmarks that belong in all of the wanted categories
        bookmark_ids = queries.pop()
        for q in queries:
            bookmark_ids = bookmark_ids.intersect(q)

        # now we have the query for the bookmark ids,
        # let's use those to load the bookmark objects
        bookmarks = db.session.query(Bookmark)\
                .filter(Bookmark.id.in_(bookmark_ids))\
                .all()

        return bookmarks

    @staticmethod
    def get_child_category_ids(category_id):
        sql = """
WITH RECURSIVE children (parent_id, child_id) AS (
    SELECT parent_id, child_id
    FROM categoryinheritance WHERE parent_id = :category_id
UNION
    SELECT ci.parent_id, ci.child_id
    FROM categoryinheritance ci
    JOIN children c ON ci.parent_id = c.child_id
)
SELECT child_id FROM children
        """

        stmt = text(sql).params(category_id=category_id)

        # fetch results
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

    @staticmethod
    def search(keywords):
        # wildcard search
        keywords = '%' + keywords + '%'

        # query bookmarks by link, text and description
        bookmarks = db.session.query(Bookmark).filter(or_(\
                Bookmark.link.like(keywords),\
                Bookmark.text.like(keywords),\
                Bookmark.description.like(keywords)))

        return bookmarks
