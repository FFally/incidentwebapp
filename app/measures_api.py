import urllib.request
from bs4 import BeautifulSoup
import requests

# HTML File-Reader Approach
with open("resources\measures.html", "r", encoding='utf-8') as f:
    text= f.read()
soup = BeautifulSoup(text,'html.parser')

#print all Measures Headlines
'''
pAll = soup.find_all('h3')
print(pAll)
'''
# relevant measures 
meas_list = ["topic_733","topic_747","topic_738"]

# put measure into python dictionary
def find_byid(topic):
    result = {}
    res_desc = ""
    cid = soup.find(id=topic)
    res_title = cid.find('h3').get_text()
    for i in cid.find_all(["div","li"]):
        part = i.get_text()
        res_desc += part 
    result["title"] = res_title
    result["description"] = res_desc
    result["topic"] = topic
    return result 

# return measures in list of dictionaries
def getall_topics():
    resultlist = []
    for x in meas_list: 
        resultlist.append(find_byid(x))
    return resultlist





# URL Request Approach
'''
content = urllib.request.urlopen('https://www.sicherheitshandbuch.gv.at/')
read_content = content.read()
soup = BeautifulSoup(read_content,'html.parser')
'''



