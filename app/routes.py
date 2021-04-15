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
    top_view_fictions = Fiction.query.order_by(Fiction.view.desc()).limit(10).all()
    top_authors = Author.query.order_by(Author.fiction_count.desc()).limit(10).all()
    
    return  render_template("home.html", top_view_fictions = top_view_fictions, top_authors=top_authors)

@app.route("/test")
def test():
    test_items = Author.query.all()
    return  jsonify(test_items)

@app.route("/author/<author_name>")
def author_page(author_name):
    author = Author.query.filter_by(name=author_name).first()
    fictions = Fiction.query.filter_by(author_id=author.id)
    return render_template("author.html", author = author, fictions =fictions)

@app.route("/authors/")
def all_authors():
    authors = Author.query.all()
    return render_template("authors.html", authors = authors)


@app.route("/fictions")
def fictions():
    fictions = Fiction.query.all()
    return  render_template("fictions.html", fictions = fictions)

@app.route("/fiction/<int:fiction_id>/")
def specific_post(fiction_id):
    fiction = Fiction.query.filter_by(id=fiction_id).first()
    author = Author.query.filter_by(id=fiction.author_id).first()
    chapter = Chapter.query.filter_by(fiction=fiction_id).first()

    chapters = Chapter.query.filter_by(fiction=fiction_id).limit(10)
    quote = Quote.query.filter_by(fiction=fiction_id)
    return  render_template("viewer.html", fiction = fiction, chapters = chapters, quote = quote, author =author, chapter=chapter)

@app.route("/fiction/<fiction_name>/")
def specific_fiction_name(fiction_name):
    fiction = Fiction.query.filter_by(name=fiction_name).first()
    author = Author.query.filter_by(id=fiction.author_id).first()
    chapters = Chapter.query.filter_by(fiction=fiction.id)
    quote = Quote.query.filter_by(fiction=fiction.id)
    return  render_template("viewer.html", fiction = fiction, chapters = chapters, quote = quote, author =author)


@app.route("/chapter/<int:chapter_id>/")
def chapter_viewer(chapter_id):
    chapter = Chapter.query.filter_by(id=chapter_id).first()
    chapter.update_view()
    fiction = Fiction.query.filter_by(id=chapter.fiction).first()
    chapters = Chapter.query.filter_by(fiction=fiction.id).limit(10)
    plus = chapter.chapter_order+1
    minus = chapter.chapter_order-1
    
    try:
        next_chapter = Chapter.query.filter_by(chapter_order=plus, fiction = fiction.id).first()
        nct = next_chapter.id
    except:
        nct = None
    
    try:
        previous_chapter = Chapter.query.filter_by(chapter_order=minus, fiction = fiction.id).first()
        pre = previous_chapter.id
    except:
        pre = None

    return render_template('chapter.html', chapter = chapter, fiction=fiction, chapters = chapters, next_chapter = nct, previous_chapter = pre)

@app.route("/api/<int:fiction_id>/", methods = ['GET'])
def api_send_fiction(fiction_id):
    fiction = Fiction.query.filter_by(id=fiction_id).first()
    chapter = Chapter.query.filter_by(fiction=fiction_id) 
    return jsonify(fiction)
    

@app.route("/api/<int:fiction_id>/<int:chapter_order>", methods = ['GET'])
def api_send_chapter_content(chapter_order, fiction_id):
    chapter = Chapter.query.filter_by(fiction=fiction_id, chapter_order=chapter_order).first()
    return jsonify(chapter)

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


