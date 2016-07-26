import pyramid.httpexceptions as http
from pyramid.view import view_config, view_defaults
from pyramid.security import remember, forget

from auth_app.model.auth import UserMgr


@view_defaults(route_name="login", renderer="login.mako")
class LoginViews(object):

    def __init__(self, request):
        self.request = request
        self.login_form = LoginForm(request.POST)

        if request.user is not None:
            LOG.warning("%s requested login while authenticated", request.user)
            raise http.HTTPFound(self.request.route_url('home'))

    @view_config(request_method="GET")
    def get_login(self):
        return {"login_form": self.login_form}

    @view_config(request_method="POST")
    def post_login(self):
        if self.login_form.validate():
            headers = remember(self.request, self.login_form.user.user_id)
            home_url = self.request.route_url('home')
            raise http.HTTPFound(home_url, headers=headers)
        else:
            return {"login_form": self.login_form}


@view_config(route_name="logout")
def logout(request):
    headers = forget(request)
    raise http.HTTPFound(request.route_url('login'), headers=headers)


import wtforms
import wtforms.validators as val


class LoginForm(wtforms.Form):
    username = wtforms.StringField("Username", [val.DataRequired()])
    password = wtforms.PasswordField("Password", [val.DataRequired()])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None  # should be None if logging in

    @staticmethod
    def validate_username(form, field):
        form.user = UserMgr.one(username=field.data)
        if form.user is None:
            msg = field.data + " isn't a registered user."
            raise val.StopValidation(msg)

    @staticmethod
    def validate_password(form, field):
        if form.user is None:
            return
        elif form.user.validate(field.data) is False:
            raise val.StopValidation("Incorrect password")

    def validate(self):
        """ ordered field validation """
        self.username.validate(self, extra_validators=[self.validate_username])
        self.password.validate(self, extra_validators=[self.validate_password])
        return False if self.errors else True
