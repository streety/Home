import os
import bcrypt
from wtforms import form, fields, validators


class LoginForm(form.Form):
    """ Login form with built in validation of password against
    environment variable as only single admin user is expected. """

    login = fields.TextField(validators=[validators.required()])
    password = fields.PasswordField(validators=[validators.required()])

    def validate_login(self, field):
        if self.login.data != os.environ['FLASK_ADMIN_USER']:
            raise validators.ValidationError('Invalid user')

        if bcrypt.hashpw(self.password.data.encode('utf-8'),
                    os.environ['FLASK_ADMIN_PASSWORD'].encode('utf-8')) != \
                os.environ['FLASK_ADMIN_PASSWORD'].encode('utf-8'):
            raise validators.ValidationError('Invalid password')

    def get_user(self):
        user = User()
        return user


class User(object):
    """ Dummy user class """

    @property
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return 1
