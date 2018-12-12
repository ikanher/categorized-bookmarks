from application import db
from application.models import Base

userrole = db.Table('accountrole',
    db.Column('account_id', db.Integer, db.ForeignKey('account.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'))
)

class User(Base):

    __tablename__ = 'account'

    name = db.Column(db.String(200), nullable=False)
    username = db.Column(db.String(200), nullable=False)
    password = db.Column(db.Binary(60), nullable=False)

    # relations
    categories = db.relationship('Category',
            cascade='all,delete', backref='user',
            order_by="asc(Category.name)",
            lazy=True)

    bookmarks = db.relationship('Bookmark',
            cascade='all,delete',
            order_by="asc(Bookmark.text)",
            backref='user',
            lazy=True)
    roles = db.relationship('Role', secondary=userrole)

    # flask-login
    is_active = True
    is_anonymous = False
    is_authenticated = True

    def __init__(self, name, username, password):
        self.name = name
        self.username = username
        self.password = password

    # flask-login
    def get_id(self):
        return self.id

    def has_role(self, role):
        for r in self.roles:
            if r.name == role:
                return True

        return False

    def is_admin(self):
        return self.has_role('admin')

    def category_count(self):
        return len(self.categories)

    def bookmark_count(self):
        return len(self.bookmarks)

class Role(db.Model):

    __tablename__ = 'role'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)

    def __init__(self, name):
        self.name = name
