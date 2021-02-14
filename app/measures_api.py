import urllib.request
from bs4 import BeautifulSoup

# HTML File-Reader Approach
with open("resources\measures.html", "r", encoding='utf-8') as f:
    text= f.read()
soup = BeautifulSoup(text,'html.parser')

#print all Measurement Headlines
'''
pAll = soup.find_all('h3')
print(pAll)
'''
#print content of one chapter

#find by id
def find_byid():
    cid = soup.find(id="topic_738")
    cid_text = cid.get_text() 
    return cid_text






# URL Request Approach
'''
content = urllib.request.urlopen('https://www.sicherheitshandbuch.gv.at/#738')
read_content = content.read()
soup = BeautifulSoup(read_content,'html.parser')

# print all Tags
for tag in soup.find_all(True):
    print(tag.name)

'''



