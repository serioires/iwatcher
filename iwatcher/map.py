from flask import (
    Blueprint, g, redirect, render_template, url_for, abort, request, make_response
)
from jinja2.exceptions import TemplateNotFound

from iwatcher.auth import login_required

bp = Blueprint('map', __name__)


@bp.before_app_request
def set_lang():
    lang = request.cookies.get('lang')
    if lang == None:
        g.lang = 'ru'
    else:
        g.lang = lang


@bp.route('/')
def index():
    return render_template('map/index.html')


@bp.route('/edit')
@login_required
def edit():
    return render_template('map/edit.html')


#переключение языков (используя cookie 'lang')
@bp.route('/en')
def en():
    resp = make_response(redirect(url_for('map.index')))
    resp.set_cookie('lang', 'en')
    return resp


@bp.route('/ru')
def ru():
    resp = make_response(redirect(url_for('map.index')))
    resp.set_cookie('lang', 'ru')
    return resp



@bp.route('/<page>')
def pages(page):
    try:
        if g.lang == 'en':
            return render_template('map/en/'+page+'.html')
        else:
            return render_template('map/'+page+'.html')
    except TemplateNotFound:
        return abort(404)
