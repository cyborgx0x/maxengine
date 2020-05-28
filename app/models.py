from app import db
from datetime import datetime

class Post(db.Model):
    __tablename__ = 'wp_posts'
    id = db.Column('id',db.Integer, primary_key=True)
    title = db.Column('post_title',db.Unicode)
    content = db.Column('post_content',db.Unicode)
    timestamp = db.Column('post_date_gmt',db.DateTime, index=True, default=datetime.now)
    excerpt = db.Column('post_excerpt', default='')
    toping = db.Column('to_ping', default='')
    pinged = db.Column('pinged', default='')
    filtered = db.Column('post_content_filtered', default='')


    def __repr__(self):
        return 'Post {}>'.format(self.content)