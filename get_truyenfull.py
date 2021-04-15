from bs4 import BeautifulSoup
import lxml
from app import db
from app.models import Chapter
import requests
for i in range(2425):
    link = "https://truyenfull.vn/pham-nhan-tu-tien/chuong-"+ str(1+i)
    file = requests.get(link).text
    bs = BeautifulSoup(file, "lxml")
    elements = bs.select_one(".chapter-c")
    title = bs.title.get_text()
    elements = str(elements).replace("div", "p")
    elements = elements.replace("<br/><br/>", "</p><p>")
    print(elements, title)
    c = Chapter (name = title, content = elements, fiction = 80, chapter_order = 1+i)
    db.session.add(c)
    print("add", c, "to the quere")
    db.session.commit()
