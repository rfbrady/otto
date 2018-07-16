from flask import Flask, render_template, request, jsonify
import json
from wtforms import Form, TextAreaField, validators
import sqlite3
import os
import numpy as np
import fastText as ft
import flask_excel as excel 
import pandas as pd

app = Flask(__name__)
excel.init_excel(app)
model = ft.load_model('sdg_model')

def classify(sentence):
	prediction =  model.predict(sentence, 5)
	ret = sentence[-6:] + "<br>"
	for i in range(5):
		ret = ret + "<strong>{}</strong>: {} ".format(prediction[0][i].replace("__label__",''), str(round(prediction[1][i],3)))
	ret = ret + "<br>"
	return ret





#print(*model.predict(" machinery designing machines", 1)[0])
class SDGForm(Form):
	description = TextAreaField('', [validators.DataRequired(), validators.length(min=15)])

#@app.route('/thanks', methods=['POST'])
#def feedback():
#	feedback = request.form['feedback_button']
#	sdg_description = request.form['description']


class HelloForm(Form):
	sayhello = TextAreaField('', [validators.DataRequired()])



@app.route('/', methods=['GET','POST'])
def index():
	form = SDGForm(request.form)
	return render_template('reviewform.html', form=form)

@app.route('/upload', methods=['GET','POST'])
def upload_file():
	if request.method == 'POST':
		ret = "<div>"
		sentence = ""
		#spreadsheet = pd.read_excel(request.get_array(field_name='file'))
		file_json = request.get_array(field_name='file')
		#df = pd.read_excel(data)
		for item in file_json:
			for i in item:
				sentence = sentence + str(i) + " "
			ret = ret + str(classify(sentence))
			ret = ret + "<br>"
			#sentence = sentence + "<br>"
			#label = str(classify(sentence))
			#ret = sentence + label + "<br>"
		#for obj in file_json:
		#	for record in obj:
		#ret = ret + "</div>"
		
		return ret

	return '''
	<!doctype html>
	<title>Upload an excel file</title>
	<h1>Excel file upload csv only</h1>
	<form action="" method=post enctype="multipart/form-data"><p>
	<input type=file name=file><input type=submit value=Upload>
	</form>
	'''

@app.route("/download", methods=['GET'])
def download_file():
	return excel.make_response_from_array([[1,2], [3,4]], "csv")

@app.route("/export", methods=['GET'])
def export_records():
	return excel.make_response_from_array([[1,2], [3,4]], "csv", file_name="export_data")

@app.route('/results', methods=['GET','POST'])
def results():
	form = SDGForm(request.form)
	if request.method == 'POST' and form.validate():
		sdg_description = request.form['description']
		label = classify(sdg_description)
		return render_template('results.html', content=sdg_description, prediction=label)
	return render_template('reviewform.html',form=form)


if __name__ == '__main__':
	app.run(debug=True)