import time

from pyramid.response import Response
from pyramid.view import view_config


session = {
        "queue": list(),
        "count": 0,
        }


@view_config(route_name='index', renderer='templates/index.mako')
def index(request):
    return {}

@view_config(route_name="ajax_process", renderer='json')
def process(request):
    request.session = session  # spoofing flask's session for this example

    if not request.session.get('queue'):  # if not queue, reset count & queue
        start = int(request.params.get("start"))
        end = int(request.params.get("end"))
        step = int(request.params.get("step"))

        request.session['count'] = 0
        request.session['queue'] = [i for i in range(start, end, step)]

    # do the "process"
    time.sleep(2)  # wait so this example can show off the loading bar
    next_number = request.session['queue'].pop(0)
    request.session['count'] += 1

    total = request.session['count'] + len(request.session['queue'])
    percentage = (request.session['count'] / total) * 100
    print("Next in queue: {} ({}%)".format(next_number, percentage))

    return {"percentage": percentage}
