﻿from wsgiref.simple_server import make_server
from pyramid.config import Configurator


def main(global_config, **settings):
    config = Configurator(settings=settings)

    config.include('pyramid_mako')

    config.add_route('index', '/')
    config.scan()

    return config.make_wsgi_app()
