# https://flask.palletsprojects.com/en/2.3.x/patterns/sqlite3/
# https://flask.palletsprojects.com/en/1.1.x/patterns/sqlite3/
#from flask import Flask
from flask_sqlalchemy import SQLAlchemy
#from sqlalchemy import func
from flask import g
from .app_module import get_app

#app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project_app.sqlite" #src/instance/project_app.sqlite
# create the extension
#db = SQLAlchemy(app)
db = SQLAlchemy()

def get_db():
  return db

"""
def get_db():
  #db = getattr(g, '_databasea', None)
  #db = getattr(g, '_databasea') #nope
  
  app = get_app()
  db = None
  with app.app_context():
    db = getattr(g, '_database', None)
    print("DB:",db)
    if db is None:
      #db = g._database = sqlite3.connect(DATABASE)     
      app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project_app.sqlite" #src/instance/project_app.sqlite
      #db = g._database = db = SQLAlchemy(app)
      #db = g._database = SQLAlchemy(app)
      g._database = SQLAlchemy(app)
      db = g._database
      print("INIT DB!", db)
      #g._database = "test"
      #db = g._database
    else:
      print("FOUND DB!")
  return db
"""

def setup_db(app):
  app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project_app.sqlite"
  #db.app = app
  #db.init_app(app)
  return db

def get_SQLAlchemy():
  return db

def get_datatest():
  print("[[---------]]")
  #dbtest = getattr(g, '_datatest', None)#does not work...
  dbtest = g.get('_datatest')
  print("g: ", g)

  #for data in g:
    #print("data  ]]]", data)
  #if '_datatest' not in g:
    #g._datatest = "test2"
  #else:
    #print("FOUND VAR")

  #print("RESULT:: ", dbtest)
  #print("GET G:", g.get('_datatest'))
  
  if dbtest is None:
    print("NOT FOUND DATA!")
    g._datatest = "test"
    dbtest = g._datatest
  else:
    print("FOUND DATA!")
    #print("RESULT]] ", g._datatest)
  return dbtest
# note clean up var...