from engine import  Website, Crawler
from app.models import Post
from app import app, db

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

    
class Newsparser(Crawler):
    def parse(self, site, url):
        file = self.getpage(url)
        if file is not None:
            title = self.selector(file, site.titletag)
            print(title)
            excerpt = self.selector(file, site.bodytag)
            print(excerpt)
            if title != '' and excerpt != '':
                news = News(url, title, excerpt)
                newpost = Post(title=title, excerpt=excerpt, original_link=url )
                db.session.add(newpost)
                db.session.commit()
                
crawler = Newsparser()
urllib =[['dantri','dantri.com.vn','title', 'div.dt-news__sapo']]
websites=[]
for row in urllib:
    websites.append(Website(row[0], row[1], row[2], row[3]))
def get_news(link):
    crawler.parse(websites[0],link)   
