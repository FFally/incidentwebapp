from flask import render_template
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

@app.route('/taskzero')
def taskzeroget():
    technique = mitre_api.get_technique()
    return render_template('taskzero.html', title='Taskzero', technique = technique)


@app.route('/taskone')
def taskonget():
    measureone = measures_api.find_byid()
    return render_template('taskone.html', title='Taskone', measureone = measureone)

@app.route('/tasktry')
def taskgetall():
    measurelist = measures_api.getall_topics()
    return render_template('tasktry.html', title='Tasktry', measurelist = measurelist )

@app.route('/policyresult', methods=['GET', 'POST'])
def showresultone():
    result = request.form['applied']
    print(result)
    return result