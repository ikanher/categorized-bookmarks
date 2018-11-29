from application import app,db
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required

from application.bookmarks.models import Bookmark
from application.bookmarks.forms import BookmarkForm, BookmarkCategoryForm

@app.route('/bookmarks/', methods=['GET'])
@login_required
def bookmarks_list():
    return render_template('bookmarks/list.html', bookmarks=Bookmark.query.all())

@app.route('/bookmarks/create', methods=['GET', 'POST'])
@login_required
def bookmarks_create():
    if request.method == 'GET':
        return render_template('bookmarks/create.html', form=BookmarkForm())

    form = BookmarkForm(request.form)

    if form.validate_on_submit():
        b = Bookmark(form.link.data, form.text.data, form.description.data)
        b.categories = form.categories.data

        db.session().add(b)
        db.session().commit()

        flash('Bookmark %s created' % b.text, 'alert-success')

        return redirect(url_for('bookmarks_list'))

    return render_template('bookmarks/create.html', form=form)

@app.route('/bookmarks/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def bookmarks_edit(id):
    if request.method == 'GET':
        b = Bookmark.query.get(id)
        form = BookmarkForm(obj=b)
        return render_template('bookmarks/edit.html', form=form, bookmark_id=id)

    form = BookmarkForm(request.form)

    if form.validate_on_submit():
        b = Bookmark.query.get(id)
        b.link = form.link.data
        b.text = form.text.data
        b.description = form.description.data
        b.categories = form.categories.data
        db.session.commit()

        flash('Bookmark "%s" saved' % b.text, 'alert-success')

        return redirect(url_for('bookmarks_list'))

    return render_template('bookmarks/edit.html', form=form)


@app.route('/bookmarks/delete/<int:id>', methods=['GET'])
@login_required
def bookmarks_delete(id):
    b = Bookmark.query.get(id)
    db.session().delete(b)
    db.session().commit()

    flash('Deleted bookmark: %s' % b.text, 'alert-success')

    return redirect(url_for('bookmarks_list'))

@app.route('/bookmarks/<int:bookmark_id>/add_category', methods=['POST'])
@login_required
def bookmarks_add_category(bookmark_id):
    form = BookmarkCategoryForm(request.form)

    if form.validate_on_submit():
        bookmark = Bookmark.query.get(bookmark_id)
        bookmark.categories = form.categories.data
        db.session().commit()

    return redirect(url_for('bookmarks_list'))
