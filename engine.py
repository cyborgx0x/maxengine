import requests
from bs4 import BeautifulSoup
import writefile


def chaptername(url):
    chapter_source = requests.get(url).text
    soup = BeautifulSoup(chapter_source, 'lxml')
    return soup.title.text

def chaptercontent(url):
    chapter_source = requests.get(url).text
    soup = BeautifulSoup(chapter_source, 'lxml')
    content = str(soup.find('div', class_='chapter-c'))
    return content

# create
def createname(x):
    filename = './templates/' + x.replace(" ", "-")   + '.html'
    filename = filename.replace(":","-")
    filename = filename.replace("?","-")
    return filename