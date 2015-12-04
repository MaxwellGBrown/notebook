from wsgiref.simple_server import make_server
from pyramid.config import Configurator

from pyramid.view import view_config, view_defaults
from webhelpers.html import literal
from wtforms import Form, StringField, FieldList, FormField


class ChildForm(Form):
    tag = StringField("Tag")

class ParentForm(Form):
    name = StringField("Name")
    tags = FieldList(FormField(ChildForm))

@view_defaults(renderer='form.mako')
class AppController(object):
    def __init__(self, request):
        self.request = request

    @view_config(route_name="form")
    def form(self):
        form = ParentForm(self.request.POST)

        if self.request.method == "POST" and form.validate():
            # form.populate_obj(parent)
            print form.name.data
            for child in form.tags.entries:
                print "\t{}".format(child.tag.data)

        return {
                "form": form,
                "child_form": ChildForm,
                "literal": literal,
                }


if __name__ == "__main__":
    config = Configurator()
    config.include('pyramid_mako')
    config.add_route('form', '/')
    config.scan()
    app = config.make_wsgi_app()
    server = make_server('localhost', 8888, app)
    print("Starting server at http://localhost:8888")
    server.serve_forever()
