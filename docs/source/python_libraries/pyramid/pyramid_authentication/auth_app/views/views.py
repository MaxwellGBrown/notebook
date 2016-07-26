from pyramid.view import view_config, forbidden_view_config

from auth_app.model.auth import UserMgr


@forbidden_view_config(renderer="forbidden.mako")
def forbidden(request):
    return {}


@view_config(route_name="index", renderer="index.mako")
def index(request):
    user_form = UserForm(request.POST)
    if request.method == "POST" and user_form.validate():
        new_user = UserMgr.new(username=user_form.username.data)
        print("new_user: ", new_user)
        new_user.password = user_form.password.data
        UserMgr.commit()
    return {"user_form": user_form}


@view_config(route_name="home", renderer="home.mako", permission="view")
def home(request):
    all_users = UserMgr.get().all()
    return {"all_users": all_users}


import wtforms


class UserForm(wtforms.Form):
    username = wtforms.StringField("Username",
            validators=[wtforms.validators.DataRequired()])
    password = wtforms.PasswordField("Password",
            validators=[wtforms.validators.DataRequired()])

    def validate_username(form, field):
        if UserMgr.one(username=field.data):
            msg = "Username {} is taken".format(field.data)
            raise wtforms.ValidationError(msg)
