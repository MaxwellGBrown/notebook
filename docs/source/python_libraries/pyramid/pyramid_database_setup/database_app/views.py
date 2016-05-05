from pyramid.response import Response
from pyramid.view import view_config
from wtforms import Form, StringField

import database_app.models as app_model
# from database_app.models import Session
# from database_app.models.contact import Contact


@view_config(route_name='index', renderer="index.mako")
def hello_world(request):
    form = ContactForm(request.POST)
    if request.method == "POST" and form.validate():
        contact = app_model.contact.Contact(**form.data)
        app_model.Session.add(contact)
        app_model.Session.commit()
        # contact = Contact(**form.data)
        # Session.add(contact)
        # Session.commit()
    return {
            "form": form,
            # "contacts": Session.query(Contact).all(),
            "contacts": app_model.Session.query(app_model.Contact).all(),
            }


class ContactForm(Form):
    first_name = StringField("First Name")
    last_name = StringField("Last Name")
    address = StringField("Address")
