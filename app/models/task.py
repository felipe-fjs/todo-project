from app import db
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length


class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    content = db.Column(db.String(), nullable=False)
    user_id = db.Column(db.Integer(),  db.ForeignKey('users.id'),  nullable=False)
    pendent = db.Column(db.Boolean())

    def __init__(self, title, content, user_id):
        self.title = title
        self.content = content
        self.user_id = user_id
        self.pendent = 1
    
    def __repr__(self):
        return str({'id': self.id, 'title': self.title, 'content': self.content})

class TaskForm(FlaskForm):
    title = StringField('Título', validators=[DataRequired(), Length(min=10)])
    content = TextAreaField('Conteúdo', validators=[DataRequired(), Length(min=10)])
    submit = SubmitField()

