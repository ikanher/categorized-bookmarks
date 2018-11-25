from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user

from application import app, db, bcrypt
from application.auth.models import User
from application.auth.forms import LoginForm, RegisterForm

@app.route('/auth/login', methods=['GET', 'POST'])
def auth_login():
    if request.method == 'GET':
        return render_template('auth/login_form.html', form=LoginForm())

    form = LoginForm(request.form)

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user is None or not bcrypt.check_password_hash(user.password, form.password.data):
            flash('Invalid username or password', 'alert-danger')
            return render_template('auth/login_form.html', form=form)

        login_user(user)

        flash('Successful login! Welcome %s' % user.name, 'alert-success')

        return redirect(url_for('index'))

    return render_template('auth/login_form.html', form=form)

@app.route('/auth/register', methods=['GET', 'POST'])
def auth_register():
    if request.method == 'GET':
        return render_template('auth/register_form.html', form=RegisterForm())

    form = RegisterForm(request.form)

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            flash('Username exists, choose another one', 'alert-warning')
            return render_template('auth/register_form.html', form=form)

        pw_hash = bcrypt.generate_password_hash(form.password.data)
        new_user = User(form.fullname.data, form.username.data, pw_hash)
        db.session().add(new_user)
        db.session().commit()

        flash('Registration complete. Please log in using your brand new account!', 'alert-success')

        return redirect(url_for('auth_login'))

    return render_template('auth/register_form.html', form=form)

@app.route('/auth/logout')
def auth_logout():
    logout_user()
    flash('Logged out', 'alert-success')
    return redirect(url_for('index'))
