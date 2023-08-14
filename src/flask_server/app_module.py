# https://flask.palletsprojects.com/en/1.1.x/patterns/sqlite3/
# https://stackoverflow.com/questions/15083967/when-should-flask-g-be-used
# https://stackoverflow.com/questions/26499428/flask-and-sqlalchemy-application-not-registered-on-instance
# 

from flask_sqlalchemy import SQLAlchemy
from .flask_app import get_app, get_db
#from .database import get_db
from . import auth
from . import page_route
from flask import g

def create_app():
  app = get_app()
  app.config['SECRET_KEY'] = 'secret!'
  app.config['DEBUG'] = True #auto watch file and reload

  #setup_db(app)
  

  #db = get_db()
  #db.create_all()

  app.register_blueprint(auth.bp)
  app.register_blueprint(page_route.bp)

  with app.app_context():
    print("init DB tables ???")
    db = get_db()
    db.create_all()

  #@app.route('/create_all')
  #def create_all():
    #db = get_db()
    #db.create_all()
    #return "create_all"

  return app

"""  

  #init datbase create table
  #with app.app_context():
    #data = get_datatest()
    #print("DATA g: ", data)
    #db = get_SQLAlchemy()
    #print("init db create table...")
    #db.create_all()

  #db = get_SQLAlchemy()

  #db2 = get_SQLAlchemy()

    #db2 = LocalProxy(get_datatest)

  #with app.app_context():
    #data = get_datatest()
    #print("DATA g: ", data)
  #db = get_SQLAlchemy()
    #print("init db create table...")
    #db.create_all()
  #app.run()

@app.route('/test')
  def test():
    #with app.app_context():
    data = get_datatest()
    print("DATA g: ", data)
    return ""
  @app.route('/test2')
  def test2():
    #with app.app_context():
    #data = get_datatest()
    #print("DATA g: ", data)
    if 'user' not in g:
      print("NOT FOUND...")
      g.user = 'test'
    print(g.user)

    return ""
 """