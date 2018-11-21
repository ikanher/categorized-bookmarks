from application import app, db
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required

from application.categories.models import Category
from application.categories.forms import CategoryForm

@app.route('/categories/', methods=['GET'])
@login_required
def categories_list():
    return render_template('categories/list.html', categories=Category.query.all())

@app.route('/categories/view/<int:id>', methods=['GET'])
@login_required
def categories_view(id):
    c = Category.query.get(id)
    return render_template('categories/view.html', category=c)

@app.route('/categories/create', methods=['GET', 'POST'])
@login_required
def categories_create():
    if request.method == 'GET':
        return render_template('categories/create.html', form=CategoryForm())

    form = CategoryForm(request.form)

    if form.validate_on_submit():
        c = Category(form.name.data, form.description.data)

        db.session().add(c)
        db.session().commit()

        flash("Category %s created" % c.name)

        return redirect(url_for("categories_list"))

    return render_template("categories/create.html", form=form)

@app.route('/categories/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def categories_edit(id):
    if request.method == 'GET':
        c = Category.query.get(id)
        form = CategoryForm(obj=c)
        return render_template('categories/edit.html', form=form, category_id=id)

    form = CategoryForm(request.form)

    if form.validate_on_submit():
        c = Category.query.get(id)
        c.name = form.name.data
        c.description = form.description.data
        db.session.commit()

        flash("Category %s saved" % c.name)

        return redirect(url_for("categories_list"))

    return render_template("categories/edit.html", form=form)

@app.route('/categories/delete/<int:id>', methods=['GET'])
@login_required
def categories_delete(id):
    c = Category.query.get(id)
    db.session().delete(c)
    db.session().commit()

    flash("Deleted category: %s" % c.name)

    return redirect(url_for("categories_list"))

@app.route('/categories/add_bookmark/<int:category_id>', methods=['GET', 'POST'])
@login_required
def categories_add_bookmark(category_id):
    pass

