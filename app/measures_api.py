from bs4 import BeautifulSoup
from pywebcopy import save_webpage
from flask import Flask
from flask_pymongo import PyMongo


# READ Sicherheitshandbuch
with open("resources\www.sicherheitshandbuch.gv.at\www.sicherheitshandbuch.gv.at\95b74696__siha.php", "r", encoding='utf-8') as f:
    text= f.read()
soup = BeautifulSoup(text,'html.parser')

# relevant measures for Phishing -> can be updated by Inspecting "https://www.sicherheitshandbuch.gv.at/"
meas_list = ["topic_733","topic_747","topic_738","topic_741"]

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

# Connection to Database
app = Flask("__name__")
mongodb_client = PyMongo(app, uri="mongodb://localhost:27017/incidentwebapp_DB")
db = mongodb_client.db

# Pull Sicherheitshandbuch from URL
def pull_url():
    url = 'https://www.sicherheitshandbuch.gv.at/'
    save_webpage(url, project_folder='resources',)

# Update Measures in DB
def update_measures():
    db.measures.drop()
    print("got here")
    for m in meas_list:
        measure = find_byid(m) 
        db.measures.insert_one({'title': measure["title"], 'description': measure["description"], 'topic': measure["topic"]})


# TESTING
'''
print(update_measures())
'''


#BACKUP########################################### 

# HTML File-Reader Approach
'''
with open("resources\measures.html", "r", encoding='utf-8') as f:
    text= f.read()
soup = BeautifulSoup(text,'html.parser')
'''





