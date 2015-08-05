from pyramid.view import view_config, view_defaults


@view_defaults(renderer='templates/home.mako')
class AppExampleViews(object):
    def __init__(self, request):
        self.request = request

    @view_config(route_name='home')
    def home(self):
        return {'name': 'Home View'}

    @view_config(route_name='hello')
    def hello(self):
        return {'name': 'Hello View'}
