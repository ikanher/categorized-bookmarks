from sqlalchemy import func

from application import db
from application.models import Base, categorybookmark

categoryinheritance = db.Table('categoryinheritance',
    db.Column('parent_id', db.Integer, db.ForeignKey('category.id'), primary_key=True),
    db.Column('child_id', db.Integer, db.ForeignKey('category.id'), primary_key=True)
)

class Category(Base):
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(500))
    bookmarks = db.relationship('Bookmark', backref='category', lazy='dynamic')
    user_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)

    bookmarks = db.relationship(
        'Bookmark',
        secondary=categorybookmark,
        back_populates='categories')

    children = db.relationship(
        'Category',
        secondary=categoryinheritance,
        primaryjoin='Category.id==categoryinheritance.c.parent_id',
        secondaryjoin='Category.id==categoryinheritance.c.child_id',
        backref='parents')

    def __init__(self, name, description, user_id):
        self.name = name
        self.description = description
        self.user_id = user_id

    def bookmark_count(self):
        count = db.session.query(func.count(Category.id))\
                .join(categorybookmark)\
                .filter(Category.id == self.id)\
                .group_by(Category.id)\
                .scalar()

        return count or 0

    def subcategory_count(self):
        count = db.session.query(func.count(Category.id))\
                .join(categoryinheritance, Category.id==categoryinheritance.c.parent_id)\
                .filter(Category.id == self.id)\
                .scalar()

        return count or 0
