# pylint: disable=missing-docstring,too-few-public-methods,invalid-name,line-too-long,wrong-import-order
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, SelectField, validators, SubmitField
from wtforms.fields.html5 import DateField
from flask_login import current_user
from myflask.models import Users


# User data class
class UserDataForm(FlaskForm):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    gender = SelectField('Gender', choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')])
    birthday = DateField('Birthday', format='%Y-%m-%d')
    username = StringField('Username', [validators.Length(min=2, max=25)], render_kw={'readonly':True})
    email = StringField('E-mail', [validators.Email()])

    def validate_email(self, field):
        user = Users.query.filter_by(email=field.data).first()

        # Found same email address
        if current_user.is_anonymous:
            # In register view
            if user is not None:
                raise validators.ValidationError(
                    'email exists! Please use another one!')
        elif user.id != current_user.id:
            raise validators.ValidationError(
                'email exists! Please use another one!')

# Password class
class PasswordForm(FlaskForm):
    password = PasswordField('Password', [validators.InputRequired(), validators.EqualTo('confirm', message="Password must match")])
    confirm = PasswordField('Confirm password')


# Register class
# username is ediable
class RegisterForm(UserDataForm, PasswordForm):
    username = StringField('Username', [validators.Length(min=2, max=25)])

    def validate_username(self, field):
        user = Users.query.filter_by(username=field.data).first()

        # Found same username
        if user is not None:
            raise validators.ValidationError(
                'username exists! Please use another one!')


# Article class
class ArticleForm(FlaskForm):
    title = StringField('Title', [validators.Length(min=1, max=191)])
    body = TextAreaField('Body', [validators.Length(min=30)])


class ProfileForm(FlaskForm):
    status = SelectField('Status', choices=[('', ''),
                                            ('😀', '😀'),
                                            ('😂', '😂'),
                                            ('🥰️', '🥰'),
                                            ('😎', '😎'),
                                            ('👿', '👿'),
                                            ('😢', '😢')], default='')
    about_me = StringField('About_me', [validators.Length(min=0, max=191)])
    submit = SubmitField('Submit')
