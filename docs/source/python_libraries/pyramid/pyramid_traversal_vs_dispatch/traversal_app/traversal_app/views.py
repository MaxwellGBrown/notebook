from pyramid.response import Response
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound, HTTPBadRequest

import traversal_app.model as app_model


# since there's no name= or context=, this is the "default view" (aka "/")
@view_config(renderer="index.mako", context=app_model.RootFactory)
def index(request):
    return {}


@view_config(name="view", renderer="view.mako")
def view(request):
    print("view - request.context: ", str(request.context.__repr__()))
    return dict()

#
# The below views demonstrate how to split a shared route based on context
#

@view_config(context=HTTPBadRequest)
def bad_new(request):
    """ Used to resolve the issue of creating __names__ that match views """
    response = "\"{}\" matches the name of a view & will mess up the resource"\
            " tree. To resolve this, one could set up a resource that acts "\
            "as a URL divider between database queries (e.g. /a/b/c/view "\
            "=> /foo/a/bar/b/baz/c/view). This example does not do that."\
            .format( request.params.get('name'))
    return Response(response)

@view_config(name="new", context=app_model.FooFactory)
def new_foo(context, request):
    if request.params.get('name') in ['view', 'new']: raise HTTPBadRequest

    print("new_foo - request.context: ", str(request.context.__repr__()))
    foo_kwargs = {"foo_name": request.params.get('name')}
    new_foo = app_model.Foo(**foo_kwargs)
    app_model.Session.add(new_foo)
    app_model.try_commit()
    raise HTTPFound(request.resource_url(new_foo, "view"))


@view_config(name="new", context=app_model.Foo)
def new_bar(context, request):
    if request.params.get('name') in ['view', 'new']: raise HTTPBadRequest

    print("new_bar - request.context: ", str(request.context.__repr__()))
    bar_kwargs = {
            "foo_name": request.context.foo_name,
            "bar_name": request.params.get("name"),
            }
    new_bar = app_model.Bar(**bar_kwargs)
    app_model.Session.add(new_bar)
    app_model.try_commit()
    raise HTTPFound(request.resource_url(new_bar, "view"))


@view_config(name="new", context=app_model.Bar)
def new_baz(request):
    if request.params.get('name') in ['view', 'new']: raise HTTPBadRequest

    print("new_baz - request.context: ", request.context.__repr__())
    baz_kwargs = {
            "foo_name": request.context.foo_name,
            "bar_name": request.context.bar_name,
            "baz_name": request.params.get("name"),
            }
    new_baz = app_model.Baz(**baz_kwargs)
    app_model.Session.add(new_baz)
    app_model.try_commit()
    raise HTTPFound(request.resource_url(new_baz, "view"))


@view_config(name="new", context=app_model.Baz)
def new_qux(request):
    if request.params.get('name') in ['view', 'new']: raise HTTPBadRequest

    print("new_qux - request.context: ", request.context.__repr__())
    qux_kwargs = {
            "foo_name": request.context.foo_name,
            "bar_name": request.context.bar_name,
            "baz_name": request.context.baz_name,
            "qux_name": request.params.get("name"),
            }
    new_qux = app_model.Qux(**qux_kwargs)
    app_model.Session.add(new_qux)
    app_model.try_commit()
    raise HTTPFound(request.resource_url(new_qux, "view"))
