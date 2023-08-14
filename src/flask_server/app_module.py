# https://flask.palletsprojects.com/en/1.1.x/patterns/sqlite3/
# https://stackoverflow.com/questions/15083967/when-should-flask-g-be-used
# https://stackoverflow.com/questions/26499428/flask-and-sqlalchemy-application-not-registered-on-instance
# 

from flask_sqlalchemy import SQLAlchemy
from .flask_app import get_app, get_db
from . import auth
from . import page_route
from flask import g

def create_app():
  app = get_app()
  app.config['SECRET_KEY'] = 'secret!'
  app.config['DEBUG'] = True #auto watch file and reload

  app.register_blueprint(auth.bp)
  app.register_blueprint(page_route.bp)

  with app.app_context():
    print("init DB tables ???")
    db = get_db()
    db.create_all()

  return app