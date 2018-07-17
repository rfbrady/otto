from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy 
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap 

app = Flask(__name__)
app.config.from_object(Config)

#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/app.db'

db = SQLAlchemy(app)
migrate = Migrate(app, db)
bootstrap = Bootstrap(app)

from app import routes, db, models
