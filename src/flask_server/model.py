#import functools
from sqlalchemy import func
#from .database import get_db
from .flask_app import get_db

db = get_db()

class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  alias = db.Column(db.String(32), unique=True, nullable=False)
  passphrase = db.Column(db.String(32), nullable=False)
  email = db.Column(db.String(128))
  role = db.Column(db.String(128), default='member')
  status = db.Column(db.String(128), default='offline')
  created = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())
  def __repr__(self):
    return '<User %r>' % self.alias