from bs4 import BeautifulSoup
import lxml
import requests
import re


def get_url(y):
    chapter_list_source = requests.get(y).text
    r = BeautifulSoup(chapter_list_source, 'lxml')
    chapter_list = r.find_all('ul', class_='list-chapter')
    # urls = [e.a.attrs['href'] for e in chapter_list]
    urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', str(chapter_list))
    return urls