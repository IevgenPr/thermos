import os

from logging import DEBUG

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_moment import Moment

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.logger.setLevel(DEBUG)
app.config["SECRET_KEY"] = b'\xd1\xaa\x13t\x87A\xbd\xfd\xddh\xbdyC\xa4\xc0\xfd\xc5HR\xe3VGM\xff'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///' + os.path.join(basedir, "db", "thermos.db")
app.config['DEBUG'] = True
db = SQLAlchemy(app)

# Configure authentication
login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = "login"
login_manager.init_app(app)

# display timestamps
moment = Moment(app)

from . import models
from . import views
