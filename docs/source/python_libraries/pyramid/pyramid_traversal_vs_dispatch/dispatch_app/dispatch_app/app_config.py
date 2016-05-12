from wsgiref.simple_server import make_server
from pyramid.config import Configurator


def foobarbaz_factory(request):
    """
    Typically this would be a model object w/ __acl__ permissions, not a dict.
    """
    return request.matchdict


def main(global_config, **settings):
    config = Configurator(settings=settings)
    config.include('pyramid_mako')  # newly added
    config.add_route('index', '/')

    # URL Dispatch fills request.matchdict and then view's manipulate it
    config.add_route('matchdict_foo', pattern='/matchdict/{foo}')
    config.add_route('matchdict_bar', pattern='/matchdict/{foo}/{bar}')
    config.add_route('matchdict_baz', pattern='/matchdict/{foo}/{bar}/{baz}')

    # URL Dispatch calls simple "route factories" to populate request.context
    config.add_route('factory_foo', pattern='/factory/{foo}',
            factory=foobarbaz_factory)
    config.add_route('factory_bar', pattern='/factory/{foo}/{bar}',
            factory=foobarbaz_factory)
    config.add_route('factory_baz', pattern='/factory/{foo}/{bar}/{baz}',
            factory=foobarbaz_factory)

    config.scan()
    return config.make_wsgi_app()
