from flask import Flask
import os


app = Flask(__name__)

# Set up configuration
app.config['SECRET_KEY'] = os.environ['FLASK_SECRET_KEY']
app.config['DEBUG'] = True if os.environ['FLASK_DEBUG'] == '1' else False


# Set up database
from flask_sqlalchemy import SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres@jsdatabase/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from flask_migrate import Migrate
migrate = Migrate(app, db)


# Set up css file creation, template utility functions,
# and general content pages
from app import assets, jinja_filters


# Register blog
from app.blog import blog
app.register_blueprint(blog, url_prefix='/blog')


# set up user login and admin area
import flask_login as login
login_manager = login.LoginManager()
login_manager.init_app(app)

class User:
    def __init__(self, user):
        self.user = user

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return self.user.id


from app import models

@login_manager.user_loader
def load_user(user_id):
    user = models.User.query.filter_by(id=int(user_id)).first()
    return User(user)


from flask_admin import Admin
from app.admin import MyAdminIndexView
admin = Admin(app, url='/admin', index_view=MyAdminIndexView(),
              base_template='my_admin_master.html')
from app.blog import admin

from app import views

