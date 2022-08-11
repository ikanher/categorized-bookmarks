from flask_login import current_user
from sqlalchemy import func, text, and_

from application import db
from application.models import Base, categorybookmark

categoryinheritance = db.Table('categoryinheritance',
    db.Column('parent_id', db.Integer, db.ForeignKey('category.id'), primary_key=True),
    db.Column('child_id', db.Integer, db.ForeignKey('category.id'), primary_key=True)
)

class Category(Base):
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(500))
    user_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)

    bookmarks = db.relationship(
        'Bookmark',
        order_by="asc(Bookmark.text)",
        secondary=categorybookmark,
        back_populates='categories')

    children = db.relationship(
        'Category',
        order_by="asc(Category.name)",
        secondary=categoryinheritance,
        primaryjoin='Category.id==categoryinheritance.c.parent_id',
        secondaryjoin='Category.id==categoryinheritance.c.child_id')

    parents = db.relationship(
        'Category',
        order_by="asc(Category.name)",
        secondary=categoryinheritance,
        primaryjoin='Category.id==categoryinheritance.c.child_id',
        secondaryjoin='Category.id==categoryinheritance.c.parent_id')

    def __init__(self, name, description, user_id):
        self.name = name
        self.description = description
        self.user_id = user_id

    def __str__(self):
        return f'<{self.id} ({self.name})>'

    def bookmark_count(self):
        count = db.session.query(func.count(Category.id))\
                .join(categorybookmark)\
                .filter(Category.id == self.id)\
                .group_by(Category.id)\
                .scalar()

        return count or 0

    def child_category_count(self):
        count = db.session.query(func.count(Category.id))\
                .join(categoryinheritance, Category.id==categoryinheritance.c.parent_id)\
                .filter(Category.id == self.id)\
                .scalar()

        return count or 0

    def parent_category_count(self):
        count = db.session.query(func.count(Category.id))\
                .join(categoryinheritance, Category.id==categoryinheritance.c.child_id)\
                .filter(Category.id == self.id)\
                .scalar()

        return count or 0

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
    def exists(name):
        exists = db.session.query(Category.query\
                .filter(and_(
                    Category.user_id == current_user.id,
                    Category.name == name)
                ).exists()).scalar()

        return exists
