from pyramid.view import view_config


@view_config(route_name='matchdict_foo', renderer='matchdict.mako')
def foo(request):
    """ /{foo} """
    return dict(
            title="foo",
            foo=request.matchdict.get('foo'),
            bar=None,
            baz=None,
            )


@view_config(route_name='matchdict_bar', renderer='matchdict.mako')
def bar(request):
    """ /{foo}/{bar} """
    return dict(
            title="bar",
            foo=request.matchdict.get('foo'),
            bar=request.matchdict.get('bar'),
            baz=None
            )


@view_config(route_name='matchdict_baz', renderer='matchdict.mako')
def baz(request):
    """ /{foo}/{bar}/{baz} """
    return dict(
            title="baz",
            foo=request.matchdict.get('foo'),
            bar=request.matchdict.get('bar'),
            baz=request.matchdict.get('baz'),
            )
