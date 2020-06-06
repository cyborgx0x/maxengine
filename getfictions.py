from engine import Content, Website, Crawler
import requests
from bs4 import BeautifulSoup
import lxml
import re

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
    

crawler = Crawler()

urllib=[
    ['truyenfull','truyenfull.vn','title', 'div.chapter-c'],
    ['tangthuvien','truyen.tangthuvien.vn','title', 'div.chapter-c-content'],
]
websites = []
for row in urllib:
    websites.append(Website(row[0], row[1], row[2], row[3]))


def get_fictions(link):
    links = get_url(link)
    for l in links:
        crawler.parse(websites[0], l)
        
link='https://truyenfull.vn/cau-ma/'
get_fictions(link)