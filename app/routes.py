from flask import Flask, jsonify
from flask import render_template
from flask import request, redirect
from app.models import Fiction, Chapter, Quote, Author
from app import app
from app.form import LoginForm, RegistrationForm, Quiz_answer, AuthorForm, FictionForm, ChapterForm
from flask import flash, url_for, send_file
from flask_login import current_user, login_user
from app.models import User
from flask_login import logout_user, login_required
from werkzeug.urls import url_parse
from app import db
from flask import Markup
from database import view_all_post
import json
from werkzeug.datastructures import ImmutableMultiDict
from img_crop import return_img

@app.route("/")
def index():
    top_view_fictions = Fiction.query.order_by(Fiction.view.desc()).limit(12).all()
    top_authors = Author.query.order_by(Author.fiction_count.desc()).limit(12).all()
    
    return  render_template("home.html", top_view_fictions = top_view_fictions, top_authors=top_authors)


@app.route("/img-cover/<path:link>")
def img_proxy(link):
    url="http://skybooks.vn/wp-content/uploads/2021/03/chung-ta-khong-the-la-ban-tang-kem-bookmark-so-tay-1.jpg"
    print(link)
    img = return_img(link)
    img.seek(0)
    return  send_file(img, mimetype='image/jpeg')

@app.route("/test/new/", methods=['GET', 'POST'])
def test():
    form = AuthorForm()
    if form.validate_on_submit():
        author = Author(name=form.author_name.data, img=form.img.data, about=form.about.data)
        db.session.add(author)
        db.session.commit()
        flash('New Author created')
        return redirect(url_for('test'))  
    print (form.errors)   
    return  render_template("test.html", form=form)

@app.route("/new-fiction/", methods=['GET', 'POST'])
def new_fiction():
    if request.method=='POST':
        data = request.form.to_dict(flat=True)
        name=data["fiction-name"]
        cover=data["cover-image"]
        status=bool(data["publish-status"])
        desc=data["description"]
        publish_year=data["publishted-date"]
        author=data["author"]
        new_fiction = Fiction(name=name, cover=cover, status=status,desc=desc, publish_year=publish_year, author_id=author)
        db.session.add(new_fiction)
        db.session.commit()
        db.session.refresh(new_fiction)
        print(new_fiction)
        return redirect(url_for('index')) 
    return new_data

@app.route("/test/new-fiction/", methods=['GET', 'POST'])
def test_new_fiction():
    form = FictionForm()
    if form.validate_on_submit():
        desc = { 
            "time": 1618735370183,
            "blocks": [
                {
                "type": "paragraph",
                "data": {"text": form.desc.data}
                }
            ],
            "version": "2.20.1",
        }
        new_fiction=Fiction(name=form.name.data, cover=form.cover.data, desc=str(desc), status=form.status.data, author_id=form.author.data, publish_year=form.year.data)
        db.session.add(new_fiction)
        db.session.commit()
        db.session.refresh(new_fiction)
        flash("Data is saved")
        return redirect(url_for("edit_specific_post", fiction_id=new_fiction.id))
    return  render_template("new_fiction.html", form=form)

@app.route("/author/<author_name>", methods=['GET', 'POST'])
def author_page(author_name):
    author = Author.query.filter_by(name=author_name).first()
    fictions = Fiction.query.filter_by(author_id=author.id)
    form = AuthorForm()
    if form.validate_on_submit():
        author.name = form.author_name.data
        author.img=form.img.data 
        about = { 
            "time": 1618735370183,
            "blocks": [
                {
                "type": "paragraph",
                "data": {"text": form.about.data}
                }
            ],
            "version": "2.20.1",
        }
        author.about=str(about)
        db.session.commit()
        flash("Update completed")
        return redirect(url_for('author_page', author_name=author.name))
    return render_template("author.html", author = author, fictions =fictions, form=form)

@app.route("/author/<int:author_id>/delete")
def delete_author(author_id):
    fictions = Fiction.query.filter_by(author_id=author_id).delete()
    author = Author.query.filter_by(id=author_id).delete()
    db.session.commit()
    return redirect(url_for('all_authors'))

@app.route("/authors/")
def all_authors():
    authors = Author.query.all()
    return render_template("authors.html", authors = authors)


@app.route("/fictions")
def fictions():
    fictions = Fiction.query.all()
    return  render_template("fictions.html", fictions = fictions)

@app.route("/fiction/<int:fiction_id>/", methods=['GET', 'POST'])
def specific_post(fiction_id):
    fiction = Fiction.query.filter_by(id=fiction_id).first()
    author = Author.query.filter_by(id=fiction.author_id).first()
    chapter = Chapter.query.filter_by(fiction=fiction_id).first()

    dsc = fiction.desc
    chapters = Chapter.query.filter_by(fiction=fiction_id).order_by(Chapter.chapter_order.asc())
    quote = Quote.query.filter_by(fiction=fiction_id)
    form = FictionForm()
    
    if form.validate_on_submit():
        fiction.name=form.name.data
        fiction.cover=form.cover.data
        desc = { 
            "time": 1618735370183,
            "blocks": [
                {
                "type": "paragraph",
                "data": {"text": form.desc.data}
                }
            ],
            "version": "2.20.1",
        }
        fiction.desc=form.desc.data
        fiction.author_id=form.author.data
        fiction.status=bool(form.status.data)
        fiction.publish_year=form.year.data
        db.session.commit()
        flash("Data is saved")
        return redirect(url_for("specific_post", fiction_id=fiction.id))
    print(form.errors)
    return  render_template("viewer.html",form=form, fiction = fiction, chapters = chapters, quote = quote, author =author, chapter=chapter, dsc=dsc)


@app.route("/fiction/<int:fiction_id>/edit", methods=['GET', 'POST'])
def edit_specific_post(fiction_id):
    fiction = Fiction.query.filter_by(id=fiction_id).first()
    author = Author.query.filter_by(id=fiction.author_id).first()
    chapter = Chapter.query.filter_by(fiction=fiction_id).first()
    editable = True
    chapters = Chapter.query.filter_by(fiction=fiction_id)
    quote = Quote.query.filter_by(fiction=fiction_id)
    if request.method == 'POST':
        incoming_data= json.loads(request.data.decode('UTF-8'))
        fiction.name = str(incoming_data['title'])
        fiction.desc = str(incoming_data['desc'])
        print(fiction.name, fiction.desc )
        db.session.commit()
        flash("Data saved")
    return  render_template("viewer_clone.html", fiction = fiction, chapters = chapters, quote = quote, author =author, chapter=chapter, editable=editable)


@app.route("/fiction/<int:fiction_id>/delete", methods=['GET', 'POST'])
def delete_fiction(fiction_id):
    chapters = Chapter.query.filter_by(fiction=fiction_id).delete()
    fiction = Fiction.query.filter_by(id=fiction_id).delete()
    db.session.commit()
    return  redirect(url_for("fictions"))


@app.route("/fiction/<fiction_name>/")
def specific_fiction_name(fiction_name):
    fiction = Fiction.query.filter_by(name=fiction_name).first()
    author = Author.query.filter_by(id=fiction.author_id).first()
    chapters = Chapter.query.filter_by(fiction=fiction.id)
    quote = Quote.query.filter_by(fiction=fiction.id)
    return  render_template("viewer.html", fiction = fiction, chapters = chapters, quote = quote, author =author)


@app.route("/chapter/<int:chapter_id>/", methods=['GET', 'POST'])
def chapter_viewer(chapter_id):
    chapter = Chapter.query.filter_by(id=chapter_id).first()
    chapter.update_view()
    fiction = Fiction.query.filter_by(id=chapter.fiction).first()
    chapters = Chapter.query.filter_by(fiction=fiction.id).order_by(Chapter.chapter_order.asc())
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
    form=ChapterForm()
    if form.validate_on_submit():
        chapter.name=form.name.data 
        chapter.content=form.content.data 
        chapter.chapter_order=form.chapter_order.data 
        db.session.commit()
        return redirect(url_for('chapter_viewer', chapter_id=chapter.id))
    return render_template('chapter.html', form = form, chapter = chapter, fiction=fiction, chapters = chapters, next_chapter = nct, previous_chapter = pre)


@app.route("/editor/<int:fiction_id>/new-chapter/", methods=['GET', 'POST'])
def new_chapter(fiction_id):
    form=ChapterForm()
    if form.validate_on_submit():
        content = form.content.data 
        content.replace("\/r\/n",'</p><p>')
        new_chapter = Chapter(name=form.name.data, content=content, chapter_order=form.chapter_order.data, fiction=fiction_id)
        db.session.add(new_chapter)
        db.session.commit()
        db.session.refresh(new_chapter)
        return redirect(url_for('chapter_viewer', chapter_id=new_chapter.id))
    return render_template('new_chapter.html', form=form)

@app.route("/api/<int:fiction_id>/", methods = ['GET'])
def api_send_fiction(fiction_id):
    fiction = Fiction.query.filter_by(id=fiction_id).first()
    chapter = Chapter.query.filter_by(fiction=fiction_id) 
    return jsonify(fiction)
    

@app.route("/api/<int:fiction_id>/<int:chapter_order>", methods = ['GET'])
def api_send_chapter_content(chapter_order, fiction_id):
    chapter = Chapter.query.filter_by(fiction=fiction_id, chapter_order=chapter_order).first()
    return jsonify(chapter)


@app.route("/api/chapter/<int:chapter_id>/", methods = ['GET'])
def api_chapter_id(chapter_id):
    chapter = Chapter.query.filter_by(id=chapter_id).first()
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


