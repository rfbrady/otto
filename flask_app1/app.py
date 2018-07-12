from flask import Flask, render_template, request
from wtforms import Form, TextAreaField, validators
<<<<<<< HEAD
import sqlite3
import os
import numpy as np
import fastText as ft

app = Flask(__name__)

cur_dir = os.path.dirname(__file__)
model = ft.load_model('truncated_model')

def classify(sentence):
	return model.predict(sentence, 2)


#print(*model.predict(" machinery designing machines", 1)[0])
class SDGForm(Form):
	description = TextAreaField('', [validators.DataRequired(), validators.length(min=15)])


@app.route('/', methods=['GET','POST'])
def index():
	form = SDGForm(request.form)
	return render_template('reviewform.html', form=form)

@app.route('/results', methods=['GET','POST'])
def results():
	form = SDGForm(request.form)
	if request.method == 'POST' and form.validate():
		sdg_description = request.form['description']
		label = classify(sdg_description)
		return render_template('results.html', content=sdg_description, prediction=label)
	return render_template('reviewform.html',form=form)

#@app.route('/thanks', methods=['POST'])
#def feedback():
#	feedback = request.form['feedback_button']
#	sdg_description = request.form['description']


=======

app = Flask(__name__)

class HelloForm(Form):
	sayhello = TextAreaField('', [validators.DataRequired()])


@app.route('/')
def index():
	form = HelloForm(request.form)
	return render_template('first_app.html', form=form)
>>>>>>> 2e61322c3a135bf5cfb4dac034896842d90dc93b

@app.route('/hello', methods=['POST'])
def hello():
	form = HelloForm(request.form)
	if request.method == 'POST' and form.validate():
		name = request.form['sayhello']
		return render_template('hello.html', name= name)
	return render_template('first_app.html', form = form)

if __name__ == '__main__':
	app.run(debug=True)