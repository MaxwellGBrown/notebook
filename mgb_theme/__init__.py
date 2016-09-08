import os


def get_path():
    """ Entrypoint for setup.py """
    # Theme directory is defined as our parent directory
    return os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


def update_context(app, pagename, templatename, context, doctree):
    context['mgb_theme'] = True


def setup(app):
    app.connect('html-page-context', update_context)

    # This extension REQUIRES that the accomodating theme is used
    app.config['html_theme'] = "mgb_theme"

    # connect to the template bridge!
    app.config["template_bridge"] = "mgb_theme.template_bridge.MakoTemplateBridge"
    # add bootstrap4 css & js (tether is required for bootstrap4 popovers)
    app.add_stylesheet("tether/css/tether.css")
    app.add_stylesheet("bootstrap/css/bootstrap.css")
    app.add_javascript("tether/js/tether.js")
    app.add_javascript("bootstrap/js/bootstrap.js")

    return {'version': "0.0.0"}
