import requests
from bs4 import BeautifulSoup
import lxml
import re
from app.models import Post
from app import app, db


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
                print(content)
            # newpost = Post(title=title, content=body)
            # db.session.add(newpost)
            # db.session.commit()
                

