from wsgiref.simple_server import make_server
from pyramid.config import Configurator

from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy

from auth_app.security.factory import RootFactory
from auth_app.model.auth import get_user, groupfinder


def main(global_config, **settings):
    config = Configurator(settings=settings)

    config.include('pyramid_mako')

    config.add_request_method(get_user, 'user', reify=True)

    # note that callback=groupfinder is how request gets current users groups
    authn_policy = AuthTktAuthenticationPolicy("auth_secret",
            callback=groupfinder, hashalg='sha512')
    authz_policy = ACLAuthorizationPolicy()
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)

    config.set_root_factory(RootFactory)

    config.add_route('index', '/')
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')
    config.add_route('admin', '/admin')
    config.add_route('public', '/public')
    config.add_route('users', '/users_only')
    config.scan()

    return config.make_wsgi_app()
