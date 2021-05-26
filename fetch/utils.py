import re

def extract(link):
    '''''
    enter link and get the core url of link
    '''
    coreurl=link.split('/')[2]
    return coreurl

