import os

from flask import Flask

from iwatcher.models import *
from iwatcher.admin import *

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'iwatcher.sqlite'),
        FLASK_ADMIN_SWATCH = 'cerulean',
    )
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass


    from . import auth
    app.register_blueprint(auth.bp)

    from . import map
    app.register_blueprint(map.bp)
    app.add_url_rule('/', endpoint='index')

    from . import api
    app.register_blueprint(api.bp)

#!!! всякие левые херы могут видеть файлоадминку!! Это не есть хорошо!!
    admin.init_app(app)


    return app
