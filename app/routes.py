from flask import Flask
from flask import render_template
from flask import request, redirect
from app.models import Post
from app import app
    

@app.route("/submit")
def submit():
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
def all_post():
    posts = Post.query.all()
    return  render_template("post.html", posts = posts)

@app.route("/post/<int:post_id>")
def specific_post(post_id):
    this_post = Post.query.filter_by(id=post_id).first()
    return  render_template("thispost.html", post = this_post)