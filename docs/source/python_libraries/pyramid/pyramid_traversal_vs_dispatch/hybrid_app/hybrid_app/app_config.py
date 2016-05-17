from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from sqlalchemy import engine_from_config

import hybrid_app.model as app_model



def main(global_config, **settings):
    config = Configurator(settings=settings)
    config.include('pyramid_mako')

    engine = engine_from_config(configuration=settings, prefix="sqlalchemy.")
    app_model.bind_engine(engine, create_all=True)

    config.add_route("index", pattern="/")

    # using *traverse, urls are completed by traversing the object factory
    config.add_route("view", pattern="/view*traverse",
            factory=app_model.FooFactory, traverse="*traverse")

    # config.add_route("new", pattern="/new*traverse",
    #         factory=app_model.FooFactory, traverse="*traverse")

    config.add_route("new_foo", pattern="/new", factory=app_model.FooFactory)
    config.add_route("new_bar", pattern="/{foo_name}/new",
            factory=app_model.FooFactory, traverse="/{foo_name}")
    config.add_route("new_baz",
            pattern="/{foo_name}/{bar_name}/new",
            factory=app_model.FooFactory,
            traverse="/{foo_name}/{bar_name}")
    config.add_route("new_qux",
            pattern="/{foo_name}/{bar_name}/{baz_name}/new",
            factory=app_model.FooFactory,
            traverse="/{foo_name}/{bar_name}/{baz_name}")


    # # special traversal sections can be provided also
    # config.add_route("new_foo", pattern="/new", factory=app_model.FooFactory)
    # config.add_route("new_bar", pattern="/{foo_name}/new",
    #         factory=app_model.FooFactory, traverse="/{foo_name}")
    # config.add_route("new_baz", pattern="/{foo_name}/{bar_name}/new",
    #         factory=app_model.FooFactory, traverse="/{foo_name}/{bar_name}")
    # config.add_route("new_qux",
    #         pattern="/{foo_name}/{bar_name}/{baz_name}/new",
    #         factory=app_model.FooFactory,
    #         traverse="/{foo_name}/{bar_name}/{baz_name}",
    #         )

    config.scan()
    return config.make_wsgi_app()
