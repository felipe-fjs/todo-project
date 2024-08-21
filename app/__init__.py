from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from itsdangerous import URLSafeTimedSerializer
import secrets

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex()
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost:3306/to_do_list'

@app.errorhandler(404)
def rota_invalida(e):
    return render_template('not_found.html')

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
mail = Mail(app)
serializer = URLSafeTimedSerializer(app.config.get('SECRET_KEY'))


login_manager.login_view = 'entry.login'
login_manager.login_message = 'Você precisa está logado para acessar o sistema!'

from app.controllers.entry import entry_route
app.register_blueprint(entry_route)

from app.controllers.taks import task_route
app.register_blueprint(task_route, url_prefix='/task')
