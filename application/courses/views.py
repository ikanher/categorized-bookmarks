from application import app, db
from flask import render_template, request, redirect, url_for, flash
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

@app.route('/courses/view/<int:id>', methods=['GET'])
def courses_view(id):
    c = Course.query.get(id)
    return render_template('courses/view.html', course=c)

@app.route('/courses/create', methods=['POST'])
@login_required
def courses_create():
    form = CourseForm(request.form)

    if not form.validate():
        return render_template("courses/create.html", form=form)

    c = Course(form.name.data)

    db.session().add(c)
    db.session().commit()

    flash("Course %s created" % c.name)

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
    form.id = id
    if not form.validate():
        return render_template("courses/edit.html", form=form)

    c = Course.query.get(id)
    c.name = form.name.data
    db.session.commit()

    flash("Course %s saved" % c.name)

    return redirect(url_for("courses_list"))

@app.route('/courses/delete/<int:id>', methods=['GET'])
@login_required
def courses_delete(id):
    c = Course.query.get(id)
    db.session().delete(c)
    db.session().commit()

    flash("Deleted course: %s" % c.name)

    return redirect(url_for("courses_list"))

