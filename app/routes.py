from flask import Flask
from flask import render_template
from flask import request, redirect
from engine import normalnews
from app import app, db
from app.models import Post

@app.route("/")
def index():
    return  render_template("form.html")

@app.route("/", methods=['GET','POST'])
def getcontent():
    link = request.form['url']
    normalnews(link)
    return  redirect('postlist')

@app.route("/postlist")
def post():
    posts = Post.query.all()
    return  render_template("post.html", posts = posts)