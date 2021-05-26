import requests
from bs4 import BeautifulSoup
import lxml
import re
from .utils import extract

class Config(object):
    webtruyen = {
                "name": "webtruyen",
                "title": "title",
                "description": ".description",
                "link": ""
                }

class Parser:
    def __init__(self, name, url):
        '''
        contain data and method that parse website, data, to initialize the class, import the name of website, and the url that need to parse.
        if the name is not in the library, this would return an errs (processing)

        Usage:

        f = Parser("webtruyen", "https://webtruyen.com/truyen-ngon-tinh-hay/")
        print(f.parse_link())

        f = Parser("webtruyen", "https://webtruyen.com/tong-tai-vo-ngai-la-hacker-ngam/")
        print(f.parse_content("description"))


        f = Parser("truyenfull", "https://truyenfull.vn/pham-nhan-tu-tien/chuong-1")
        print(f.parse_content("content"))

        d = Parser("dantri","https://dantri.com.vn/kinh-doanh/de-xuat-giam-gia-dien-tien-dien-do-anh-huong-covid-19-20210520223014984.htm")
        print(d.parse_content("content"))
        '''
        self.name = name
        self.url = url
        self.lib = {
            "webtruyen.com":{
                "name": "webtruyen",
                "title": "title",
                "description": ".description",
                "link": ""
            },
            "truyenfull.vn": {
                "name": "truyenfull",
                "title": "title",
                "content": ".chapter-c",
                "description": ".chapter-c",
            },
            "dantri.com.vn": {
                "title": "title",
                
                "content": ".dt-news__content"
            },
            "localhost":{
                "name":"localhost",
                "title": "title",
                "description": ".entry-content",
            },
        }
        self.page = self.get_page(self.url)
        self.title = self.parse_content("title")
        self.content = self.parse_content("description")
    def get_page(self,url):
        '''
        take an url as argument and return an BeautifulSoup Object
        also, set the self page = this object
        '''
        try: 
            source = requests.get(url).text
        except  requests.exceptions.RequestException:
            return None
        return BeautifulSoup(source, 'lxml')
    def select_element(self, selector):
        '''
        take an Beautiful Object and param, set the self elements and return a string
        '''
        elements = self.page.select(selector)
        if elements is not None and len(elements) > 0:
            return '\n'.join([elem.get_text() for elem in elements])
        return ''
    def parse_content(self, type):
        selector = self.lib[self.name][type]
        try:
            content = self.select_element(selector)
        except:
            content = "Network Err"
        return content
    def parse_link(self):
        f = self.page.select(".list-stories > ul > li > .thumb")
        links = []
        for e in f: 
            links.append(e['href'])
        print(links)

def get_url(link, comparing):
    chapter_list_source = requests.get(link).text
    r = BeautifulSoup(chapter_list_source, 'lxml')
    chapter_list = r.select(comparing)
    # urls = [e.a.attrs['href'] for e in chapter_list]
    return re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', str(chapter_list))