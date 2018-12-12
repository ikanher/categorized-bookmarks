from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, TextAreaField, SubmitField, SelectField, validators
from wtforms.ext.sqlalchemy.fields import QuerySelectMultipleField

from application.categories.models import Category
from application.bookmarks.models import Bookmark

class SortableForm(FlaskForm):
    sort_by = SelectField(
            'Sort by',
            [validators.AnyOf(list(map(lambda by: by[0], Bookmark.get_sort_fields())))],
            choices=Bookmark.get_sort_fields())

    sort_direction = SelectField(
            'Sort direction',
            [validators.AnyOf(list(map(lambda dir: dir[0], Bookmark.get_sort_directions())))],
            choices=Bookmark.get_sort_directions())

class SearchForm(SortableForm):
    search_field = StringField('Search', [validators.DataRequired()])
    search = SubmitField('Search')

class SelectCategoriesFormWithSort(SortableForm):
    categories = QuerySelectMultipleField(
            query_factory=lambda: current_user.categories,
            get_label=lambda c: c.name,
            validators=[validators.NumberRange()])

class SelectCategoriesForm(FlaskForm):
    categories = QuerySelectMultipleField(
            query_factory=lambda: current_user.categories,
            get_label=lambda c: c.name,
            validators=[validators.NumberRange()])

class BookmarkForm(SelectCategoriesForm):
    link = StringField('Link', [validators.URL(), validators.DataRequired()])
    text = StringField('Text', [validators.Length(max=2000), validators.DataRequired()])
    description = TextAreaField('Description', [validators.Length(max=2000), validators.Optional()])
    save = SubmitField('Save')

class BookmarkCategoryForm(SelectCategoriesForm):
    add = SubmitField('Add')
