from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response


def hello_world(request):
    return Response("Hello")


def main():
    config = Configurator()
    config.add_route('hello', '/')
    config.add_view(hello_world, route_name="hello")
    app = config.make_wsgi_app()
    return app


if __name__ == "__main__":
    app = main()
    server = make_server('localhost', 8888, app)
    print("Starting server at http://localhost:8888")
    server.serve_forever()
