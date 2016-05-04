from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.config import Configurator
from pyramid.events import ApplicationCreated, subscriber

import sqlalchemy as sa

from full_auth_app.security.factory import RootFactory, UserFactory, \
        GroupFactory
import full_auth_app.model as app_model
from full_auth_app.model.auth import get_user, groupfinder


@subscriber(ApplicationCreated)
def create_app_database(event):
    print("Initializing database...")
    settings = event.app.registry.settings
    # connect_str = "{driver_dialect}://{user}:{password}@{host}/{database}"\
    #         .format(**settings['database'])
    connect_str = "mysql://auth_app_user:auth_app_pass@localhost/auth_app_dev"
    app_model.engine = sa.create_engine(connect_str, echo=True)
    app_model.Base.metadata.bind = app_model.engine
    app_model.Base.metadata.create_all()
    print("Database initialized!")


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
    config.add_route('list_users', '/users')
    # name: the route name (that you assign in @view_config)
    # pattern: the URL pattern w/ variables & whatnot
    # factory: the factory used to retrieve that view's resource
    # traverse: the traversal pattern used to match against factory
    config.add_route(name='user', pattern='/users/{user_id}',
            factory=UserFactory, traverse="/{user_id}")
    config.add_route('list_groups', '/groups')
    config.add_route(name="group", pattern='/groups/{group_id}',
            factory=GroupFactory, traverse="/{group_id}")
    config.add_route(name="join_group", pattern='/groups/{group_id}/join',
            factory=GroupFactory, traverse="/{group_id}")
    config.add_route(name="leave_group", pattern='/groups/{group_id}/leave',
            factory=GroupFactory, traverse="/{group_id}")
    config.scan()

    return config.make_wsgi_app()
