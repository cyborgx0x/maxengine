import requests
from bs4 import BeautifulSoup
import lxml
import re
from app import db
from app.models import Fiction, Author


class Content:
    """ 
    Class for all page
    """
    def __init__(self,url,title,body):
        self.url = url
        self.title = title
        self.body = body
    def __repr__(self):
        return '{}  \n {}  \n {}'.format(self.url,self.title,self.body)
 

class Website:
    """Contain the website structure"""
    def __init__(self, name, url, titletag, bodytag):
        self.name = name
        self.url = url
        self.titletag = titletag
        self.bodytag = bodytag


def getpage(url):
    try: 
        source = requests.get(url).text
    except  requests.exceptions.RequestException:
        return None
    return BeautifulSoup(source, 'lxml')

def selector(page, selector):
    """
    the selector rule
    """
    elements = page.select(selector)
    if elements is not None and len(elements) > 0:
        return '\n'.join([elem.get_text() for elem in elements])
    return ''

def parse(site, url):
    """
    extract content
    """
    file = getpage(url)
    if file is not None:
        title = selector(file, site.titletag)
        body = selector(file, site.bodytag)
        cover = file.select_one(".cover")
        author = file.select_one(".author").get_text()
        img = cover["src"]
    return {
        "name":title,
        "desc": body,
        "cover": img,
        "author": author
    }
# url = 'https://webtruyen.com/tong-tai-vo-ngai-la-hacker-ngam/'
# links = ['https://webtruyen.com/tong-tai-vo-ngai-la-hacker-ngam/', 'https://webtruyen.com/nu-quyen-anh-xuyen-thanh-co-gai-nong-thon/', 'https://webtruyen.com/neu-moi-thu-la-cach-tro/', 'https://webtruyen.com/series-truyen-ma-tam-linh-truyen-ky/', 'https://webtruyen.com/trai-tim-nay-la-de-yeu-thuong/', 'https://webtruyen.com/thien-truong-dia-cuu-co-mot-tinh-yeu-duoc-goi-la-buong-tay/', 'https://webtruyen.com/khi-nha-van-tap-yeu/', 'https://webtruyen.com/cham-mot-buoc/', 'https://webtruyen.com/trong-ac-quy-co-dau-thuong/', 'https://webtruyen.com/thanh-chien-phuc-sinh-mat-the-xac-song/', 'https://webtruyen.com/sinh-ton-o-khu-rung-ky-quai-ban-doi-toi-la-thu-nhan/', 'https://webtruyen.com/me-cung-tuyet-vong-1-noi-khoi-dau-tuyet-vong/', 'https://webtruyen.com/thien-kiep/', 'https://webtruyen.com/mai-mot-tinh-yeu/', 'https://webtruyen.com/song-gio/', 'https://webtruyen.com/mong-ngan-nam/', 'https://webtruyen.com/ginsherry-bloody-rose/', 'https://webtruyen.com/nam-tay-nhau-buoc-qua-thanh-xuan-ruc-ro/', 'https://webtruyen.com/de-ho-truyen/', 'https://webtruyen.com/ma-de-truyen-ky-mong-ao-tu-tien/', 'https://webtruyen.com/cho-toi-them-mot-chut-thanh-xuan/', 'https://webtruyen.com/mot-thoi-de-nho-1/', 'https://webtruyen.com/long-cai-ban-lao-tu-cu-nhu-vay-nguu/', 'https://webtruyen.com/gap-anh-o-nga-re-tinh-yeu-1/', 'https://webtruyen.com/toi-tro-thanh-con-cho-cua-bao-chua/']

site = Website("title", "title", "title", ".description")
url = "https://webtruyen.com/truyen-ngon-tinh-hay/"
fictions  = requests.get(url).text
res = BeautifulSoup(fictions, 'lxml')
res.find("div", class_="list-stories")
all_link = res.find_all("a", class_="thumb")
links = []
for link in all_link:
    links.append( link['href'])
    print(links)


for url in links:
    A = parse(site,url)
    author = Author.query.filter_by(name=A['author']).first()
    if author:
        print("author exist")
        print(A)
        new_fiction = Fiction(name = A['name'], desc = A['desc'], cover = A['cover'], author_id = author.id)
        db.session.add(new_fiction)
        db.session.commit() 
    else:
        print("create new author")
        new_author = Author(name = A['author'])
        db.session.add(new_author)
        db.session.flush()
        new_fiction = Fiction(name = A['name'], desc = A['desc'], cover = A['cover'], author_id = new_author.id)
        db.session.add(new_fiction)
        db.session.commit() 



