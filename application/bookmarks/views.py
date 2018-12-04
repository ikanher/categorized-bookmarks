from application import app, db, login_manager
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from application.bookmarks.models import Bookmark
from application.bookmarks.forms import BookmarkForm, BookmarkCategoryForm, SelectCategoriesForm

@app.route('/bookmarks/', methods=['GET', 'POST'])
@login_required
def bookmarks_list():
    # show all bookmarks
    if request.method == 'GET':
        return render_template('bookmarks/list.html',
                bookmarks=current_user.bookmarks,
                form=SelectCategoriesForm())

    # show only bookmarks in selected categories
    if request.method == 'POST':
        form = SelectCategoriesForm(request.form)
        categories = form.categories.data

        if not categories:
            # show all user's bookmarks
            bookmarks = current_user.bookmarks
        else:
            # collect user's bookmarks that are in all selected categories
            bookmarks = Bookmark.get_bookmarks_in_categories(categories)

        return render_template('bookmarks/list.html', bookmarks=bookmarks, form=form)

@app.route('/bookmarks/create', methods=['GET', 'POST'])
@login_required
def bookmarks_create():
    if request.method == 'GET':
        return render_template('bookmarks/create.html', form=BookmarkForm())

    form = BookmarkForm(request.form)

    if form.validate_on_submit():
        b = Bookmark(form.link.data, form.text.data, form.description.data, current_user.id)
        b.categories = form.categories.data

        db.session().add(b)
        db.session().commit()

        flash('Bookmark %s created' % b.text, 'alert-success')

        return redirect(url_for('bookmarks_list'))

    return render_template('bookmarks/create.html', form=form)

@app.route('/bookmarks/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def bookmarks_edit(id):
    b = Bookmark.query.get(id)
    if not b in current_user.bookmarks:
        return login_manager.unauthorized()

    if request.method == 'GET':
        form = BookmarkForm(obj=b)
        return render_template('bookmarks/edit.html', form=form, bookmark_id=id)

    form = BookmarkForm(request.form)

    if form.validate_on_submit():
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

    if not b in current_user.bookmarks:
        return login_manager.unauthorized()

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

        if not b in current_user.bookmarks:
            return login_manager.unauthorized()

        bookmark.categories = form.categories.data
        db.session().commit()

    return redirect(url_for('bookmarks_list'))
