from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from database_app.models import bind_engine


def main(global_config, **settings):
    config = Configurator(settings=settings)

    config.include('pyramid_mako')

    # config.scan('database_app.models')
    engine = engine_from_config(configuration=settings, prefix="sqlalchemy.")
    bind_engine(engine, create_all=True)

    config.add_route('index', '/')
    config.scan()

    return config.make_wsgi_app()
