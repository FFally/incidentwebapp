from flask import Flask, render_template, request, jsonify, url_for
from app import app, measures_api, mitre_api, evidence_api, cases_api
from flask_pymongo import PyMongo
from werkzeug.utils import redirect


# Connection to Database
'''
mongodb_client = PyMongo(app, uri="mongodb://localhost:27017/incidentwebapp_DB")
db = mongodb_client.db
'''

# PyMongo Connection Approach
app.config["MONGO_URI"] = "mongodb://localhost:27017/incidentwebapp_DB"
mongo = PyMongo(app)


@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Felix'}
    mongo.db.techniques.update_many({}, {"$set": {'chosen': False}})
    return render_template('index.html', title='Home', user=user)


@app.route('/updatetechniques')
def update_tec():
    mitre_api.update_techniques()
    return redirect(url_for('index'))
    

@app.route('/updatemeasures')
def update_meas():
    #measures_api.pull_url()
    
    return redirect(url_for('index'))

@app.route('/technique', methods=['GET', 'POST'])
def get_technique():
    

    if request.method == 'GET':
        # Get Technique directly from MITRE ATT&CK Server -> always up to date, but slow
        '''
        phishing_id = "T1566"
        technique = mitre_api.get_technique(id)
        '''
        # Update and Get all available Techniques from Database
        
        techniques = list(mongo.db.techniques.find({}))
        return render_template('technique.html', title='Choose Technique', techniques = techniques)   
    elif request.method == 'POST':
        tec = request.form["answer"]
        dbres = mongo.db.techniques.find_one_and_update({"name": tec}, {"$set": {'chosen': True}})
        
        #load relevant measures set 
        choice = mongo.db.techniques.find_one({"chosen": True})
        #load measures for chosen technique
        measures_api.update_measures(choice["name"])

        return redirect(url_for('select_case'))

     


@app.route('/case')
def select_case():
    return render_template('cases.html', title='Choose TestCase')

@app.route('/case', methods=['POST'])
def get_case():
    global testset

    if "testset_1" in request.form:
        testset = cases_api.get_testset_1()
        
    elif "testset_2" in request.form:
        testset = cases_api.get_testset_2()

    elif "testset_3" in request.form:
        testset = cases_api.get_testset_3()
    
    #DELETE FROM DB AND INSERT NEW
    mongo.db.testset.drop()
    mongo.db.testset.insert(testset)
    return redirect(url_for('taskgetall'))


@app.route('/reviewmeas')
def taskgetall():
    #old Approach with Database
    '''
    global measurelist
    measurelist = measures_api.getall_topics()
    '''

    measurelist = list(mongo.db.measures.find({}))    
    return render_template('review_meas.html', title='Review Measures', measurelist = measurelist)

@app.route('/reviewmeas', methods=['POST'])
def get_userinput():

    #old_Approach_without database
    '''
    policylist = []
    
    for i in range(len(measurelist)):
        answer = {}

        apl = measurelist[i]["topic"]
        answer["topic"] = measurelist[i]["topic"]
        answer["title"] = measurelist[i]["title"]
        answer["description"] = measurelist[i]["description"]
        answer["relevant"] = request.form["rel_"+str(apl)] 
        answer["applied"] = request.form[apl]
        policylist.append(answer)
     '''
    dbmeasurelist = list(mongo.db.measures.find({}))

    for i in range(len(dbmeasurelist)):
        topic = dbmeasurelist[i]["topic"]
        rel = request.form["rel_"+str(topic)] 
        apl = request.form[topic]
        mongo.db.measures.find_one_and_update({"topic": topic}, {"$set": {'applied': apl, 'relevant': rel}})

    policylist = list(mongo.db.measures.find({}))

    addmeas = request.form["addmeas"] 
    #Results Measures Analysis
    one_applied = "TRUE"
    for pol in policylist: 
        if pol["applied"] == "FALSE":
            one_applied = "FALSE"
    if one_applied == "FALSE":
        return render_template('policylack.html', title='Policy Lack', policylist = policylist, addmeas = addmeas)
    else:
        return render_template('policycoverage.html', title='Policy Coverage', policylist = policylist, addmeas = addmeas)


@app.route('/inspect')
def inspect_evidence():
    testset = list(mongo.db.testset.find({}, {'_id': False}))
    return render_template('inspect.html', title='Inspect Evidence', testset = testset)



@app.route('/analysis')
def get_evidence():
    global evidencelist
    evidencelist = evidence_api.getall_evidences()
    testset = list(mongo.db.testset.find({}, {'_id': False}))
    return render_template('analysis.html', title='Analyse Evidence', evidencelist = evidencelist, testset = testset)
    

@app.route('/analysis', methods=['POST'])
def get_evidenceinput():
    answerlist = []
    for i in range(len(evidencelist)):
        answer = {}
        answer["id"] = evidencelist[i]["id"]
        answer["question"] = evidencelist[i]["question"]
        answer["violation"] = request.form[evidencelist[i]["id"]]
        answerlist.append(answer)

    print(answerlist)
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
        technique = mongo.db.techniques.find_one({'chosen': True})
        policylist = list(mongo.db.measures.find({}))
        return render_template('pol_applied.html', title='Policy applied', answerlist = answerlist, ownanalysis = ownanalysis, technique = technique, policylist = policylist)


@app.route('/end', methods=['GET'])
def get_earlyend():
    return render_template('earlyend.html', title='End')