from app import app, bcrypt, db, login_manager
from app.models.user import User
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, logout_user

entry_route = Blueprint('entry', __name__)


@login_manager.user_loader
def get_user(id_user):
    return User.query.filter_by(id=id_user).first()


@entry_route.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('entry/login.html')
    elif request.method == 'POST':
        if User.query.filter_by(username=request.form['username']).first():
            user = User.query.filter_by(username=request.form['username']).first()
            if user.verifyPass(request.form['pwd']):
                login_user(user)
                return redirect(url_for('entry.teste'))
            else:
                flash("Senha incorreta!")
                return redirect(url_for('entry.login'))
        else:
            flash('Não existe usuário cadastrado com esse username!')
            return redirect(url_for('entry.login'))


@entry_route.route('/logout', methods=['POST'])
def logout():
    logout_user()
    return jsonify(status='ok', url=url_for("entry.login"))


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
