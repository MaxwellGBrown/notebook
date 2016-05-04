from pyramid.httpexceptions import HTTPFound
from pyramid.security import remember, forget
from pyramid.view import view_config

from full_auth_app.model.auth import find_user


# from pyramid.view import forbidden_view_config
# @forbidden_view_config(renderer="full_auth_app:templates/forbidden.mako")
# def forbidden(request):
#     return {}


@view_config(route_name='login', renderer="full_auth_app:templates/login.mako")
def login(request):
    login_form = LoginForm(request.POST)
    if request.method == "POST" and login_form.validate():
        user = find_user(login_form.username.data)
        if user.validate(login_form.password.data) is True:
            headers = remember(request, user.id)
            raise HTTPFound(request.route_url('index'), headers=headers)
    return {"login_form": login_form}


@view_config(route_name="logout")
def logout(request):
    headers = forget(request)
    return HTTPFound(request.route_url('login'), headers=headers)


from wtforms import Form, StringField, PasswordField


class LoginForm(Form):
    username = StringField("Username")
    password = PasswordField("Password")
