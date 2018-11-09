from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user

from application import app, db
from application.auth.models import User
from application.auth.forms import LoginForm, RegisterForm

@app.route('/auth/login', methods=['GET', 'POST'])
def auth_login():
    if request.method == 'GET':
        return render_template('auth/login_form.html', form=LoginForm())

    form = LoginForm(request.form)

    user = User.query.filter_by(username=form.username.data, password=form.password.data).first()
    if not user:
        return render_template('auth/login_form.html', form=form, error='No such username or password')

    login_user(user)
    return redirect(url_for('index'))

@app.route('/auth/register', methods=['GET', 'POST'])
def auth_register():
    if request.method == 'GET':
        return render_template('auth/register_form.html', form=RegisterForm())

    form = RegisterForm(request.form)

    user = User.query.filter_by(username=form.username.data).first()
    if user:
        return render_template('auth/register_form.html', form=form, error='Username exists, choose another username')

    if form.password.data != form.password_confirm.data:
        return render_template('auth/register_form.html', form=form, error='Passwords do not match')

    new_user = User(form.fullname.data, form.username.data, form.password.data)
    db.session().add(new_user)
    db.session().commit()

    return redirect(url_for('auth_login'))

@app.route("/auth/logout")
def auth_logout():
    logout_user()
    return redirect(url_for('index'))
