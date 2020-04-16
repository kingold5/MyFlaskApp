# pylint: disable=missing-docstring,too-few-public-methods,invalid-name,line-too-long,wrong-import-order
import datetime
from passlib.hash import sha256_crypt
from hashlib import md5
from flask_login import UserMixin
from myflask import db, login


class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.VARCHAR(100), nullable=True)
    gender = db.Column(db.Enum('male', 'female', 'other'))
    birthday = db.Column(db.Date)
    email = db.Column(db.VARCHAR(100), unique=True, nullable=True)
    username = db.Column(db.VARCHAR(30), unique=True, nullable=True)
    password = db.Column(db.VARCHAR(128), nullable=True)
    articles = db.relationship('Articles', backref='author', lazy='dynamic')
    register_date = db.Column(db.TIMESTAMP, nullable=False, default=datetime.datetime.utcnow)

    def __repr__(self):
        return '<User %r>' % self.username

    def set_password(self, password_str):
        self.password = sha256_crypt.encrypt(password_str)

    def check_password(self, password_candidate):
        return sha256_crypt.verify(password_candidate, self.password)

    def avatar(self, size=80):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)

class Articles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.VARCHAR(255), nullable=True)
    uid = db.Column(db.Integer, db.ForeignKey('users.id'))
    body = db.Column(db.Text, nullable=True)
    create_date = db.Column(db.TIMESTAMP, nullable=False, default=datetime.datetime.utcnow)

    def __repr__(self):
        return '<Title %r>' % self.title


@login.user_loader
def load_user(id):
    return Users.query.get(int(id))
