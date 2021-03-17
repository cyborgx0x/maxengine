from app.models import Fiction
from app import app, db

def insert_post(title,excerpt,original_link):
    newpost = Fiction(title=title, excerpt=excerpt, original_link=original_link )
    db.session.add(newpost)
    db.session.commit()  

def delete_all_post():
    selected = Fiction.query.all()
    for i in selected:
        db.session.delete(i)
    db.session.commit()
def view_all_post():
    selected = Fiction.query.all()
    return selected

