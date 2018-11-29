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
    categories = db.relationship('Category', backref='user', lazy=True)

    roles = db.relationship('Role', secondary=userrole)

    def __init__(self, name, username, password):
        self.name = name
        self.username = username
        self.password = password

    def get_id(self):
        return self.id

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True

    def has_role(self, role):
        for r in self.roles:
            if r.name == role:
                return True

        return False

    def is_admin(self):
        return self.has_role('admin')

    def category_count(self):
        return len(self.categories)

class Role(db.Model):

    __tablename__ = 'role'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)

    def __init__(self, name):
        self.name = name
