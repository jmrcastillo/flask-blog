

from flask import render_template, url_for, flash, redirect
from blog.forms import RegistrationForm, LoginForm
from blog.models import User, Post
from blog import app

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
    form = RegistrationForm()
    if form.validate_on_submit():
        # flash for sending alert
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template("register.html", title="Register", form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have benn logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template("login.html", title="Login", form=form)

