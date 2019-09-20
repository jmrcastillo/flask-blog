

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SECRET_KEY'] = 'asdf121312jasdfsdf1212'
# location of database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
# create db instance
db = SQLAlchemy(app)

from blog import routes
