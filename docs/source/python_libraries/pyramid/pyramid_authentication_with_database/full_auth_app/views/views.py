from pyramid.view import view_config


@view_config(route_name="index", renderer="full_auth_app:templates/index.mako")
def index(request):
    return {}
