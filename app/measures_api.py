import urllib.request
from bs4 import BeautifulSoup
import requests

# HTML File-Reader Approach
with open("resources\measures.html", "r", encoding='utf-8') as f:
    text= f.read()
soup = BeautifulSoup(text,'html.parser')

#print all Measurement Headlines
'''
pAll = soup.find_all('h3')
print(pAll)
'''

# put measure into python dictionary
def find_byid():
    cid = soup.find(id="topic_733")
    result = {}
    res_title = cid.find('h3')
    res_desc = cid.get_text()
    result["title"] = res_title.get_text() 
    result["description"] = res_desc
    return result 



# URL Request Approach
'''
content = urllib.request.urlopen('https://www.sicherheitshandbuch.gv.at/')
read_content = content.read()
soup = BeautifulSoup(read_content,'html.parser')
'''



