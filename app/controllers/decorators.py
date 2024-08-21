from flask import redirect, url_for
from flask_login import current_user
from  functools import wraps

def email_confirmation_required(f):
    @wraps(f)
    def decored_function(*wargs,  **kwargs):
        if not current_user.email_confirmed:
            return redirect(url_for('confirm_mail'))
        return f(*wargs, **kwargs)
    return decored_function
