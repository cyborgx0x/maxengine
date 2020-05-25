import requests
from bs4 import BeautifulSoup
import re
import writefile

# Get path of file
# def get_name(): 
#     filename = str(r.title.text)
#     filename='./templates/' + filename.replace(" ", "-")+'.html'
#     return filename

def chaptername(url):
    chapter_source = requests.get(url).text
    soup = BeautifulSoup(chapter_source, 'lxml')
    return soup.title.text

def chaptercontent(url):
    chapter_source = requests.get(url).text
    soup = BeautifulSoup(chapter_source, 'lxml')
    content = str(soup.find('div', class_='chapter-c'))
    return content

