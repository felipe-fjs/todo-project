from flask import Flask

import secrets

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex()


from app.controllers.entry import entry_route
app.register_blueprint(entry_route)