from bs4 import BeautifulSoup
from pywebcopy import save_webpage, save_website, config
from flask import Flask
from flask_pymongo import PyMongo


# READ Sicherheitshandbuch
with open("resources\www.sicherheitshandbuch.gv.at\www.sicherheitshandbuch.gv.at\95b74696__siha.php", "r", encoding='utf-8') as f:
    text= f.read()
soup = BeautifulSoup(text,'html.parser')
soup2 = BeautifulSoup(text,'html.parser')


# relevant measures for General -> can be updated by Inspecting "https://www.sicherheitshandbuch.gv.at/"
meas_list1 = ["topic_733", "topic_734","topic_738", "topic_739", "topic_741", "topic_743", "topic_747", "topic_748", "topic_749", "topic_158", "topic_754", "topic_755", "topic_757"]
# relevant measures for Phishing -> can be updated by Inspecting "https://www.sicherheitshandbuch.gv.at/"
meas_list2 = ["topic_865", "topic_430", "topic_868", "topic_869", "topic_883", "topic_893", "topic_900", "topic_3038", "topic_909", "topic_911", "topic_20201201", "topic_20201202", "topic_20201203", "topic_20201204", "topic_20201205"]
# put measure into python dictionary

def find_byid(topic):
    result = {}
    cid = soup.find(id=topic)
    
    result["title"] = cid.find('h3').get_text()

    des = soup2.find(id=topic)
    for h3 in des('h3'):
        h3.decompose()
    
    for a in des.findAll('a'):
        a.replaceWithChildren()
    
    result["description"] = des.prettify()
    result["topic"] = topic
  
    return result 


# Connection to Database
app = Flask("__name__")
mongodb_client = PyMongo(app, uri="mongodb://localhost:27017/incidentwebapp_DB")
db = mongodb_client.db

# Pull Sicherheitshandbuch from URL
def pull_url():
    
    url = 'https://www.sicherheitshandbuch.gv.at/'
    kwargs = {
     'bypass_robots':False,
     'debug': False,
     'project_folder': 'resources',
     'load_css': False,
     'load_images': False,
     'load_javascript': False,
     'over_write': True,
     'zip_project_folder': False

     }

    save_webpage(url,**kwargs)


# Update Measures in DB
def update_measures(choice):
    db.measures.drop()

    if choice == "Phishing":
        meas_list = meas_list2
    elif choice == "Access Token Manipulation Mitigation":
        meas_list = meas_list1

    for m in meas_list:
        measure = find_byid(m) 
        db.measures.insert_one({'title': measure["title"], 'description': measure["description"], 'topic': measure["topic"]})
 
# get whole chapter
def get_chapter(chapterid): 
    resultlist = [] 
    #find chapter
    cid = soup.find(id=chapterid)
    for topic in cid(class_="topic"):
        resultlist.append(find_byid(topic['id']))
    
    for r in resultlist: 
        db.chapter.insert_one(({'title': r["title"], 'description': r["description"], 'topic': r["topic"]}))

# get SHB Structure
def get_shbindex():
    resultlist = []
    cid = soup
    #find all chapters 
    for chapter in cid(class_="chapter"):
        #print(chapter['id'])
        print(chapter.h1.get_text())
        #find all sections
        for section in chapter(class_="section"):
            print(section.h2.get_text())
    

# TESTING

#print(pull_url())
#print(update_measures())
#print(find_byid("topic_733"))

#BACKUP########################################### 

# HTML File-Reader Approach
'''
with open("resources\measures.html", "r", encoding='utf-8') as f:
    text= f.read()
soup = BeautifulSoup(text,'html.parser')
'''



# old put to find_byid and put to string
'''
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
'''

# return measures in list of dictionaries
'''
def getall_topics():
    resultlist = []
    for x in meas_list: 
        resultlist.append(find_byid(x))
    return resultlist
'''