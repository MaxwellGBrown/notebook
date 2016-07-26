"""
Separated from app_config:main() so they can be leveraged in fxnal testing.
"""
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy


def authn_policy(*args, **kwargs):
    return AuthTktAuthenticationPolicy(*args, **kwargs)


def authz_policy(*args, **kwargs):
    return ACLAuthorizationPolicy()
