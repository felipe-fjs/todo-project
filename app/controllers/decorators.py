from flask import redirect, url_for, session, flash
from flask_login import current_user
from  functools import wraps

def email_confirmation_required(f):
    @wraps(f)
    def decored_function(*wargs,  **kwargs):
        if not current_user.email_confirmed:
            return redirect(url_for('confirm_mail'))
        return f(*wargs, **kwargs)
    return decored_function


def signup_required(f):
    @wraps(f)
    def decored_function(*wargs, **kwargs):
        if not session['new_user_id']:
            flash("Você precisa estar cadastrado para solicitar validação de email!")
            return redirect(url_for('entry.signup'))
        return f(*wargs, **kwargs)
    return decored_function
