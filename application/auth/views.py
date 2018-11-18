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
    if not form.validate():
        return render_template("auth/login_form.html", form=form)

    user = User.query.filter_by(username=form.username.data).first()
    if not user:
        return render_template('auth/login_form.html', form=form, error='No such username or password')

    if not bcrypt.check_password_hash(user.password, form.password.data):
        return render_template('auth/login_form.html', form=form, error='No such username or password')

    login_user(user)

    flash('Successful login! Welcome %s' % user.name)

    return redirect(url_for('index'))

@app.route('/auth/register', methods=['GET', 'POST'])
def auth_register():
    if request.method == 'GET':
        return render_template('auth/register_form.html', form=RegisterForm())

    form = RegisterForm(request.form)
    if not form.validate():
        return render_template("auth/register_form.html", form=form)

    user = User.query.filter_by(username=form.username.data).first()
    if user:
        return render_template('auth/register_form.html', form=form, error='Username exists, choose another username')

    if form.password.data != form.password_confirm.data:
        return render_template('auth/register_form.html', form=form, error='Passwords do not match')

    pw_hash = bcrypt.generate_password_hash(form.password.data)
    new_user = User(form.fullname.data, form.username.data, pw_hash)
    db.session().add(new_user)
    db.session().commit()

    flash('Registration complete. Please log in using your brand new account!')

    return redirect(url_for('auth_login'))

@app.route('/auth/logout')
def auth_logout():
    logout_user()
    flash('Logged out')
    return redirect(url_for('index'))
