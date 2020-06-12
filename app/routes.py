from flask import Flask
from flask import render_template
from flask import request, redirect
from app.models import Post
from app import app
from app.form import LoginForm, RegistrationForm
from flask import flash, url_for
from flask_login import current_user, login_user
from app.models import User
from flask_login import logout_user, login_required
from werkzeug.urls import url_parse
from app import db
from flask import Markup

@app.route("/submit")
def submit_link():
    return  render_template("form.html")

# @app.route("/submit", methods=['GET','POST'])
# def submit_link():
#     link = request.form['url']
#     get_news(link)
#     return  redirect('/')

@app.route("/")
def index():
    return  render_template("index.html")

@app.route("/post")
@login_required
def all_post():
    posts = Post.query.all()
    return  render_template("post.html", posts = posts)

@app.route("/post/<int:post_id>")
def specific_post(post_id):
    this_post = Post.query.filter_by(id=post_id).first()
    return  render_template("thispost.html", post = this_post)

@app.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(user_name=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form = form)
    
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(first_name=form.firstname.data, last_name=form.lastname.data, user_name=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulation, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('reg.html', title='Register', form=form)

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(user_name=username).first_or_404()
    posts = [
        {'author' : user, 'body' : 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', user=user, posts=posts)