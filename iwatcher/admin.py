from flask import abort

from flask_admin import *
from flask_admin.contrib.peewee import ModelView
from flask_admin.contrib.fileadmin import FileAdmin
from flask_admin.contrib import peewee
from flask_admin.form import SecureForm

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


class MapModelView(peewee.ModelView):
    can_edit = False
    form_base_class = SecureForm
    def is_accessible(self):
        if g.user is None:
            return False
        else:
            return g.user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return abort(404)


class UserView(MapModelView):
    column_exclude_list = ['password',]
    column_searchable_list = ['username']


class CameraView(MapModelView):
    column_exclude_list = ['id',]


class UReportView(MapModelView):
    column_exclude_list = ['id',]
    

admin = Admin(
    #app,
    #url='/topsecret',
    #name='iwatcher',
    template_mode='bootstrap3',
    index_view=TopSecretIndex(url='/topsecret'),)

import os.path as op

path = op.join(op.dirname(__file__), 'static')
admin.add_view(TheStorage(path, '/main/', name='Main'))
admin.add_view(UserView(User))
admin.add_view(CameraView(Camera))
admin.add_view(MapModelView(UCcheck))
admin.add_view(UReportView(UReport))
