from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, TextAreaField, SubmitField, validators
from wtforms.ext.sqlalchemy.fields import QuerySelectMultipleField

from application.categories.models import Category

class SelectCategoriesForm(FlaskForm):
    categories = QuerySelectMultipleField(
            query_factory=lambda: current_user.categories,
            get_label=lambda c: c.name,
            validators=[validators.NumberRange()])

class BookmarkForm(SelectCategoriesForm):
    link = StringField('Link', [validators.URL()])
    text = StringField('Text', [validators.Length(max=2000), validators.Optional()])
    description = TextAreaField('Description', [validators.Length(max=2000), validators.Optional()])
    save = SubmitField('Save')

class BookmarkCategoryForm(SelectCategoriesForm):
    add = SubmitField('Add')
