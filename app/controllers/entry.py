from app import app, bcrypt, db
from app.models.user import User
from flask import Blueprint, render_template, request, redirect, url_for, flash

entry_route = Blueprint('entry', __name__)

@entry_route.route('/', methods=['GET'])
@entry_route.route('/login', methods=['GET'])
def login_form():
    return render_template('entry/login.html')


@entry_route.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template("entry/signup.html")
    elif request.method == 'POST':
        user = request.form
        if User.query.filter_by(username=user['username']).first():
            flash('Esse nome de usuário já está cadastrado!')
            return redirect(url_for('entry.signup'))
        else:
            new_user = User(user['username'], bcrypt.generate_password_hash(user['password']))
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('entry.login_form'))
