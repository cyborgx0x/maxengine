import requests
from bs4 import BeautifulSoup
import re
import csv


# Get chapter list

chapter_list_source = requests.get(input("Paste the link:")).text
r = BeautifulSoup(chapter_list_source, 'lxml')
filename = str(r.title.text)
filename=filename.replace(" ", "-")+'.html'
chapter_list = r.find_all('ul', class_='list-chapter')

urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', str(chapter_list))
# print(urls)
# print(filename)
html_file = open(filename,'w')
# # Get content
for url in urls:
    chapter_source = requests.get(url).text
    soup = BeautifulSoup(chapter_source, 'lxml')

    chapter_name = soup.title.text
    print(chapter_name)

    chapter_content = soup.find('div', class_='chapter-c')
    print(chapter_content)

    html_file.write(chapter_name)
    html_file.write(str(chapter_content))

html_file.close()

