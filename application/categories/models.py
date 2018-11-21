from application import db
from application.models import Base

class Course(Base):
    name = db.Column(db.String(200), nullable=False)
    location = db.Column(db.String(200), nullable=False)

    def __init__(self, name, location):
        self.name = name
        self.location = location
