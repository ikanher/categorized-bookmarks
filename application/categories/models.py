from flask_login import current_user
from sqlalchemy import func, and_

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

    def bookmark_count(self):
        # changed temporarily to bring ttapio love and happiness

        #count = db.session.query(func.count(Category.id))\
        #        .join(categorybookmark)\
        #        .filter(Category.id == self.id)\
        #        .group_by(Category.id)\
        #        .scalar()

        #return count or 0

        sql = """
SELECT COUNT(Category.id)
FROM Category
JOIN CategoryBookmark ON Category.id = CategoryBookmark.category_id
WHERE Category.id = :category_id
GROUP BY Category.id
        """

        stmt = text(sql).params(category_id=self.id)
        resultProxy = db.engine.execute(stmt)
        rows = resultProxy.fetchone()

        if not rows:
            return 0

        return rows[0]

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
    def exists(name):
        exists = db.session.query(Category.query\
                .filter(and_(
                    Category.user_id == current_user.id,
                    Category.name == name)
                ).exists()).scalar()

        return exists
