from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, validators
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from application.categories.models import Category

class BookmarkForm(FlaskForm):
    link = StringField('Link', [validators.Length(min=4, max=2000), validators.URL()])
    text = StringField('Text', [validators.Length(max=2000), validators.Optional()])
    description = TextAreaField('Description', [validators.Length(max=2000), validators.Optional()])
    save = SubmitField('Save')

class BookmarkCategoryForm(FlaskForm):
    category = QuerySelectField(
            query_factory=lambda: Category.query.all(),
            get_label=lambda c: c.name,
            validators=[validators.DataRequired()])
    add = SubmitField('Add')
