from wsgiref.simple_server import make_server
from pyramid.config import Configurator

from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from sqlalchemy import engine_from_config

from auth_app.security.factory import RootFactory
from auth_app.model.auth import auth_callback, request_user
from auth_app.model.meta import bind_engine
from auth_app.auth import authn_policy, authz_policy


def main(global_config, **settings):
    config = Configurator(settings=settings)

    config.include('pyramid_mako')

    # create the model based on the .ini
    engine = engine_from_config(configuration=settings, prefix='sqlalchemy.')
    bind_engine(engine, create_all=True)

    # add current authenticated user as request.user
    config.add_request_method(request_user, 'user', reify=True)

    # get auth kwargs from .ini file
    auth_cfg = {k[5:]: v for k, v in settings.items() if k.startswith('auth.')}

    # set authentication policy from auth_app.auth:authn_policy()
    authentication_policy = authn_policy(callback=auth_callback, **auth_cfg)
    config.set_authentication_policy(authentication_policy)

    # set authorization policy from auth_app.auth:authz_policy()
    authorization_policy = authz_policy()
    config.set_authorization_policy(authorization_policy)

    # set the root factory w/ __acl__ permissions
    config.set_root_factory(RootFactory)

    config.add_route('index', '/')
    config.add_route('home', '/home')
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')
    config.scan()

    return config.make_wsgi_app()
