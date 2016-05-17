from collections import OrderedDict

from pyramid.response import Response
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound, HTTPBadRequest

import hybrid_app.model as app_model


@view_config(route_name="index", renderer="index.mako")
def index(request):
    return {"view_root_factory": app_model.FooFactory()}


@view_config(route_name="view", renderer="view.mako")
def view(request):
    print("view - request.context: ", str(request.context.__repr__()))
    return dict()


@view_config(route_name="new", name="new")
def new(context, request):
    """
    resource_url(resource, "new", route_name="new")
    -----------------------------------------------
    /route/defined/path/*traverse/<view_name>

    since this model is pretty straightforward, the contexts all share the same
    "new" view/route.

    Notice how this has a route_name AND a view_name. The complete aspect of
    Traversal can be leveraged in Hybrid Traversal.
    """
    print("new - request.context: ", str(request.context.__repr__()))
    if request.params.get('name') in ['view', 'new']: raise HTTPBadRequest

    kwargs = dict()
    kwarg_keys = (
            ("foo_name", app_model.Foo),
            ("bar_name", app_model.Bar),
            ("baz_name", app_model.Baz),
            ("qux_name", app_model.Qux),
    )
    for key, cls in kwarg_keys:
        if hasattr(request.context, key) is True:
            kwargs[key] = getattr(request.context, key)
        else:
            kwargs[key] = request.params.get('name')
            break

    new_obj = cls(**kwargs)
    app_model.Session.add(new_obj)
    success = app_model.try_commit()
    raise HTTPFound(request.resource_url(new_obj, route_name="view"))


@view_config(context=HTTPBadRequest)
def bad_new(request):
    """ Used to resolve the issue of creating __names__ that match views """
    response = "\"{}\" matches the name of a view & will mess up the resource"\
            " tree. To resolve this, one could set up a resource that acts "\
            "as a URL divider between database queries (e.g. /a/b/c/view "\
            "=> /foo/a/bar/b/baz/c/view). This example does not do that."\
            .format( request.params.get('name'))
    return Response(response)
