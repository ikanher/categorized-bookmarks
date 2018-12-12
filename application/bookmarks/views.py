from application import app, db, login_manager
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from application.bookmarks.models import Bookmark
from application.bookmarks.forms import (
        BookmarkForm,
        BookmarkCategoryForm,
        SelectCategoriesForm,
        SelectCategoriesFormWithSort,
        SearchForm,
        SortableForm)

@app.route('/bookmarks/', methods=['GET', 'POST'])
@login_required
def bookmarks_list():
    if request.method == 'GET':
        if request.args.get('uncategorized'):
            # list only uncategorized bookmarks, no category selection
            return render_template('bookmarks/list.html',
                    bookmarks=Bookmark.get_uncategorized_bookmarks(),
                    uncategorized=1,
                    form=SortableForm())
        else:
            # show all bookmarks
            return render_template('bookmarks/list.html',
                    bookmarks=Bookmark.get_user_bookmarks(current_user.id),
                    form=SelectCategoriesFormWithSort())

    # list only uncategorized bookmarks if requested so
    if request.args.get('uncategorized'):
        form = SortableForm(request.form)
        sort_by = form.sort_by.data
        sort_direction = form.sort_direction.data

        bookmarks = Bookmark.get_uncategorized_bookmarks(sort_by, sort_direction)
        return render_template('bookmarks/list.html',
                uncategorized=1,
                bookmarks=bookmarks,
                form=form)

    # show only bookmarks in selected categories
    form = SelectCategoriesFormWithSort(request.form)
    sort_by = form.sort_by.data
    sort_direction = form.sort_direction.data

    categories = form.categories.data

    if not categories:
        # show all user's bookmarks
        bookmarks = Bookmark.get_user_bookmarks(current_user.id, sort_by, sort_direction)
    else:
        # collect user's bookmarks that are in all selected categories
        bookmarks = Bookmark.get_bookmarks_in_categories(categories, sort_by, sort_direction)

    return render_template('bookmarks/list.html',
            uncategorized=request.args.get('uncategorized'),
            bookmarks=bookmarks,
            form=form)

@app.route('/bookmarks/create', methods=['GET', 'POST'])
@login_required
def bookmarks_create():
    if request.method == 'GET':
        return render_template('bookmarks/create.html', form=BookmarkForm())

    form = BookmarkForm(request.form)

    if form.validate_on_submit():

        if Bookmark.exists(form.link.data, form.text.data):
            flash('Bookmark already exists, please try again.', 'alert-danger')
            return render_template('bookmarks/create.html', form=form)

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

    return redirect(url_for('bookmarks_list'))


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

@app.route('/bookmarks/search', methods=['GET', 'POST'])
@login_required
def bookmarks_search():
    if request.method == 'GET':
        return render_template('bookmarks/search.html', form=SearchForm())

    form = SearchForm(request.form)
    sort_by = form.sort_by.data
    sort_direction = form.sort_direction.data

    if form.validate_on_submit():
        keywords = form.search_field.data
        bookmarks = Bookmark.search(keywords, sort_by, sort_direction)
        return render_template('bookmarks/search.html', form=form, bookmarks=bookmarks)

    return render_template('bookmarks/search.html', form=form)
