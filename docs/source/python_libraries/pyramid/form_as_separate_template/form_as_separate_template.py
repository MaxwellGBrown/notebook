from wsgiref.simple_server import make_server

from pyramid.config import Configurator
from pyramid.renderers import render_to_response
from pyramid.view import view_config
from wtforms import Form, StringField, IntegerField
from wtforms.validators import Required, Length, NumberRange


class PersonForm(Form):

    firstname = StringField("First Name",
            validators=[Required(), Length(min=2)])
    lastname = StringField("Last Name",
            validators=[Required(), Length(min=2)])
    age = IntegerField("Age", validators=[NumberRange(min=1, max=99)])
    phone_number = StringField("Phone Number", validators=[Length(min=7)])


all_people = []


@view_config(route_name='index', renderer='index.mako')
def index(request):
    return {"people": all_people}


@view_config(route_name='form')
def form(request):
    if request.method == "GET":
        status_code = 200
        message = "Fill out the form!"
        form = PersonForm()
    elif request.method == "POST":
        form = PersonForm(request.POST)
        if form.validate():
            status_code = 200
            message = "Form was successfully submitted!"
            all_people.append(dict(form.data))  # add person to the "database"
        else:
            status_code = 422
            message = "There were errors in the form!"
    response = render_to_response('form.mako',
            {"message": message, "form": form},
            request=request)
    response.status = status_code
    return response


if __name__ == "__main__":
    config = Configurator()
    config.include('pyramid_mako')
    config.add_route('index', '/')
    config.add_route('form', '/form')
    config.scan()
    app = config.make_wsgi_app()
    server = make_server('localhost', 9999, app)
    print("Starting server at http://localhost:9999")
    server.serve_forever()
