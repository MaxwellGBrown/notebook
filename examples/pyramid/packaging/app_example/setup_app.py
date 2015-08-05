from pyramid.config import Configurator


def main():
    config = Configurator()
    config.app_route('hello', '/')
    config.scan('views')
    app = config.make_wsgi_app()
    return app
