from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators

class CourseForm(FlaskForm):
    name = StringField('Course name', [validators.Length(min=3)])
    location = StringField('Course location', [validators.DataRequired(), validators.Length(max=200)])
    save = SubmitField('Save')
