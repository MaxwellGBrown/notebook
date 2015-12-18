from wsgiref.simple_server import make_server
from pyramid.config import Configurator


def main(global_config, **settings):
    config = Configurator(settings=settings)

    config.include('pyramid_mako')

    config.add_static_view('static', 'static')

    config.add_route('table', '/{table_type}')
    config.add_route('table_data', '/table_data/{table_type}')

    config.scan()
    return config.make_wsgi_app()
