

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


app = Flask(__name__)
app.config['SECRET_KEY'] = 'asdf121312jasdfsdf1212'
# location of database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
# create db instance
db = SQLAlchemy(app)
# create bcrypt instance
bcrypt = Bcrypt(app)
# create LoginManager instance
login_manager = LoginManager(app)
# url /account - required login if not redirect to log in page
login_manager.login_view = 'login'
# warning design if not login
login_manager.login_message_category = 'info'

from blog import routes
