from app import bcrypt, db, login_manager, serializer, mail
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

            db.session.add(new_user)
            db.session.commit()

            token = serializer.dumps({'id':new_user.id, "email": new_user.email}, salt=SALT_SERIALIZER)

            url_confirm = url_for("entry.email_confirmation", token=token, _external=True)
            subject = f'Mensagem para confirmação do seu email {new_user.name}'
            body = f"""Acesse o link abaixo para confirmar seu endereço de email ou copie e cole no seu navegador
                {url_confirm}
                Obrigado por utilizar nossos serviços"""
            message = Message(subject=subject, sender=EMAIL_USERNAME, recipients=[new_user.email], body=body)
            mail.send(message)

            return redirect(url_for('entry.login'))
    return render_template("entry/signup.html", form=form)


@entry_route.route('/gerando-chave')
@login_required
def generate_token():
    token = serializer.dumps({'id':current_user.id, "email":current_user.email}, salt=SALT_SERIALIZER)

    url_confirm = url_for("entry.email_confirmation", token=token, _external=True)
    subject = f'Mensagem para confirmação do seu email {current_user.name}'
    body = f"""Acesse o link abaixo para confirmar seu endereço de email ou copie e cole no seu navegador
        {url_confirm}
        Obrigado por utilizar nossos serviços"""
    message = Message(subject=subject, sender=EMAIL_USERNAME, recipients=[current_user.email], body=body)
    mail.send(message)


    return redirect(url_for('entry.login'))

@entry_route.route('/confirmação-de-email/<token>')
def email_confirmation(token):
    try:
        user_info = serializer.loads(token, salt=SALT_SERIALIZER)

    except SignatureExpired:
        return render_template('entry/error-confirm.html', error=1)
    
    except  BadSignature:
        return render_template('entry/error-confirm.html', error=2)
    
    user = User.query.filter_by(email=user_info['email']).first()
    if user.email_confirmed:
        flash(f"Olá {user.name}, seu email já foi confirmado anteriormente!")
        return redirect(url_for('entry.login'))
    user.email_confirmed = True
    db.session.commit()
    flash(f"Olá {user.name}, seu email foi confirmado com sucesso!")
    return redirect(url_for('entry.login'))


@entry_route.route('/esqueci-a-senha', methods=['GET', 'POST'])
def request_password():
    if request.method == 'POST':
        if User.query.filter_by(email=request.form['email']).first():
            email = request.form['email']

            token = serializer.dumps(email, salt='email-token-confirmation')
            urlConfirm = url_for('entry.new_pwd', token=token, _method='GET', _external=True)

            body =  f"""Segue abaixo o link para recurepação de senha!
                        {urlConfirm}"""
            message = Message(subject='Mensagem com link para redefinição de senha',
                            recipients=[email],
                            body=body,  sender=EMAIL_USERNAME)
            
            mail.send(message)

            email = email.split('@')
            print(email)
            email = email[0][0:4] + "*"*(len(email[0])-4) + "@" +email[1]
            print(email)

            message = f'Email com link para redefinição de senha foi enviado para {email}'
        else:
            message = f"email '{request.form['email']} não é um email registrado!'"
        flash(message)
        return redirect(url_for('entry.request_password'))
    return render_template('entry/request-pwd.html')

@entry_route.route('/nova-senha/<token>', methods=['GET'])
@entry_route.route('/nova-senha', methods=['POST'])
def new_pwd(token=0):
    if request.method == 'GET':
        try:
            email = serializer.loads(token, salt='email-token-confirmation')
        except SignatureExpired:
            return "<h1>Token expirou!</h1>"
        except BadSignature:
            return "<h1>Token corrompido!</h1>"
        
        user = User.query.filter_by(email=email).first()
        return render_template('entry/new-pwd.html', user={'id':user.id, 'email':user.email})
    
    new_password = request.form['pwd']
    user = User.query.filter_by(email=request.form['email']).first()
    user.pwd = bcrypt.generate_password_hash(new_password)
    db.session.commit()
    if current_user:
        logout_user()
    return redirect(url_for('entry.login'))
 
