from app.models import Post, Urllib
from app import app, db

def insert_post(title,excerpt,original_link):
    newpost = Post(title=title, excerpt=excerpt, original_link=original_link )
    db.session.add(newpost)
    db.session.commit()  

def delete_all_post():
    selected = Post.query.all()
    for i in selected:
        db.session.delete(i)
    db.session.commit()
def view_all_post():
    selected = Post.query.all()
    return selected
def receive_lib(website_url):
    received = Urllib.query.filter_by(website_url=website_url).first()
    return received
def import_lib(name, url, title_tag, body_tag):
    newlib = Urllib(website_name=name, website_url=url, website_title_tag=title_tag, website_body_tag=body_tag)
    db.session.add(newlib)
    db.session.commit()