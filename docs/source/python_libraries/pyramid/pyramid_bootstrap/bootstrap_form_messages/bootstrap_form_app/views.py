from pyramid.view import view_config
from wtforms import Form, BooleanField, StringField, PasswordField
import wtforms.validators as val


@view_config(route_name="index", renderer="templates/basic.mako")
def index(request):
    form = ExampleForm(request.POST)
    if request.method == "POST" and form.validate():
        message = "The form was validated!"
    elif request.method == "POST" and not form.validate():
        message = "Please review errors in the form below."
    else:
        message = "Complete the form w/ errors to see the example in action!"
    return {"form": form, "message": message}


class ExampleForm(Form):
    username = StringField("Username", [val.Length(min=5, max=25)])
    email = StringField("Email", [val.Email(), val.InputRequired()])
    password = PasswordField("Password", [val.Length(min=6, max=25)])
