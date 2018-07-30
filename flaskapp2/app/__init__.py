from flask import Flask
from config import Config
import logging
from flask_sqlalchemy import SQLAlchemy 
from logging.handlers import RotatingFileHandler
import os

from flask_migrate import Migrate
from flask_bootstrap import Bootstrap 

app = Flask(__name__)
app.config.from_object(Config)

app.static_folder = 'static'

#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/app.db'

db = SQLAlchemy(app)
migrate = Migrate(app, db)
bootstrap = Bootstrap(app)

from app import routes, db, models


if not app.debug:
	if not os.path.exists('logs'):
		os.mkdir('logs')
	file_handler = RotatingFileHandler('logs/otto.log', maxBytes=10240, backupCount=10)
	file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s %(lineno)d ]'))
	file_handler.setLevel(logging.INFO)
	app.logger.addHandler(file_handler)
	app.logger.setLevel(logging.INFO)
	app.logger.info('otto startup')