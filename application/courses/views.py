from application import app, db
from flask import render_template, request, redirect, url_for
from flask_login import login_required

from application.courses.models import Course
from application.courses.forms import CourseForm

@app.route('/courses/', methods=['GET'])
def courses_list():
    return render_template('courses/list.html', courses=Course.query.all())

@app.route('/courses/create')
@login_required
def courses_form():
    return render_template('courses/create.html', form=CourseForm())

@app.route('/courses/', methods=['POST'])
@login_required
def courses_create():
    form = CourseForm(request.form)
    c = Course(form.name.data)

    db.session().add(c)
    db.session().commit()

    return redirect(url_for("courses_list"))

@app.route('/courses/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def courses_edit(id):
    if request.method == 'GET':
        c = Course.query.get(id)
        form = CourseForm(obj=c)
        form.id = id
        return render_template('courses/edit.html', form=form)

    form = CourseForm(request.form)
    c = Course.query.get(id)
    c.name = form.name.data
    db.session.commit()

    return redirect(url_for("courses_list"))
