from app import db
from datetime import datetime
from sqlalchemy import MetaData
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login
from hashlib import md5
meta = MetaData()

class Post(db.Model):
    'engine', meta
    __tablename__ = "engine"
    id = db.Column('id',db.Integer, primary_key=True)
    title = db.Column('post_title',db.Unicode(300))
    content = db.Column('post_content',db.Unicode(5000))
    timestamp = db.Column('post_date_gmt',db.DateTime, index=True, default=datetime.utcnow)
    excerpt = db.Column('post_excerpt',db.Unicode(500))
    original_link = db.Column('original_link', db.Unicode(300))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return 'Post {}>'.format(self.title)
    
class User(UserMixin, db.Model):
    'users', meta
    id = db.Column('id', db.Integer, primary_key=True)
    first_name = db.Column('first_name',db.Unicode(50))
    last_name = db.Column('last_name',db.Unicode(50))
    user_name = db.Column('user_name', db.String(64))
    email = db.Column('email', db.String(120))
    password_hash = db.Column(db.String(128))
    post = db.relationship('Post', backref ='author', lazy='dynamic')
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

class Urllib(db.Model):
    'urllib', meta
    id = db.Column('id', db.Integer, primary_key=True)
    website_name = db.Column('website_name', db.String(100))
    website_url = db.Column('website_url', db.String(100))
    website_title_tag = db.Column('website_title_tag', db.String(100))
    website_body_tag = db.Column('website_body_tag', db.String(100))
