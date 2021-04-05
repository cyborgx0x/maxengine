from app.models import Fiction, Author, Chapter
from app import db

class Query_Fiction(Fiction):

    def get_fiction_by_id(id):
        fiction = Fiction.query.filter_by(id=id).first()
        return fiction.name

    def get_fiction_by_author_name(author_name):
        fictions = Fiction.query.filter_by(author=author_name)
        dataset = []
        for fiction in fictions:
            dataset.append(fiction)
        return dataset

    def get_fiction_by_author_id(author_id):
        fictions = Fiction.query.filter_by(author_id=author_id).count()
        return fictions

def update_chapter_count():
    fictions = Fiction.query.all()
    for fiction in fictions:
        chapter_count = Chapter.query.filter_by(fiction = fiction.id).count()
        fiction.set_count(chapter_count)
        print(fiction.name, chapter_count)
    db.session.commit()

def update_fiction_count():
    authors = Author.query.all()
    for author in authors:
        fiction_number = Fiction.query.filter_by(author_id=author.id).count()  
        author.set_count(fiction_number)    
        print (author.name, fiction_number)
    db.session.commit()
    
def update_fiction_view():
    fictions = Fiction.query.all()
    for fiction in fictions:
        chapters = Chapter.query.filter_by(fiction = fiction.id)
        total_view = 0
        for chapter in chapters:
            total_view = total_view + chapter.view_count
        fiction.set_view(total_view)
        print(fiction.name, total_view)
    db.session.commit()
update_fiction_view()