import requests
from bs4 import BeautifulSoup
import lxml
import re



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
    return url, title, body


                

