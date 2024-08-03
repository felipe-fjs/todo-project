from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import secrets

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex()
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost:3306/to_do_list'

db = SQLAlchemy(app)


from app.controllers.entry import entry_route
app.register_blueprint(entry_route)