from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from application import app, db, role_required
from application.auth.models import User, Role

@app.route('/users/', methods=['GET'])
@login_required
@role_required('admin')
def users_list():
    return render_template('users/list.html', users=User.query.all())

