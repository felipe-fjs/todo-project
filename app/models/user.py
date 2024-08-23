from app import db, bcrypt
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField
from wtforms.validators import DataRequired, Length, EqualTo
from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    pwd = db.Column(db.String(128), nullable=False)
    email_confirmed = db.Column(db.Boolean)

    def __init__(self, name, email, pwd):
        self.name = name
        self.email = email
        self.pwd = pwd
        self.email_confirmed = False

    def __repr__(self) -> str:
        return f""" id = {self.id};
                    nome = {self.name};
                    email = {self.email};
                    email-fonrimado = {self.email_confirmed}
            """
    

    def verifyPass(self, pwd):
        return bcrypt.check_password_hash(self.pwd, pwd)


class UserLoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    pwd = PasswordField('Senha', validators=[DataRequired(), Length(min=8, max=16)])
    submit = SubmitField()


class UserSignupForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Length(min=6, max=100)])
    name = StringField('Seu nome', validators=[DataRequired(), Length(min=3, max=120)])
    pwd = PasswordField('Senha', validators=[DataRequired(), Length(min=8, max=16)])
    pwd_check = PasswordField(label='Repita a senha', validators=[DataRequired(), EqualTo('pwd')])
    submit = SubmitField()

