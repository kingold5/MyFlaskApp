# pylint: disable=missing-docstring,too-few-public-methods,invalid-name,line-too-long,wrong-import-order
import os


class Config():
    # Config MySQL and secret key
    SECRET_KEY = os.environ.get('SECRET_KEY', 'secret_my_flask_key')

    # Use utf8mb4
    SQLALCHEMY_DATABASE_URI = 'mysql://root:5515660@localhost/myflaskapp?charset=utf8mb4'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
