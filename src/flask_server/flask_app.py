from flask import Flask
from flask_sqlalchemy import SQLAlchemy

#init set up
app = Flask(__name__)
#app.config['SECRET_KEY'] = 'secret!'
#app.config['DEBUG'] = True #auto watch file and reload

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project_app.sqlite"
db = SQLAlchemy(app)

def get_db():
  return db

def get_app():
  return app