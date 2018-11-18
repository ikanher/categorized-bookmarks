from flask_wtf import FlaskForm
from wtforms import StringField, validators

class CourseForm(FlaskForm):
    name = StringField("Course name", [validators.Length(min=3)])

    class Meta:
        csrf = False
