from pyramid.view import view_config


@view_config(route_name='factory_foo', renderer='factory.mako')
def factory_foo(request):
    """ /factory/{foo} """
    render_dict = dict(title="Factory Foo")
    render_dict.update(request.context)
    render_dict.setdefault('bar', None)
    render_dict.setdefault('baz', None)
    return render_dict


@view_config(route_name='factory_bar', renderer='factory.mako')
def factory_bar(request):
    """ /factory/{foo}/{bar} """
    render_dict = dict(title="Factory Foo")
    render_dict.update(request.context)
    render_dict.setdefault('baz', None)
    return render_dict


@view_config(route_name='factory_baz', renderer='factory.mako')
def factory_baz(request):
    """ /factory/{foo}/{bar}/{baz} """
    render_dict = dict(title="Factory Foo")
    render_dict.update(request.context)
    return render_dict
