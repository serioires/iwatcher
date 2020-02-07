import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import  check_password_hash, generate_password_hash

from iwatcher.models import User
from iwatcher.forms import LoginForm,RegistrationForm

bp = Blueprint('auth', __name__)#, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        error = None

        if User.get_or_none(User.username == form.username.data) is not None:
            error = 'User {} is already registered.'.format(form.username.data)
        else:
            q = User.insert(
                username=form.username.data,
                password=generate_password_hash(form.password.data))
            q.execute()
            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html', form=form)


@bp.route('/login', methods=('GET', 'POST'))
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        error = None
        user = User.get_or_none(User.username == form.username.data)

        if user is None or not check_password_hash(user.password, form.password.data):
            error = 'Incorrect username or password.'

        if error is None:
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for('index'))
        flash(error)
    return render_template('auth/login.html', form=form)


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = User.get_or_none(User.id == user_id)


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view
