from flask import Flask
from flask_pymongo import PyMongo

# relevant evidence question
evidencelist = ["Violation identified from analysis of User Ticket", "Violation identified from analysis of relevant collected system data","Violation identified from analysis of Incident Reports"]


# get all evidence questions

def getall_evidences():
    resultlist = []
    a = 0
    for ev in evidencelist: 
         a += 1
         evidence_obj = {}
         evidence_obj["id"] = "ev" + str(a)
         evidence_obj["question"] = ev
         resultlist.append(evidence_obj)
    return resultlist


# Only For Testing
#print (getall_evidences()) 


# Connection to Database
app = Flask("__name__")
mongodb_client = PyMongo(app, uri="mongodb://localhost:27017/incidentwebapp_DB")
db = mongodb_client.db