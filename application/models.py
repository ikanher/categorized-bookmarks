from application import db

categorybookmark = db.Table('categorybookmark',
    db.Column('category_id', db.Integer, db.ForeignKey('category.id')),
    db.Column('bookmark_id', db.Integer, db.ForeignKey('bookmark.id'))
)

class Base(db.Model):

    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())
