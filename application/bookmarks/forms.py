from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, TextAreaField, SubmitField, validators
from wtforms.ext.sqlalchemy.fields import QuerySelectMultipleField, QuerySelectField

from application.categories.models import Category

class BookmarkBaseForm(FlaskForm):
    category = QuerySelectField(
            query_factory=lambda: current_user.categories,
            get_label=lambda c: c.name,
            validators=[validators.DataRequired()])

class BookmarkForm(BookmarkBaseForm):
    link = StringField('Link', [validators.URL()])
    text = StringField('Text', [validators.Length(max=2000), validators.Optional()])
    description = TextAreaField('Description', [validators.Length(max=2000), validators.Optional()])
    save = SubmitField('Save')

class BookmarkCategoryForm(BookmarkBaseForm):
    add = SubmitField('Add')
