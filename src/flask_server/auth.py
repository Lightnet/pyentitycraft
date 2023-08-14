import functools
from flask import (
  Blueprint, flash, g, jsonify, make_response, redirect, render_template, request, session, url_for
)
import jwt
#from .database import get_db
from .flask_app import get_db
from .model import User

#bp = Blueprint('auth', __name__, url_prefix='/auth')
bp = Blueprint('auth', __name__)

#================================================
# SIGNIN
#================================================
# Page Html
@bp.route('/signin')
def html_sign_in():
  return render_template('auth/signin.html')

# AUTH SIGNIN
@bp.route('/api/signin', methods = ['POST'])
def auth_signin():
  user = request.get_json()
  db = get_db()
  userData = db.session.execute(db.select(User).filter_by(alias=user['alias'])).fetchone()
  print(user)#need to check string
  data ={}
  if userData:
    print("User Exist!")
    print("userData: ", userData)
    print(userData[0].passphrase)
    if userData[0].passphrase == user['passphrase']:
      data['api'] = "PASS"
      token = jwt.encode({"alias": userData[0].alias, 'date':"NOne"}, "secret", algorithm="HS256")

      resp = make_response(jsonify({"alias":user['alias'],"api":"PASS"}))
      resp.set_cookie('token', token)
      return resp
    else:
      data['api'] = "DENIED"
      return jsonify(data)
  else:
    print("FAIL")
    data['api'] = "FAIL"
    return jsonify(data)

#================================================
# SIGNUP
#================================================
# Page Html
@bp.route('/signup')
def html_signup():
  return render_template('auth/signup.html')

# Auth signup
@bp.route('/api/signup', methods = ['POST'])
def auth_signup():
  user = request.get_json()
  #print(user)
  if not user['alias'] or not user['alias']:
    return jsonify({"api":"EMPTY"})
  print("Alias: ",user['alias'])
  print("Passphrase: ",user['passphrase'])
  #user data
  data = {}
  #check if user exist
  db = get_db()
  userData = db.session.execute(db.select(User).filter_by(alias=user['alias'])).fetchone()
  if userData:#if exist return message exist
    print("User Exist!")
    #print("userData: ", userData)
    #print("userData: ", userData[0].alias)
    #print("userData: ", userData[0].passphrase)
    data['api'] = "EXIST"
  else:
    #CREATE USER
    print("NOT FOUND...")
    new_user = User(
      alias=user['alias'],
      passphrase=user['passphrase']
    )
    db.session.add(new_user) #query
    db.session.commit() #update
    data['api'] = "CREATED"

  #print("result data: ", data)
  #return jsonify({"msg":"hello"})
  return jsonify(data)

#================================================
# SIGNOUT
#================================================
@bp.route('/signout')
def html_signout():
  return render_template('auth/signout.html')

@bp.route('/api/signout', methods=['POST'])
def auth_signout():

  token = request.cookies.get('token')
  if token:
    user_data = jwt.decode(token, "secret", algorithms=["HS256"])
    resp = None
    if user_data:
      #print("FOUND TOKEN:", request.cookies.get('token'))
      resp = make_response(jsonify({'api':'logout'}))
    else:
      resp = make_response(jsonify({'api':'NONE'}))
    resp.set_cookie('token', '', expires=0)
    return resp
  else:
    return jsonify({'api':'NONE'})
#================================================
# RECOVERY
#================================================
@bp.route('/recovery')
def html_recovery():
  return render_template('auth/recovery.html')

@bp.route('/api/recovery', methods=['POST'])
def auth_recovery():
  return jsonify({'api':'NONE'})

#================================================
# Login check middle ware
# @app.route(...)
# @login_required
#def test_foo():
#  return "access bar"
#================================================
def login_required(view):
  @functools.wraps(view)
  def wrapped_view(**kwargs):
    print("CHECK LOGIN REQUIRED")
    print(g)
    #if g.user is None:
      #return redirect(url_for('/login'))
      ##return redirect(url_for('auth.login'))
    return view(**kwargs)
  return wrapped_view

#================================================
# Testing...
#================================================
@bp.route('/api/token')
def get_token():
  print("nest")
  token = request.cookies.get('token')
  print("token: ", token)
  user_data = jwt.decode(token, "secret", algorithms=["HS256"])
  print("user_data: ", user_data)
  return "token"

