from flask import Blueprint, redirect, url_for, flash, render_template, current_app
from flask_login import current_user, login_user, logout_user, login_required

from blog import bcrypt, db
from blog.users.forms import RegistrationForm, LoginForm
from blog.models import User

users = Blueprint('users', __name__)


@users.route('/register', methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode(
            'utf-8')  # decode -> string instead of bites
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to login.', 'success')  # success is bootstrap class
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)


@users.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('main.home'))
            flash('You have been logged in!', 'success')  # success is bootstrap class
        else:
            flash('Login Unsuccessful. Check if your data is correct.',
                  'danger')  # danger is bootstrap class for visual rendering
    return render_template('login.html', title='Login', form=form)


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@users.route("/account")
@login_required
def account():
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file)
