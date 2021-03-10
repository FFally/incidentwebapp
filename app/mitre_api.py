from stix2 import TAXIICollectionSource
from stix2 import Filter
from taxii2client.v20 import Collection # only specify v20 if your installed version is >= 2.0.0
from taxii2client.v20 import Server # only specify v20 if your installed version is >= 2.0.0
from flask import Flask, jsonify
from flask_pymongo import PyMongo


# Connection to MITRE ATT&CK Framework
server = Server("https://cti-taxii.mitre.org/taxii/")
api_root = server.api_roots[0]
collections = {
    "enterprise_attack": "95ecc380-afe9-11e4-9b6c-751b66dd541e",
    "mobile_attack": "2f669986-b40b-4423-b720-4396ca6a462b",
    "ics-attack": "02c3ef24-9cd4-48f3-a99f-b74ce24f1d34"
}

collection = Collection(f"https://cti-taxii.mitre.org/stix/collections/{collections['enterprise_attack']}/")
src = TAXIICollectionSource(collection)

# Get Technique by ID 
def get_technique(id):
    tec = src.query([ Filter("external_references.external_id", "=", id) ])[0]
    return tec

# Connection to Database
app = Flask("__name__")
mongodb_client = PyMongo(app, uri="mongodb://localhost:27017/incidentwebapp_DB")
db = mongodb_client.db
# List of techniques considered for Incidentwebapp -> can be updated by adding ATT&CK-ID of new Technique into List
techniques = ["T1566","T1134"]
# Upate Techniques in Database
def update_techniques():
    db.techniques.drop()
    for t in techniques:
        technique = get_technique(t) 
        db.techniques.insert_one({'name': technique["name"], 'description': technique["description"]})




# Only For Testing
'''
update_techniques()
print(phish['name']) #print name of technique phishing
print(phish['description']) #print description of technique phishing

'''