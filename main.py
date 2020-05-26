from app import app, db
from app.models import Post
from engine import chaptercontent, chaptername

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Post': Post, 'Name': chaptername, 'Content': chaptercontent}

