import functools
from flask import (
  Blueprint, flash, g, jsonify, make_response, redirect, render_template, request, session, url_for
)
import jwt

from flask_server.auth import login_required
bp = Blueprint('page_route', __name__)

@bp.route("/")
def index():
  #token = request.cookies.get('token')
  #if token: #check token exist
    #user_data = jwt.decode(token, "secret", algorithms=["HS256"])
    #if user_data: #check for sign data
      #return render_template('home.html')
  return render_template('index.html')
  #return "Hello"

@bp.route("/test_access")
@login_required
def test_access():
  return "test access"