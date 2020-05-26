from app import db
import datetime

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    body = db.Column(db.String(10000))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.date.today())

    def __repr__(self):
        return 'Post {}>'.format(self.body)