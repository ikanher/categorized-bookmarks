from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from application import app, db, role_required
from application.auth.models import User, Role

@app.route('/users/', methods=['GET'])
@login_required
@role_required('admin')
def users_list():
    return render_template('users/list.html', users=User.query.all())

@app.route('/users/delete/<int:id>', methods=['GET'])
@login_required
@role_required('admin')
def users_delete(id):
    u = User.query.get(id)

    db.session().delete(u)
    db.session().commit()

    flash('Deleted user: %s (%s)' % (u.username, u.name), 'alert-success')

    return redirect(url_for('users_list'))

