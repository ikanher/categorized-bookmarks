from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, validators

class CategoryForm(FlaskForm):
    name = StringField('Category name', [validators.DataRequired(), validators.Length(max=200)])
    description = TextAreaField('Category description', [validators.Optional(), validators.Length(max=500)])
    save = SubmitField('Save')
