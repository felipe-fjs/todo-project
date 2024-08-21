from app import bcrypt, db, login_manager
from app.models.user import User, UserSignupForm, UserLoginForm
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user

entry_route = Blueprint('entry', __name__)


@login_manager.user_loader
def get_user(id_user):
    return User.query.filter_by(id=id_user).first()

@entry_route.route('/')
@entry_route.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        form = UserLoginForm()
        if User.query.filter_by(email=form['email']).first():
            user = User.query.filter_by(email=form['email']).first()
            if user.verifyPass(form['pwd']):
                login_user(user)
                return redirect(url_for('tasks.home'))
            else:
                flash("Senha incorreta!")
                return redirect(url_for('entry.login'))
        else:
            flash('Não existe usuário cadastrado com esse username!')
            return redirect(url_for('entry.login'))
    return render_template('entry/login.html', form=form)


@entry_route.route('/logout')
def logout():
    logout_user()
    return redirect(url_for("entry.login"))


@entry_route.route('/signup', methods=['GET', 'POST'])
def signup():
    form = UserSignupForm()
    if request.method == 'POST':
        user = form.data
        if User.query.filter_by(email=user['email']).first():
            flash('Esse nome de usuário já está cadastrado!')
            return redirect(url_for('entry.signup'))
        else:
            new_user = User(user['nome'], user['email'], bcrypt.generate_password_hash(user['pwd']))
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('entry.login_form'))
    return render_template("entry/signup.html", form=form)
