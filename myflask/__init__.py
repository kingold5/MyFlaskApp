# pylint: disable=missing-docstring,too-few-public-methods,invalid-name,line-too-long,wrong-import-order
from flask import Flask, logging
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config


app = Flask(__name__)

# Config
app.config.from_object(Config)

# Init SQLAlchemy & migrate
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Init login
login = LoginManager(app)
login.login_view = 'login'

# Create log handle
log = logging.create_logger(app)

from myflask import forms, routes
