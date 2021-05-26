import json
from dataclasses import dataclass
from datetime import datetime
from hashlib import md5

from sqlalchemy import MetaData, Text

from app import db

meta = MetaData()

@dataclass
class Fiction(db.Model):
    id:int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name:str = db.Column(db.Unicode(300))
    status = db.Column(db.Boolean,  default = True)
    view = db.Column(db.Integer)
    desc = db.Column(db.Text)
    cover = db.Column(db.Text)
    publish_year = db.Column(db.Integer)
    page_count = db.Column(db.Integer)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'))
    tiki_link = db.Column(db.Text)
    mediafire_link = db.Column(db.Text)
    slug = db.Column(db.String(160))
    version = db.Column(db.Integer)
    chapter_count = db.Column(db.Integer)
    quote_count = db.Column(db.Integer)
    chapter = db.relationship('Chapter')
    tag = db.Column(db.Unicode(300))
    like = db.relationship('Like', backref ='fiction')
    media = db.relationship('Media', backref='fiction')



@dataclass
class FictionIndex(Fiction):
    id:int
    name: str
    desc: str 

    
@dataclass
class Chapter(db.Model):
    id:int
    name: str
    content: str

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(160))
    content = db.Column(db.Text)
    view_count = db.Column(db.Integer)
    fiction = db.Column(db.Integer, db.ForeignKey('fiction.id'))
    chapter_order = db.Column(db.Integer)


@dataclass
class Author(db.Model):
    id: int
    name: str 
    img: str
    fiction: Fiction
    about: str

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(160))
    birth_year = db.Column(db.Integer)
    author_page = db.Column(db.String(160))
    about = db.Column(db.Text)
    view = db.Column(db.Integer)
    fiction = db.relationship('Fiction', backref ='author')
    media = db.relationship('Media', backref ='author')
    email = db.Column('email', db.String(120))
    img = db.Column(db.String(240))
    fiction_count = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class Quote(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    quote = db.Column(db.Text)
    fiction = db.Column(db.Integer, db.ForeignKey('fiction.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'))
    img = db.Column(db.Text)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Unicode(300))
    content = db.Column(db.Text)
    post_type = db.Column(db.Unicode(300))
    template = db.Column(db.Unicode(200))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class Media(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Unicode(300))
    content = db.Column(db.Text)
    media_type = db.Column(db.Unicode(300))
    fiction_id = db.Column(db.Integer, db.ForeignKey('fiction.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
