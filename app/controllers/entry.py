from app import app, bcrypt, db, login_manager, serializer, mail
from app.models.user import User, UserSignupForm, UserLoginForm
from CONFIG import SALT_SERIALIZER, EMAIL_USERNAME
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from flask_mail import Message
from itsdangerous import BadSignature, SignatureExpired


entry_route = Blueprint('entry', __name__)


@login_manager.user_loader
def get_user(id_user):
    return User.query.filter_by(id=id_user).first()

@entry_route.route('/')
@entry_route.route('/login', methods=['GET', 'POST'])
def login():
    form = UserLoginForm()
    if request.method == 'POST':
        form = form.data
        if User.query.filter_by(email=form['email']).first():
            user = User.query.filter_by(email=form['email']).first()
            if user.verifyPass(form['pwd']):
                login_user(user)
                return redirect(url_for('tasks.home'))
            else:
                flash("Senha incorreta!")
                return redirect(url_for('entry.login'))
        else:
            flash('Não existe usuário cadastrado com esse Email!')
            return redirect(url_for('entry.login'))
    if current_user.is_authenticated:
        return redirect(url_for('tasks.home'))
    return render_template('entry/login.html', form=form)


@entry_route.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("entry.login"))


@entry_route.route('/signup', methods=['GET', 'POST'])
def signup():
    form = UserSignupForm()
    if request.method == 'POST':
        
        if User.query.filter_by(email=form.email.data).first():
            flash('Esse nome de usuário já está cadastrado!')
            return redirect(url_for('entry.signup'))
        else:
            
            new_user = User(form.name.data, form.email.data, bcrypt.generate_password_hash(form.pwd.data))
            
            print(new_user)

            token = serializer.dumps({'id': new_user.id,'email':new_user.email}, salt=SALT_SERIALIZER)

            url_confirm = url_for("entry.email_confirmation", token=token, _external=True)
            subject = f'Mensagem para confirmação do seu email {form.name.data}'
            body = f"""Acesse o link abaixo para confirmar seu endereço de email ou copie e cole no seu navegador
                {url_confirm}
                Obrigado por utilizar nossos serviços"""
            message = Message(subject=subject, sender=EMAIL_USERNAME, recipients=[new_user.email], body=body)
            mail.send(message)

            db.session.add(new_user)
            db.session.commit()

            return redirect(url_for('entry.login'))
    return render_template("entry/signup.html", form=form)


@entry_route.route('/confirmação-de-email/<token>')
def email_confirmation(token):
    try:
        user_info = serializer.loads(token, salt=SALT_SERIALIZER)
    except SignatureExpired:
        message = "A sua chave foi expiradoa click em [link] para gerar uma nova"
        return render_template('entry/error-confirm.html', message=message)
    except  BadSignature:
        message = "A seu chave está corrompida, copie e cole-a corretamente ou faça login e click na opção 'gerar nova chave'!"
        return render_template('entry/error-confirm.html', message=message)
    user = User.query.filter_by(id=user_info['id']).first()
    user.email_confirmed = True

    db.session.commit()
    flash(f"Olá {user.name}, seu email foi confirmado com sucesso!")
    return redirect(url_for('entry.login'))
