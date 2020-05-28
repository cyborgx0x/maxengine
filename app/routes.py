from flask import Flask
from flask import render_template
from flask import request, redirect
from engine import chaptercontent, chaptername
from urlprocessing import get_url
from app import app, db
from app.models import Post


@app.route("/")
def index():
    return  render_template("form.html")

@app.route("/", methods=['GET','POST'])
def getcontent():
    link = request.form['url']
    urlslist = get_url(link)
    message = "successed"
    for url in urlslist:
        b = chaptername(url)
        c = chaptercontent(url)
        p = Post(title=b, content=c)
        db.session.add(p)
        db.session.commit()
        # with open(a, 'w', encoding='utf-8') as f:
        #     f.write(b + c )
        #     f.flush()
    return  redirect('postlist')

@app.route("/postlist")
def post():
    posts = Post.query.all()
    return  render_template("post.html", posts = posts)