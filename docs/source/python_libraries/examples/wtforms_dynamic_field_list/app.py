from wsgiref.simple_server import make_server
from pyramid.config import Configurator

from pyramid.view import view_config, view_defaults
from wtforms import Form, StringField, FieldList, FormField

from dynamic_field_list import DynamicFieldList


class PhoneNumberForm(form):
    location = SelectField("Location",
            options=[
                ("home", "Home Phone"),
                ("work", "Work Phone"),
                ("cell", "Cell Phone"),
                ],
            )
    number = TextField("Phone Number")

class ContactForm(form):
    name = TextField("Name")
    phone_numbers = DynamicFieldList(FormField(PhoneNumberForm))


@view_defaults(renderer='form.mako')
class AppController(object):
    def __init__(self, request):
        self.request = request

    @view_config(route_name="form")
    def form(self):
        form = ParentForm(self.request.POST)
        if self.request.method == "POST" and form.validate():
            print("Validated!")
            for key, value in form.data.items():
                print("{}: {}".format(key, value))
        return {"form": form}


if __name__ == "__main__":
    config = Configurator()
    config.include('pyramid_mako')
    config.add_route('form', '/')
    config.scan()
    app = config.make_wsgi_app()
    server = make_server('localhost', 8888, app)
    print("Starting server at http://localhost:8888")
    server.serve_forever()
