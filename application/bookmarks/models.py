from flask_login import current_user
from sqlalchemy import func, text, or_, and_
from sqlalchemy.sql import text

from application import db
from application.models import Base, categorybookmark
from application.categories.models import categoryinheritance

class Bookmark(Base):
    link = db.Column(db.String(2000), nullable=False, index=True)
    text = db.Column(db.String(2000), index=True)
    description = db.Column(db.String(2000), index=True)
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
    def get_user_bookmarks(user_id, sort_by=None, sort_direction=None):
        bookmarks = db.session().query(Bookmark)\
                .filter(Bookmark.user_id == user_id)

        sort_field = Bookmark.get_sort_field(sort_by, sort_direction)
        bookmarks = bookmarks.order_by(sort_field)

        return bookmarks

    @staticmethod
    def get_sort_field(sort_by, sort_direction):
        if sort_by:
            sort_field = Bookmark.__table__.c[sort_by]
        else:
            sort_field = Bookmark.text

        if sort_direction == 'desc':
            sort_field = sort_field.desc()
        else:
            sort_field = sort_field.asc()

        return sort_field

    @staticmethod
    def get_bookmarks_in_categories_with_children(category, sort_by=None, sort_direction=None):
        # fetch bookmarks that belong to all these categories

        # get the ids of child categories recursively
        category_ids = Bookmark.get_child_category_ids(category.id)

        # add id of the root category
        category_ids.append(category.id)

        # query for bookmark ids in these categories
        query = db.session.query(categorybookmark.c.bookmark_id)\
                .filter(categorybookmark.c.category_id.in_(category_ids))

        # now we have the query for the bookmark ids,
        # let's use those to load the bookmark objects
        bookmarks = db.session.query(Bookmark)\
                .filter(Bookmark.id.in_(query))

        # sorting
        sort_field = Bookmark.get_sort_field(sort_by, sort_direction)
        bookmarks = bookmarks.order_by(sort_field)

        return bookmarks

    @staticmethod
    def get_bookmarks_in_categories(categories, sort_by=None, sort_direction=None):

        # build aliases to be used in building multiple joins for
        # the same table to ensure that the, in fact, the bookmarks
        # belong to _all_ the categories. NB: IN() query does not work
        # here because it is "category1 OR category2 OR ..." and we
        # really want "category1 AND category 2 AND ..."
        category_aliases = { f'cb{i}': c.id for i, c in enumerate(categories) }

        # fetch bookmarks that belong to all these categkories
        sql = "SELECT b.id FROM bookmark b"

        for alias, category_id in category_aliases.items():
            sql += f" JOIN categorybookmark {alias} ON b.id = {alias}.bookmark_id and {alias}.category_id = :{alias}"

        stmt = text(sql).params(**category_aliases)

        # fetch results
        res = db.engine.execute(stmt)

        # and collect values
        bookmark_ids = []
        for row in res:
            bookmark_ids.append(row[0])

        # now we have the query for the bookmark ids,
        # let's use those to load the bookmark objects
        bookmarks = db.session.query(Bookmark)\
                .filter(Bookmark.id.in_(bookmark_ids))

        # sorting
        sort_field = Bookmark.get_sort_field(sort_by, sort_direction)
        bookmarks = bookmarks.order_by(sort_field)

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
    def get_uncategorized_bookmarks(sort_by=None, sort_direction=None):
        # subquery for ids of uncategorized bookmarks
        bookmark_ids = db.session().query(categorybookmark.c.bookmark_id)

        # query for bookmarks that do not belong to a category
        bookmarks = db.session().query(Bookmark)\
                .filter(Bookmark.user_id == current_user.id)\
                .filter(Bookmark.id.notin_(bookmark_ids))\

        sort_field = Bookmark.get_sort_field(sort_by, sort_direction)
        bookmarks = bookmarks.order_by(sort_field)

        return bookmarks

    @staticmethod
    def search(search_string, sort_by=None, sort_direction=None):
        # wildcard search
        search_string = func.lower('%' + search_string + '%')

        # query bookmarks by link, text and description
        bookmarks = db.session.query(Bookmark).filter(
                and_(
                    Bookmark.user_id == current_user.id,
                    or_(
                        func.lower(Bookmark.link).like(search_string),
                        func.lower(Bookmark.text).like(search_string),
                        func.lower(Bookmark.description).like(search_string))))

        sort_field = Bookmark.get_sort_field(sort_by, sort_direction)
        bookmarks = bookmarks.order_by(sort_field)

        return bookmarks

    @staticmethod
    def get_sort_fields():
        fields = []
        fields.append(('text', 'Link text'))
        fields.append(('date_modified', 'Modification time'))
        fields.append(('link', 'Link URL'))

        return fields

    @staticmethod
    def get_sort_directions():
        return [('asc', 'Ascending'), ('desc', 'Descending')];

    @staticmethod
    def exists(link, text):
        exists = db.session.query(Bookmark.query\
                .filter(and_(
                    Bookmark.user_id == current_user.id,
                    or_(Bookmark.link == link, Bookmark.text == text))
                ).exists()).scalar()

        return exists
