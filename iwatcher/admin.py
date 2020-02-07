from flask import abort

from flask_admin import *
from flask_admin.contrib.peewee import ModelView
from flask_admin.contrib.fileadmin import FileAdmin

from iwatcher.models import *
from iwatcher.auth import login_required

class TheStorage(FileAdmin):
    form_base_class = SecureForm
    def is_accessible(self):
        if g.user is None:
            return False
        else:
            return g.user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return abort(404)

class TopSecretIndex(AdminIndexView):
    form_base_class = SecureForm
    def is_accessible(self):
        if g.user is None:
            return False
        else:
            return g.user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return abort(404)


class BlogModelView(peewee.ModelView):
    form_base_class = SecureForm
    def is_accessible(self):
        if g.user is None:
            return False
        else:
            return g.user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return abort(404)


admin = Admin(
    #app,
    #url='/topsecret',
    #name='iwatcher',
    template_mode='bootstrap3',
    index_view=TopSecretIndex(url='/topsecret'),)

import os.path as op

path = op.join(op.dirname(__file__), 'static')
admin.add_view(TheStorage(path, '/main/', name='Main'))
admin.add_view(BlogModelView(User))
admin.add_view(BlogModelView(Camera))
