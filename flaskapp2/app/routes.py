from app import app, db
from flask import render_template
from app.models import sdg_truncated as sdg

@app.route('/')
def index():
	return render_template('index.html',title='Home')

@app.route('/view_database', methods=['POST','GET'])
def view_database():
	records = sdg.query.all()
	return render_template('view_database.html', records=records)

