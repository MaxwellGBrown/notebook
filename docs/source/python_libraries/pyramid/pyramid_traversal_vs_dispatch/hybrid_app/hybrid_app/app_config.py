from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from sqlalchemy import engine_from_config

import hybrid_app.model as app_model



def main(global_config, **settings):
    config = Configurator(settings=settings)
    config.include('pyramid_mako')

    engine = engine_from_config(configuration=settings, prefix="sqlalchemy.")
    app_model.bind_engine(engine, create_all=True)

    # Traversal works on the assumption of one great resource tree that
    # begins w/ the RootFactory.
    config.set_root_factory(app_model.RootFactory)

    # All traversal views are matched by "view_name" and context which is 
    # declared in @view_config(name="", context=cls_obj)
    # The last piece of the URL that does not match a resource is used as the
    # view_name.

    config.scan()
    return config.make_wsgi_app()
