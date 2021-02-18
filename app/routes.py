from flask import render_template, request, jsonify, url_for
from app import app, measures_api, mitre_api, evidence_api
from flask_pymongo import PyMongo
from werkzeug.utils import redirect


# Connection to Database
mongodb_client = PyMongo(app, uri="mongodb://localhost:27017/incidentwebapp_DB")
db = mongodb_client.db


@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Felix'}
    return render_template('index.html', title='Home', user=user)

@app.route('/technique')
def get_technique():
    # Get Technique directly from MITRE ATT&CK Server -> always up to date, but slow
    '''
    phishing_id = "T1566"
    technique = mitre_api.get_technique(id)
    '''
    # Get Technique from Database 
    technique = db.techniques.find_one({"name":"Phishing"})

    return render_template('technique.html', title='Choose Technique', technique = technique)

@app.route('/update')
def update_elements():
    mitre_api.update_techniques()
    return redirect(url_for('index'))

@app.route('/reviewmeas')
def taskgetall():
    global measurelist
    measurelist = measures_api.getall_topics()
    return render_template('review_meas.html', title='Review Measures', measurelist = measurelist )

@app.route('/reviewmeas', methods=['POST'])
def get_userinput():

    policylist = []
    for i in range(len(measurelist)):
        answer = {}
        check = measurelist[i]["topic"]
        answer["topic"] = measurelist[i]["topic"]
        answer["title"] = measurelist[i]["title"]
        answer["description"] = measurelist[i]["description"]
        answer["applied"] = request.form[check]
        policylist.append(answer)
     
    addmeas = request.form["addmeas"] 
    #Results Measures Analysis
    for pol in policylist: 
        if pol["applied"] == "FALSE":
            return render_template('policylack.html', title='Policy Lack', policylist = policylist, addmeas = addmeas)
        else:
            return render_template('policycoverage.html', title='Policy Coverage', policylist = policylist, addmeas = addmeas)

  
@app.route('/analysis')
def get_evidence():
    global evidencelist
    evidencelist = evidence_api.getall_evidences()
    return render_template('analysis.html', title='Analyse Evidence', evidencelist = evidencelist)
    

@app.route('/analysis', methods=['POST'])
def get_evidenceinput():
    answerlist = []
    for i in range(len(evidencelist)):
        answer = {}
        answer["id"] = evidencelist[i]["id"]
        answer["question"] = evidencelist[i]["question"]
        answer["violation"] = request.form[evidencelist[i]["id"]]
        answerlist.append(answer)

    ownanalysis = {}
    ownanalysis["ownquestion"] = request.form["addanalysis"]
    ownanalysis["violation"] = request.form["own_violation"]
    #Results Evidence Analysis
    one_violated = "FALSE"
    for ans in answerlist:
        if ans["violation"] == "TRUE":
            one_violated = "TRUE"

    if one_violated == "TRUE" or ownanalysis["violation"] == "TRUE":
        return render_template('pol_violated.html', title='Policy Violation', answerlist = answerlist, ownanalysis = ownanalysis)
    else:
        return render_template('pol_applied.html', title='Policy applied', answerlist = answerlist, ownanalysis = ownanalysis)


   