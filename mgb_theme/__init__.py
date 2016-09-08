import os


def get_path():
    """ Entrypoint for setup.py """
    # Theme directory is defined as our parent directory
    return os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


def update_context(app, pagename, templatename, context, doctree):
    context['mgb_theme'] = True


def setup(app):
    app.connect('html-page-context', update_context)
    return {'version': "0.0.0"}
