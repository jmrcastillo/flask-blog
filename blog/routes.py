

import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
# from form module
from blog.forms import RegistrationForm, LoginForm, UpdateAccountForm
# from models module
from blog.models import User, Post
from blog import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required

posts = [
    {
        'author': 'Jm Castillo',
        'title': 'Blog 1',
        'content': 'First Post Content',
        'date_posted': 'April 20, 2018'
    },
    {
        'author': 'Jm Castillo',
        'title': 'Blog 2',
        'content': 'Second Post Content',
        'date_posted': 'April 20, 2018'
    },
    {
        'author': 'Jm Castillo',
        'title': 'Blog 3',
        'content': 'Third Post Content',
        'date_posted': 'April 20, 2018'
    }

]


@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html", posts=posts)


@app.route("/about")
def about():
    return render_template("about.html", title="About")


@app.route("/register", methods=['GET', 'POST'])
def register():

    # if user is authenticated redirect to home
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RegistrationForm()
    if form.validate_on_submit():
        # decode('utf-8') - to make it string not byte
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data,
                    email=form.email.data,
                    password=hashed_password)
        # add and commit user
        db.session.add(user)
        db.session.commit()
        # flash for sending alert
        flash('Your account has been created! You are now able to login',
              'success')
        return redirect(url_for('login'))
    return render_template("register.html", title="Register", form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():

    # if user is authenticated redirect to home
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        # if user exists and password is valid in db let the user login
        if user and bcrypt.check_password_hash(user.password,
                                               form.password.data):
            login_user(user, remember=form.remember.data)
            # redirect to account page if user directly go to account
            # home if not
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password',
                  'danger')
    return render_template("login.html", title="Login", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _name, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/photos', picture_fn)
    # resize image using pillow
    output_size = (125, 125)
    i = Image.open((form_picture))
    i.thumbnail(output_size)
    # save picture
    i.save(picture_path)
    return picture_fn


# method arguments to allow to get and post
@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    # form to update account
    form = UpdateAccountForm()
    # form to update photo
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    # image location in static folder
    image_file = url_for('static', filename='photos/' + current_user.image_file)
    # render to account.html template, variable form, image_file
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)
