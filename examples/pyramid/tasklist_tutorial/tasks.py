import os
import logging
import sqlite3

from pyramid.config import Configurator
from pyramid.session import UnencryptedCookieSessionFactoryConfig

from pyramid.events import NewRequest, subscriber, ApplicationCreated

from pyramid.exceptions import NotFound
from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config

from wsgiref.simple_server import make_server


logging.basicConfig()
log = logging.getLogger(__file__)

here = os.path.dirname(os.path.abspath(__file__))


@view_config(route_name='list', renderer='list.mako')
def list_view(request):
    rs = request.db.execute("select id, name from tasks where closed = 0")
    tasks = [dict(id=row[0], name=row[1]) for row in rs.fetchall()]
    return {'tasks': tasks}


@view_config(route_name='new', renderer='new.mako')
def new_view(request):
    if request.method == "POST":
        if request.POST.get("name"):
            request.db.execute(
                    'insert into tasks (name, closed) values (?, ?)',
                    [request.POST['name'], 0])
            request.db.commit()
            request.session.flash('New task was successfully added!')
            return HTTPFound(location=request.route_url('list'))
        else:
            request.session.flash("Please enter a name for the task!")
    return {}


@view_config(route_name='close')
def close_view(request):
    task_id = int(request.matchdict['id'])
    request.db.execute("update tasks set closed = ? where id = ?",
            (1, task_id))
    request.db.commit()
    request.session.flash('Task was successfully closed!')
    return HTTPFound(location=request.route_url('list'))


@view_config(context='pyramid.exceptions.NotFound', renderer='notfound.mako')
def notfound_view(request):
    request.response.status = '404 Not Found'
    return {}


@subscriber(ApplicationCreated)
def create_database_with_app(event):
    log.warn("Initializing database...")
    with open(os.path.join(here, 'schema.sql')) as schema:
        sql_command = schema.read()
        settings = event.app.registry.settings
        db = sqlite3.connect(settings['db'])
        db.executescript(sql_command)


@subscriber(NewRequest)
def connect_to_database_on_new_request(event):
    request = event.request
    settings = request.registry.settings
    request.db = sqlite3.connect(settings['db'])
    request.add_finished_callback(close_db_connection)


def close_db_connection(request):
    request.db.close()


if __name__ == '__main__':
    # typically, settings would be an .ini file
    settings = {}
    settings['reload_all'] = True
    settings['debug_all'] = True
    settings['db'] = os.path.join(here, 'tasks.db')
    settings['mako.directories'] = os.path.join(here, 'templates')

    secret = "itsaseekreet"
    session_factory = UnencryptedCookieSessionFactoryConfig(secret)

    config = Configurator(settings=settings, session_factory=session_factory)
    config.include('pyramid_mako')
    config.add_route('list', '/')
    config.add_route('new', '/new')
    config.add_route('close', '/close/{id}')
    config.add_static_view('static', os.path.join(here, 'static'))
    config.scan()

    app = config.make_wsgi_app()
    print "serving app at localhost:8888"
    server = make_server('127.0.0.1', 8888, app)
    server.serve_forever()
