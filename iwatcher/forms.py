from datetime import timedelta

from wtforms import Form, StringField, PasswordField, validators
from wtforms.csrf.session import SessionCSRF
from flask import session

CSRF_SECRET_KEY = b'gwrt23r332e33t2gs23tt23t'


class BaseForm(Form):
    class Meta:
        csrf = True
        csrf_class = SessionCSRF
        csrf_secret = CSRF_SECRET_KEY
        csrf_time_limit = timedelta(minutes=20)
        @property
        def csrf_context(self):
            return session

class RegistrationForm(BaseForm):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.Length(min=8, max=25),
        validators.EqualTo('confirm', message='Password must match')
    ])
    confirm = PasswordField('RepeatPassword')


class LoginForm(BaseForm):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    password = PasswordField('Password', [validators.DataRequired()])
