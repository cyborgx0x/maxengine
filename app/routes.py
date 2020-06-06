from flask import Flask
from flask import render_template
from flask import request, redirect
from getnews import get_news
from app.models import Post
from app import app

@app.route("/")
def index():
    return  render_template("form.html")

@app.route("/", methods=['GET','POST'])
def getcontent():
    link = request.form['url']
    get_news(link)
    return  redirect('postlist')

@app.route("/postlist")
def post():
    posts = Post.query.all()
    return  render_template("post.html", posts = posts)