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
    excerpt = db.Column('post_excerpt',db.Unicode(200), default='')

    def __repr__(self):
        return 'Post {}>'.format(self.content)