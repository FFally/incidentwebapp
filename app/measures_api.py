#import urllib
from bs4 import BeautifulSoup
#import requests
#import urllib.request
#from pywebcopy import WebPage, config, save_website
import pywebcopy


#> a .html file would be saved at

# HTML File-Reader Approach
with open("resources\measures.html", "r", encoding='utf-8') as f:
    text= f.read()
soup = BeautifulSoup(text,'html.parser')

# relevant measures for Phishing -> can be updated by Inspecting "https://www.sicherheitshandbuch.gv.at/"
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
url = 'https://www.sicherheitshandbuch.gv.at/'
download_folder = 'C:/Users/Felix/Downloads/'  

pywebcopy.save_website(url, download_folder)

#HTML = open('resources\test.html').read()
base_url = 'https://www.sicherheitshandbuch.gv.at' # used as a base for downloading imgs, css, js files.
project_folder = '/saved_pages/'
config.setup_config(base_url, project_folder)

wp = WebPage()
wp.get(url)
#wp.set_source(HTML)
#wp.url = base_url
wp.save()
'''



'''
urllib.request.urlretrieve('https://www.sicherheitshandbuch.gv.at/', 'C:/Users/Felix/Downloads/test.html')
content = urllib.request.urlopen('https://www.sicherheitshandbuch.gv.at/')
read_content = content.read()
soup = BeautifulSoup(read_content,'html.parser')
'''



