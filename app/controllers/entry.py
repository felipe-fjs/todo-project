from app import app
from flask import Blueprint, render_template

entry_route = Blueprint('entry', __name__)

@entry_route.route('/', methods=['GET'])
@entry_route.route('/login', methods=['GET'])
def login_form():
    return render_template('entry/login.html')

@entry_route.route('/signup')
def signup_form():
    return render_template("entry/signup.html")