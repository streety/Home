from app import admin, db

from app.admin import MyModelView
from app.blog import models as bm

from flask_admin.contrib.fileadmin import FileAdmin
import os.path as op

class PostView(MyModelView):
    form_excluded_columns = ['comments']

admin.add_view(PostView(bm.Post, db.session))
admin.add_view(MyModelView(bm.Tag, db.session))
admin.add_view(MyModelView(bm.Comment, db.session))

path = op.join(op.dirname(__file__), '../media')
admin.add_view(FileAdmin(path, '/media/', name='Media Files'))
