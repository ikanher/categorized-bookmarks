from flask_wtf import FlaskForm
from wtforms import StringField

class CourseForm(FlaskForm):
    name = StringField("Course name")

    class Meta:
        csrf = False
