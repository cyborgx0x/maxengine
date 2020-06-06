from app import db
from datetime import datetime
from sqlalchemy import MetaData

meta = MetaData()

class Post(db.Model):
    'posts', meta
    id = db.Column('id',db.Integer, primary_key=True)
    title = db.Column('post_title',db.Unicode(300))
    content = db.Column('post_content',db.Unicode(5000))
    timestamp = db.Column('post_date_gmt',db.DateTime, index=True, default=datetime.now)
    excerpt = db.Column('post_excerpt',db.Unicode(200))
    original_link = db.Column('original_link', db.Unicode(300))
    

    def __repr__(self):
        return 'Post {}>'.format(self.content)
    
class User(db.Model):
    'users', meta
    id = db.Column('id', db.Integer, primary_key=True)
    first_name = db.Column('first_name',db.Unicode(50))
    last_name = db.Column('last_name',db.Unicode(50))
    user_name = db.Column('user_name', db.String(20))
    email = db.Column('email', db.String(64))
    password_hash = db.Column(db.String(128))

    