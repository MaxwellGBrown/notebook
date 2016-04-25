from pyramid.view import view_config, forbidden_view_config
from pyramid.httpexceptions import HTTPFound
from pyramid.security import remember, forget, Allow, Everyone
from wtforms import Form, StringField, PasswordField, validators

from auth_app.model.auth import USERS


@view_config(route_name='login', renderer="auth_app:templates/login.mako")
def login(request):
    login_form = LoginForm(request.POST)
    if request.method == "POST" and login_form.validate():
        for user in USERS:
            if user.username == login_form.login.data:
                if user.password == login_form.password.data:
                    print("Successful auth as ", login_form.login.data)
                    headers = remember(request, user.userid)
                    raise HTTPFound(request.route_url('index'), headers=headers)
    return {"login_form": login_form}


@view_config(route_name="logout")
def logout(request):
    headers = forget(request)
    return HTTPFound(request.route_url('login'), headers=headers)


@forbidden_view_config(renderer="auth_app:templates/forbidden.mako")
def forbidden(request):
    return {}


@view_config(route_name="index", renderer="auth_app:templates/index.mako",
        permission="view")
def index(request):
    return {}


@view_config(route_name="admin", renderer="auth_app:templates/admin.mako",
        permission='admin')
def admin(request):
    return {}


@view_config(route_name="public", renderer="auth_app:templates/public.mako")
def public(request):
    return {}


class LoginForm(Form):
    login = StringField("Username")
    password = PasswordField("Password")
