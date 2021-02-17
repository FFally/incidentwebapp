from flask import render_template, request
from app import app, measures_api,mitre_api


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
        answer["applied"] = request.form[check]
        policylist.append(answer)

    return render_template('result.html', title='result', policylist = policylist)