from pyramid.view import view_config


@view_config(route_name='hello', renderer='hello.mako')
def hello_world(request):
    return dict(title="Hello World")
