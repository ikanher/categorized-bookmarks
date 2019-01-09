from application import app, db, login_manager
from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from flask_paginate import Pagination, get_page_parameter

from application.categories.models import Category
from application.bookmarks.models import Bookmark
from application.schemas import BookmarkSchema
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

    # pagination parameters
    page = request.args.get(get_page_parameter(), type=int, default=1)

    # sort parameters
    sort_by = request.args.get('sort_by')
    sort_direction = request.args.get('sort_direction')

    if request.args.get('uncategorized'):
        # list only uncategorized bookmarks, no category selection
        bookmarks = Bookmark.get_uncategorized_bookmarks(sort_by, sort_direction)

        # create form and fill it with data from request
        form = SortableForm()
        form.sort_by.data = sort_by
        form.sort_direction.data = sort_direction

        # pagination
        pagination = get_pagination(page, bookmarks)

        if request.args.get('json'):
            bookmarks_schema = BookmarkSchema(many=True)
            output = bookmarks_schema.dump(bookmarks.all()).data
            return jsonify({'bookmarks': output})
        else:
            return render_template('bookmarks/list.html',
                    pagination=pagination,
                    bookmarks=bookmarks,
                    uncategorized=1,
                    form=form)

    if request.args.get('categories'):
        # get category ids from query string and fetch categories
        category_ids = request.args.getlist('categories')
        categories = Category.query.filter(Category.id.in_(category_ids))

        # create form and fill it with data from request
        form = SelectCategoriesFormWithSort()
        form.sort_by.data = sort_by
        form.sort_direction.data = sort_direction
        form.categories.data = categories

        # collect user's bookmarks that are in all selected categories
        bookmarks = Bookmark.get_bookmarks_in_categories(categories, sort_by, sort_direction)

        # paging
        pagination = get_pagination(page, bookmarks)

        if request.args.get('json'):
            bookmarks_schema = BookmarkSchema(many=True)
            output = bookmarks_schema.dump(bookmarks.all()).data
            return jsonify({'bookmarks': output})
        else:
            return render_template('bookmarks/list.html',
                    pagination=pagination,
                    uncategorized=request.args.get('uncategorized'),
                    bookmarks=bookmarks,
                    form=form)
    else:
        # show all bookmarks
        bookmarks = Bookmark.get_user_bookmarks(current_user.id, sort_by, sort_direction)

        form = SelectCategoriesFormWithSort()
        form.sort_by.data = sort_by
        form.sort_direction.data = sort_direction

        pagination = get_pagination(page, bookmarks)

        if request.args.get('json'):
            bookmarks_schema = BookmarkSchema(many=True)
            output = bookmarks_schema.dump(bookmarks.all()).data
            return jsonify({'bookmarks': output})
        else:
            return render_template('bookmarks/list.html',
                    pagination=pagination,
                    bookmarks=bookmarks.paginate(page, app.config['BOOKMARKS_PER_PAGE'], False).items,
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

    # pagination parameters
    page = request.args.get(get_page_parameter(), type=int, default=1)

    form = SearchForm(request.form)
    sort_by = form.sort_by.data
    sort_direction = form.sort_direction.data

    if form.validate_on_submit():
        search_string = form.search_field.data
        bookmarks = Bookmark.search(search_string, sort_by, sort_direction)
        pagination = get_pagination(page, bookmarks, search=True)

        return render_template('bookmarks/search.html',
                pagination=pagination,
                form=form,
                bookmarks=bookmarks)

    return render_template('bookmarks/search.html', form=form)

def get_pagination(page, bookmarks, search=False):
    pagination = Pagination(
            page=page,
            per_page=app.config['BOOKMARKS_PER_PAGE'],
            search=search,
            total=bookmarks.count(),
            found=bookmarks.count(),
            css_framework='bootstrap4',
            link_size=1,
            record_name='bookmarks')

    return pagination

