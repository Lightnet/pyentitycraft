from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
#from .auth import login_required
#import jwt
from flask import g

#init set up
app = Flask(__name__)
#app.config['SECRET_KEY'] = 'secret!'
#app.config['DEBUG'] = True #auto watch file and reload

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project_app.sqlite"
db = SQLAlchemy(app)
#db = SQLAlchemy()
#db.init_app(app)
#db = SQLAlchemy()

def get_db():
  return db

def get_app():
  """db = getattr(g, '_projectapp', None)
  if db is None:
    #app = Flask(__name__)
    db = g._projectapp = db = app
  return db"""
  return app