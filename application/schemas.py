from flask_marshmallow import Marshmallow

from application import app
from application.categories.models import Category
from application.bookmarks.models import Bookmark

ma = Marshmallow(app)

class CategorySchema(ma.ModelSchema):
    class Meta:
        model = Category

class BookmarkSchema(ma.ModelSchema):
    class Meta:
        model = Bookmark

