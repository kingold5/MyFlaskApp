# pylint: disable=missing-docstring,too-few-public-methods,invalid-name,line-too-long,wrong-import-order
import datetime
from passlib.hash import sha256_crypt
from hashlib import md5
from flask_login import UserMixin
from myflask import db, login


# Followers association table
followers = db.Table(
    'followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('users.id'))
)

class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.VARCHAR(100), nullable=True)
    gender = db.Column(db.Enum('male', 'female', 'other'))
    birthday = db.Column(db.Date)
    email = db.Column(db.VARCHAR(100), unique=True, nullable=False)
    username = db.Column(db.VARCHAR(30), unique=True, nullable=False)
    status = db.Column(db.String(30), nullable=True)
    about_me = db.Column(db.String(140), nullable=True)
    password = db.Column(db.VARCHAR(128), nullable=True)
    last_seen = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    # Set followers
    followed = db.relationship('Users', secondary=followers,
                               primaryjoin=(followers.c.follower_id == id),
                               secondaryjoin=(followers.c.followed_id == id),
                               backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')
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
        return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}'

    def follow(self, user):
        """If not following, follow the user

        user : Class Users
            user candidiate to be followed
        """
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        """If followed, unfollow the user

        Parameters
        ----------
        user : Class Users
            user candidate to be unfollowed
        """
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        """Check if following the user

        Parameters
        ----------
        user : Class Users

        Returns
        -------
        boolean
            True : user is followed
            False : user is not followed
        """
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0

    def followed_articles(self):
        followed = Articles.query.join(
            followers, (followers.c.followed_id == Articles.uid)).filter(
                followers.c.follower_id == self.id)
        own = Articles.query.filter_by(uid=self.id)
        return followed.union(own).order_by(Articles.create_date.desc())


class Articles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.VARCHAR(191), nullable=True)
    uid = db.Column(db.Integer, db.ForeignKey('users.id'))
    body = db.Column(db.Text, nullable=True)
    create_date = db.Column(db.TIMESTAMP, nullable=False, default=datetime.datetime.utcnow)

    def __repr__(self):
        return '<Title %r>' % self.title


@login.user_loader
def load_user(id):
    return Users.query.get(int(id))
