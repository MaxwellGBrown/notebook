from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound



@view_config(route_name="index")
def index(request):
    return HTTPFound(request.route_url("foo"))


@view_config(route_name="foo", renderer='templates/basic.mako')
def foo(request):
    return {"page": "Foo"}


@view_config(route_name="bar", renderer='templates/basic.mako')
def bar(request):
    return {"page": "Bar"}


@view_config(route_name="baz", renderer='templates/basic.mako')
def baz(request):
    return {"page": "Baz"}
