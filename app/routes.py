from flask import render_template
from app import app, measures_api


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

@app.route('/taskone')
def taskonget():
    measureone = measures_api.find_byid()
    return render_template('taskone.html', title='Taskone',measureone = measureone)
