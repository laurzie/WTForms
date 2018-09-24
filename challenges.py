#import statements go here
from flask import Flask, request, render_template, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import Required, Email
import requests
import json


app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
app.debug = True

@app.route('/')
def home():
    return "Hello, world!"

#create class to represent WTForm that inherits flask form
class ItunesForm(FlaskForm):
    artist_name = StringField('Enter the artist name?', validators=[Required()])
    num_results = IntegerField('Enter the number of results?', validators=[Required()])
    user_email = StringField('Enter your email?', validators=[Required(), Email(message=u'Invalid email address.')])
    submit = SubmitField('Submit')

@app.route('/itunes-form')
def itunes_form():
    simpleForm = ItunesForm()
    return render_template('itunes-form.html', form=simpleForm) # HINT : create itunes-form.html to represent the form defined in your class

@app.route('/itunes-result', methods = ['GET', 'POST'])
def itunes_result():
    #what code goes here?
    # HINT : create itunes-results.html to represent the results and return it
    form = ItunesForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        artist_name = form.artist_name.data
        num_results = form.num_results.data
    baseurl = "https://itunes.apple.com/search"
    params_diction = {}
    params_diction['term'] = artist_name
    params_diction['limit'] = num_results
    response = requests.get(baseurl, params= params_diction)
    text = response.text
    python_obj = json.loads(text)
    response_py = python_obj["results"]
    # for item in python_obj["results"]:
    #         track_name = item["trackName"]
    #         collection_name = item["collectionName"]
    flash('All fields are required!')
    return render_template('itunes-results.html', result_html = response_py) #this redirects you to itunes_form if there are errors

if __name__ == '__main__':
    app.run()
