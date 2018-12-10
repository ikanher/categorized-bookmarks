from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, TextAreaField, SubmitField, validators
from wtforms.ext.sqlalchemy.fields import QuerySelectMultipleField

class CategoryForm(FlaskForm):
    name = StringField('Category name', [validators.DataRequired(), validators.Length(max=200)])
    description = TextAreaField('Category description', [validators.Optional(), validators.Length(max=500)])

    bookmarks = QuerySelectMultipleField(
            query_factory=lambda: current_user.bookmarks,
            get_label=lambda c: c.text,
            validators=[validators.NumberRange()])

    children = QuerySelectMultipleField(
            query_factory=lambda: current_user.categories,
            get_label=lambda c: c.name,
            label='Child categories',
            validators=[validators.NumberRange()])

    parents = QuerySelectMultipleField(
            query_factory=lambda: current_user.categories,
            get_label=lambda c: c.name,
            label='Parent categories',
            validators=[validators.NumberRange()])

    save = SubmitField('Save')
