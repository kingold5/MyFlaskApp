# pylint: disable=missing-docstring,too-few-public-methods,invalid-name,line-too-long,wrong-import-order
import datetime
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from myflask import app, log, db
from myflask.forms import UserDataForm, PasswordForm, RegisterForm, ArticleForm, ProfileForm
from myflask.models import Users, Articles


# Home
@app.route('/')
@app.route('/index')
def index():
    return render_template('home.html')

# About
@app.route('/about')
def about():
    return render_template('about.html')

# Last seen
@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.datetime.utcnow()
        db.session.commit()

# Articles
@app.route('/articles')
def all_articles():
    # Fetch articles from database
    articles = Articles.query.all()

    if articles is not None:
        return render_template('articles.html', articles=articles)
    else:
        msg = 'No articles found'
        return render_template('articles.html', msg=msg)

# Single article
@app.route('/article/<string:id>/')
def single_article(id):
    # Fetch one article from database
    article = Articles.query.get(int(id))

    if article is not None:
        return render_template('article.html', article=article)
    else:
        flash('No page found!', 'warning')
        return redirect(url_for('articles'))

# User register
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        # Create new user
        new_user = Users(name=form.name.data, birthday=form.birthday.data, gender=form.gender.data, username=form.username.data, email=form.email.data)
        new_user.set_password(str(form.password.data))

        # Commit to database
        db.session.add(new_user)
        db.session.commit()

        flash('You are now registered and can log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

# User login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password_candidate = request.form['password']

        user = Users.query.filter_by(username=username).first()

        if user is not None and user.check_password(password_candidate):
            # Username and password verified
            log.info('login successful')

            login_user(user)
            flash('You are now logged in', 'success')
            if request.form['next'] != '':
                # 'next' attribute exits
                return redirect(request.form['next'])
            else:
                return redirect(url_for('dashboard'))

        log.info('NO SUCH USERNAME!')
        error = 'Invalid username or password'
        return render_template('login.html', error=error)

    return render_template('login.html')

# Dashboard
@app.route('/dashboard')
@login_required
def dashboard():
    # Fetch all articles from login user
    articles = current_user.articles

    if articles is not None:
        return render_template('dashboard.html', articles=articles)
    else:
        return render_template('dashboard.html')

# User logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))

# Add article
@app.route('/add_article', methods=['GET', 'POST'])
@login_required
def add_article():
    form = ArticleForm(request.form)

    if request.method == 'POST' and form.validate():
        article = Articles(title=form.title.data, body=form.body.data, uid=current_user.id)
        db.session.add(article)
        db.session.commit()

        flash('Article is successfully submitted', 'success')
        return redirect('dashboard')
    return render_template('add_article.html', form=form)

# Edit article
@app.route('/edit_article/<string:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    form = ArticleForm(request.form)
    print('we are here agagin')
    article = Articles.query.get(int(id))

    if article is not None:
        # Article exits
        if request.method == 'POST' and form.validate():
            # Form validated. Write form into database
            article.title = form.title.data
            article.body = form.body.data

            db.session.commit()

            flash('Article updated!', 'success')
            return redirect(url_for('dashboard'))
        # Populate article form fileds
        form.title.data = article.title
        form.body.data = article.body
        return render_template('edit_article.html', form=form)
    else:
        # Article not found
        flash('Article (id = {}) not found'.format(id), 'warning')
        return redirect(url_for('dashboard'))

# Delete article
@app.route('/delete_article/<string:id>', methods=['POST'])
@login_required
def delete_article(id):
    article = Articles.query.get(int(id))

    db.session.delete(article)
    db.session.commit()

    flash('Article is deleted', 'success')
    return redirect(url_for('dashboard'))

# Forgot password
@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']

        user = Users.query.filter_by(username=username).first()
        if user is not None and email == user.email:
            # Identity verified

            log.info('Verification passed')
            flash('Verification passed', 'success')
            return redirect(url_for('reset_password', id=user.id))

        log.info('Identity verification failed')
        error = 'Username or email is wrong'
        return render_template('forgot_password.html', error=error)

    return render_template('forgot_password.html')

# Reset password
@app.route('/reset_password/<string:id>', methods=['GET', 'POST'])
def reset_password(id):
    form = PasswordForm(request.form)

    if request.method == 'POST' and form.validate():
        # Find user and reset password
        user_pass_reset = Users.query.filter_by(id=id).first()
        user_pass_reset.set_password(str(form.password.data))

        # Commit to database
        db.session.commit()

        flash('Password successfully reset', 'success')
        return redirect(url_for('login'))

    return render_template('reset_password.html', form=form)

# User settings
@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    userDataForm = UserDataForm(request.form)
    passwordForm = PasswordForm(request.form)

    userDataForm.name.data = current_user.name
    userDataForm.gender.data = current_user.gender
    userDataForm.birthday.data = current_user.birthday
    userDataForm.username.data = current_user.username
    userDataForm.email.data = current_user.email

    return render_template('settings.html', userDataForm=userDataForm, passwordForm=passwordForm)

# Reset password from settings
@app.route('/resetpassword', methods=['POST'])
@login_required
def resetpassword():
    passwordForm = PasswordForm(request.form)
    userDataForm = UserDataForm(request.form)

    userDataForm.name.data = current_user.name
    userDataForm.gender.data = current_user.gender
    userDataForm.birthday.data = current_user.birthday
    userDataForm.username.data = current_user.username
    userDataForm.email.data = current_user.email

    if passwordForm.validate():
        # Change password and commit to database
        current_user.set_password(str(passwordForm.password.data))
        db.session.commit()

        msg = 'Password successfully reset'
        return render_template('settings.html', msg=msg, userDataForm=userDataForm, passwordForm=passwordForm)

    error = 'Invalid password'
    return render_template('settings.html', error=error, userDataForm=userDataForm, passwordForm=passwordForm)

# Change user data
@app.route('/user_data', methods=['POST'])
@login_required
def user_data():
    userDataForm = UserDataForm(request.form)
    passwordForm = PasswordForm(request.form)

    if userDataForm.validate():
        # Change user data
        current_user.name = userDataForm.name.data
        current_user.gender = userDataForm.gender.data
        current_user.birthday = userDataForm.birthday.data
        current_user.email = userDataForm.email.data

        # Commit to database
        db.session.commit()
        msg = 'User data sumitted'
        return render_template('settings.html', msg=msg, userDataForm=userDataForm, passwordForm=passwordForm)

    userDataForm.name.data = current_user.name
    userDataForm.gender.data = current_user.gender
    userDataForm.birthday.data = current_user.birthday
    userDataForm.email.data = current_user.email

    error = 'Invalid user data'
    return render_template('settings.html', error=error, userDataForm=userDataForm, passwordForm=passwordForm)

# User profile display
@app.route('/user/<string:username>')
@login_required
def user_profile(username):
    user = Users.query.filter_by(username=username).first_or_404()

    return render_template('user_profile.html', user=user)

# Edit user/self profile
@app.route('/edit_profile', methods=['POST', 'GET'])
@login_required
def edit_profile():
    form = ProfileForm(request.form)

    if form.validate_on_submit():
        current_user.status = form.status.data
        current_user.about_me = form.about_me.data

        db.session.commit()
        flash('Your profile is updated!', 'success')
        return redirect(url_for('user_profile', username=current_user.username))

    form.status.data = current_user.status
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form)

# Follow users
@app.route('/follow/<string:username>', methods=['POST'])
@login_required
def follow(username):
    user = Users.query.filter_by(username=username).first_or_404()
    current_user.follow(user)
    db.session.commit()

    flash(f'You are following {username}!', 'success')
    return redirect(url_for('user_profile', username=username))

# Unfollow users
@app.route('/unfollow/<string:username>', methods=['POST'])
@login_required
def unfollow(username):
    user = Users.query.filter_by(username=username).first_or_404()
    current_user.unfollow(user)
    db.session.commit()

    flash(f'You have unfollowed {username}!', 'success')
    return redirect(url_for('user_profile', username=username))