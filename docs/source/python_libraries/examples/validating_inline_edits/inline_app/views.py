from pyramid.response import Response
from pyramid.view import view_config
from wtforms import Form, StringField, FieldList, validators


names = {}  # keys will act as ids


@view_config(route_name='index', renderer='templates/index.mako')
def index(request):
    if request.POST:
        print(request.POST)
        form = NameForm(request.POST)
        if form.validate():
            new_name = NameModel()
            form.populate_obj(new_name)
            new_name.id = len(names) + 1
            names[new_name.id] = new_name
    else:
        form = NameForm()

    return {"names": names, "form": form}


@view_config(route_name='inline_edit')
def inline_edit(request):
    print(request.POST)
    pk = int(request.POST.get("pk"))
    name = request.POST.get("name")
    value = request.POST.get("value")

    name_to_be_edited = names.get(pk)

    form = NameForm(obj=name_to_be_edited)
    field = getattr(form, name)
    field.process_formdata([value])  # change the value of the field

    if form.validate():  # the change was good!
        setattr(name_to_be_edited, name, value)
        # session.commit()  # in ORM you'd commit the change!
        response = Response()
        return response  # 200 OK tells X-Editable everything worked
    else:  # change was bad!
        # Since validation failed, no change is made!
        response = Response()
        response.status_int = 422  # Unprocessable Entity is most-correct
        errors = []
        for error_key in form.errors.keys():
            errors.extend(map(lambda x: error_key + x, form.errors[error_key]))
        response.text = "\n".join(errors)
        return response


class NameModel(object):
    """This class spoofs an ORM object."""

    id = 0
    fullname = ""
    nickname = ""


class NameForm(Form):
    fullname = StringField("Full Name", validators=[validators.Required()])
    nickname = StringField("Nick Name")
