from flask import Flask, jsonify
from flask import render_template
from flask import request, redirect
from app.models import Fiction, Chapter, Quote, Author
from app import app
from app.form import LoginForm, RegistrationForm, Quiz_answer
from flask import flash, url_for
from flask_login import current_user, login_user
from app.models import User
from flask_login import logout_user, login_required
from werkzeug.urls import url_parse
from app import db
from flask import Markup
from database import view_all_post

@app.route("/")
def index():
    return  render_template("space.html")

@app.route("/post")
def all_post():
    fiction = Fiction.query.all()
    return  render_template("post.html", fiction = fiction)

@app.route("/post/<int:fiction_id>/")
def specific_post(fiction_id):
    fiction = Fiction.query.filter_by(id=fiction_id).first()
    chapter = Chapter.query.filter_by(fiction=fiction_id).first()
    quote = Quote.query.filter_by(fiction=fiction_id)
    return  render_template("viewer.html", post = fiction, chapter = chapter, quote = quote)

@app.route("/<int:fiction_id>/<int:chapter_id>")
def chapter_viewer(chapter_id, fiction_id):
    chapter_view = Chapter.query.filter_by(id=chapter_id).first()
    fiction = Fiction.query.filter_by(id=fiction_id).first()
    current = chapter_view.chapter_order
    
    return render_template('chapter.html', post = chapter_view, fiction=fiction)

@app.route("/api/<int:fiction_id>/", methods = ['GET'])
def api_send_fiction(fiction_id):
    fiction = Fiction.query.filter_by(id=fiction_id).first()
    chapter = Chapter.query.filter_by(fiction=fiction_id) 
    api_return = {
        "id" : fiction.id,
        "name" : fiction.name,
        "author": fiction.author,
        "status": fiction.status,
        "totalview": fiction.view,
        "detail": fiction.desc,
        "coverpage": fiction.cover,
        "publishyear": fiction.publish_year,
        "page": fiction.page_count
    }
    return api_return
    

@app.route("/api/<int:fiction_id>/<int:chapter_order>", methods = ['GET'])
def api_send_chapter_content(chapter_order, fiction_id):
    chapter = Chapter.query.filter_by(fiction=fiction_id, chapter_order=chapter_order).first()
    return {
        "order":chapter.chapter_order,
        "name" : chapter.name,
        "content": chapter.content
    }

@app.route("/api/chapter_list_by_fiction/<int:fiction_id>", methods = ['GET'])
def api_send_chapter_list(fiction_id):
    chapter = Chapter.query.filter_by(fiction=fiction_id)
    newdict ={}
    for c in chapter:
       newdict[c.id] = c.name
    return newdict

@app.route("/quote/<int:quote_id>", methods = ['GET'])
def get_quote(quote_id):
    quote = Quote.query.filter_by(id=quote_id).first()
    author = Author.query.filter_by(id=quote.author_id).first()
    fiction = Fiction.query.filter_by(id=quote.fiction).first()
    return render_template("quote.html", quote = quote, author = author, fiction = fiction)

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


