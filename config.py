# pylint: disable=missing-docstring,too-few-public-methods,invalid-name,line-too-long,wrong-import-order
class Config():
    # Config MySQL and secret key
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = '5515660'
    MYSQL_DB = 'myflaskapp'
    MYSQL_CURSORCLASS = 'DictCursor'
    SECRET_KEY = 'secret_my_flask_key'

    SQLALCHEMY_DATABASE_URI = 'mysql://root:5515660@localhost/myflaskapp'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
