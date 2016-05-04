from pyramid.view import view_config

from full_auth_app.model.auth import all_users, new_user


@view_config(route_name="list_users",
        renderer="full_auth_app:templates/list_users.mako")
def list_users(request):
    form = UserForm(request.POST)
    if request.method == "POST" and form.validate():
        added_user = new_user(username=form.username.data,
                password=form.password.data)
    else:
        added_user = None
    return {"users": all_users(), "new_user": added_user, "user_form": form}


@view_config(route_name="user", renderer="full_auth_app:templates/user.mako")
def user_view(request):
    """ request.context is a User gathered by UserFactory """
    return {"user": request.context}


from wtforms import Form, StringField, PasswordField, validators as val
from wtforms.validators import ValidationError


def unique_username(form, field):
    all_usernames = [u.username for u in all_users()]
    if field.data in all_usernames:
        raise ValidationError(field.data + " is already being used!")


class UserForm(Form):
    username = StringField("Username",
            validators=[unique_username, val.Length(min=6)])
    password = PasswordField("Password",
            validators=[val.Length(min=6)])
    match_password = PasswordField("Confirm Password",
            validators=[val.EqualTo('password')],
            )
