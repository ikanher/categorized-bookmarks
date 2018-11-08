from application import app, db
from flask import render_template, request
from application.courses.models import Course

@app.route('/courses/', methods=['GET'])
def courses_list():
    return render_template('courses/list.html', courses=Course.query.all())

@app.route('/courses/new')
def courses_form():
    return render_template('courses/new.html')

@app.route('/courses/', methods=['POST'])
def courses_create():
    c = Course(request.form.get('name'))

    db.session().add(c)
    db.session().commit()

    return redirect(url_for("courses_list"))
