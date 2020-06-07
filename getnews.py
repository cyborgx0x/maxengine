from engine import  Website, parse
from database import insert_post, receive_lib
import requests
from bs4 import BeautifulSoup

class News:
    """
    class for the job that we get
    """
    def __init__(self,url,title, excerpt):
        self.url = url
        self.title = title
        self.excerpt = excerpt
    def __repr__(self):
        return '{}  \n {}  \n {}'.format(self.url,self.title,self.excerpt)
    def insert_news_to_db(self):
        insert_post(self.title,self.excerpt,self.url)

lib = receive_lib("dantri.com.vn")
site = Website(lib.website_name, lib.website_url, lib.website_title_tag, lib.website_body_tag)
    
links=[
    "https://beta.dantri.com.vn/phap-luat/nguoi-dan-mong-som-bat-duoc-pham-nhan-vuot-nguc-lan-tron-tren-deo-hai-van-20200606103249738.htm",
    "https://beta.dantri.com.vn/viec-lam/ha-noi-ban-hanh-lo-trinh-giai-ngan-goi-62000-ty-dong-toi-5-nhom-doi-tuong-20200513073448996.htm"
]

sources = 'https://beta.dantri.com.vn/su-kien/7-6-2020.htm'
link_format = "datetime.today().strftime('%d-%m-%Y')"
source = requests.get(sources).text
soup = BeautifulSoup(source, 'lxml')
url = soup.main.find_all('a')
urls=set()
for link in url:
    try: 
        newlink=link['href']
        urls.add(newlink)
    except KeyError:
        pass
print (urls)
urls.remove('/su-kien/trang-2.htm')
urls.remove('/su-kien.htm')
fullurls=set()
for item in urls:
    fullurls.add('https://beta.dantri.com.vn'+str(item))
print (fullurls)

for item in fullurls:
    A = parse(site,item)
    news_a = News(*A)
    news_a.insert_news_to_db()
    