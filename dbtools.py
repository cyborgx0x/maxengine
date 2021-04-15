from app.models import Fiction, Author, Chapter
from app import db
import random

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
# update_chapter_count()
# update_fiction_count()


def update_chapter_count_begin():
    fictions = Fiction.query.all()
    for fiction in fictions:
        chapters = Chapter.query.filter_by(fiction = fiction.id)
        
        for chapter in chapters:
            chapter.view_count =+  random.randrange(10000)
        
        print(fiction.name, chapter.view_count)
    db.session.commit()
# update_chapter_count_begin()
# update_fiction_view()
# content = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
# fictions = Fiction.query.all()
# for fiction in fictions:
#     for i in range (20): 
#         chapter_order = i
#         name = "Chương " + str(i)
#         c = Chapter(name = name, content = content, fiction =fiction.id, chapter_order = chapter_order)
#         db.session.add(c)
#         db.session.commit()

def replace_new_line(a,b):
    fictions = Fiction.query.all()
    for f in fictions:
        if f.desc:
            txt = f.desc
            f.desc = txt.replace(a,b)
            print(f.name, "is replacing")
        else:
            print("desc not exitst")
            f.desc = "sample desc"
    chapters = Chapter.query.all()
    for c in chapters:
        if c.content:
            txt=c.content
            c.content = txt.replace(a,b)
            print("chapter ", c.name, "is replacing")
        else:
            print("content not found, creating new one")
            c.content = "sample content"
    db.session.commit()
# a = "</p></p>"
# b = "</p>"
# replace_new_line(a,b)

f = Fiction.query.order_by(Fiction.id.desc()).first()
txt = f.desc
f.desc = txt.replace("\r\n","</p><p>")
db.session.commit()