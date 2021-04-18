from app import db
from datetime import datetime
from sqlalchemy import MetaData, Text
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login
from hashlib import md5
from dataclasses import dataclass
meta = MetaData()


@dataclass
class Fiction(db.Model):
    'fiction', meta
    id: int
    name: str
    desc: str
    cover: str

    __tablename__ = "fiction"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Unicode(300))
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

    def set_count(self, chapter_count):
        self.chapter_count = chapter_count
        print("update completed")    
    def set_view(self, total_view):
        self.view = total_view
        print("update completed")    

    def __repr__(self):
        return 'Fiction info {}>'.format(self.name)


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
    def update_view(self):
        if self.view_count:
            self.view_count=self.view_count+1
        else:
            self.view_count = 1
        print(self.id, self.name, self.view_count)
        db.session.commit()
    def update_chapter_count_zero(self, count):
        self.view_count = count
        db.session.commit()


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
    fiction = db.relationship('Fiction', backref ='fiction')
    email = db.Column('email', db.String(120))
    img = db.Column(db.String(240))
    fiction_count = db.Column(db.Integer)
    def set_count(self, fiction_number):
        self.fiction_count = fiction_number
        print("update completed")
    def update_fiction_count(self):
        fiction_number = Fiction.query.filter_by(author_id=self.id).count()  
        self.fiction_count = fiction_number
        print (self.name, fiction_number)
        db.session.commit()

class Quote(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    quote = db.Column(db.Text)
    fiction = db.Column(db.Integer, db.ForeignKey('fiction.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'))
    img = db.Column(db.Text)



class User(UserMixin, db.Model):
    'users', meta
    id = db.Column('id', db.Integer, primary_key=True)
    first_name = db.Column('first_name',db.Unicode(50))
    last_name = db.Column('last_name',db.Unicode(50))
    user_name = db.Column('user_name', db.String(64))
    email = db.Column('email', db.String(120))
    password_hash = db.Column(db.String(128))
    # post = db.relationship('Post', backref ='author', lazy='dynamic')
    about_me = db.Column(db.String(140))
    last_seen = db.Column (db.DateTime, default = datetime.utcnow)
    def __repr__(self):
        return '<User {}>'.format(self.user_name)
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    @login.user_loader
    def load_user(id):
        return User.query.get(int(id))
    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)