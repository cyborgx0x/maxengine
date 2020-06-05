import requests
from bs4 import BeautifulSoup
import lxml
import re
from app.models import Post
from app import app, db

def get_url(link):
    coreurl=link.split('/')[2]
    urllibrary={
        "truyenfull.vn":"div#list-chapter",
        "truyen.tangthuvien.vn":"ul.cf"
    }
    comparing=urllibrary[coreurl]
    chapter_list_source = requests.get(link).text
    r = BeautifulSoup(chapter_list_source, 'lxml')
    chapter_list = r.select(comparing)
    # urls = [e.a.attrs['href'] for e in chapter_list]
    return re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', str(chapter_list))
    

class Content:
    """
    Class for all page
    """
    def __init__(self,url,title,body):
        self.url = url
        self.title = title
        self.body = body
    def writedb(self):
        """
        write to database
        """
        print("URL: {}".format(self.url))
        print("title: {}".format(self.title))
        print("body: {}".format(self.body))   

class Website:
    """Contain the website structure"""
    def __init__(self, name, url, titletag, bodytag):
        self.name = name
        self.url = url
        self.titletag = titletag
        self.bodytag = bodytag

class Crawler: 
    '''
    Crawler Engine
    '''

    def getpage(self, url):
        try: 
            source = requests.get(url).text
        except  requests.exceptions.RequestException:
            return None
        return BeautifulSoup(source, 'lxml')

    def selector(self, page, selector):
        """
        the selector rule
        """
        elements = page.select(selector)
        if elements is not None and len(elements) > 0:
            return '\n'.join([elem.get_text() for elem in elements])
        return ''

    def parse(self, site, url):
        """
        extract content
        """
        file = self.getpage(url)
        if file is not None:
            title = self.selector(file, site.titletag)
            body = self.selector(file, site.bodytag)
            if title != '' and body != '':
                content = Content(url, title, body)
            newpost = Post(title=title, content=body)
            db.session.add(newpost)
            db.session.commit()
                

crawler = Crawler()

urllib=[
    ['truyenfull','truyenfull.vn','title', 'div.chapter-c'],
    ['tangthuvien','truyen.tangthuvien.vn','title', 'div.chapter-c-content'],
    ['dantri','dantri.com.vn','title', 'div#divNewsContent'],
]
websites = []
for row in urllib:
    websites.append(Website(row[0], row[1], row[2], row[3]))


def fictionparser(link):
    links = get_url(link)
    for l in links:
        crawler.parse(websites[0], l)
def normalnews(link):
    crawler.parse(websites[2],link)
