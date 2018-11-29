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
