from flask import render_template, request
from app import app, measures_api, mitre_api, evidence_api


@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Felix'}
    posts = [
        {
            'author': {'username': 'Q1'},
            'body': 'Has measurement A been applied?'
        },
        {
            'author': {'username': 'Q2'},
            'body': 'Has measurement B been applied?'
        }
    ]
    return render_template('index.html', title='Home', user=user, posts=posts)

@app.route('/technique')
def taskzeroget():
    technique = mitre_api.get_technique()
    return render_template('technique.html', title='Choose Technique', technique = technique)


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
    #Results:
    for pol in policylist: 
        if pol["applied"] == "FALSE":
            return render_template('policylack.html', title='Policy Lack', policylist = policylist, addmeas = addmeas)
        else:
            return render_template('result.html', title='result', policylist = policylist, addmeas = addmeas)

  
@app.route('/analyze')
def get_evidence():
    global evidencelist
    evidencelist = evidence_api.getall_evidences()
    return render_template('evidence.html', title='Analyze Evidence', evidencelist = evidencelist)
    

@app.route('/analyze', methods=['POST'])
def get_evidenceinput():
    answerlist = []
    for i in range(len(evidencelist)):
        answer = {}
        answer["id"] = evidencelist[i]["id"]
        answer["question"] = evidencelist[i]["question"]
        answer["applied"] = request.form[evidencelist[i]["id"]]
        answerlist.append(answer)

    ownmeas = request.form["addanalyzation"]

    #Results
    for ans in answerlist:
        if ans["applied"] == "FALSE":
            return render_template('positive.html', title='Policy applied', answerlist = answerlist, ownmeas = ownmeas)
        else:
            return render_template('negative.html', title='Policy Violation', answerlist = answerlist, ownmeas = ownmeas)
        


   