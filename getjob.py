from engine import  Website, Crawler

class Job:
    """
    class for the job that we get
    """
    def __init__(self,url,title, excerpt):
        self.url = url
        self.title = title
        self.excerpt = excerpt
    
    
class Jobparser(Crawler):
    def parse(self, site, url):
        file = self.getpage(url)
        if file is not None:
            title = self.selector(file, site.titletag)
            print(title)
            excerpt = self.selector(file, site.bodytag)
            print(excerpt)
            if title != '' and excerpt != '':
                job = Job(url, title, excerpt)
                print(job)
    
crawler = Jobparser()
urllib =[['dantri','dantri.com.vn','title', 'div.dt-news__sapo']]
websites=[]
for row in urllib:
    websites.append(Website(row[0], row[1], row[2], row[3]))
def get_news(link):
    crawler.parse(websites[0],link)   
link = 'https://beta.dantri.com.vn/viec-lam/ha-noi-ban-hanh-lo-trinh-giai-ngan-goi-62000-ty-dong-toi-5-nhom-doi-tuong-20200513073448996.htm'
get_news(link)