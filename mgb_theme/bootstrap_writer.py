"""
bootstrap_writer.py

While there are a few projects for turning .rst into bootstrap html, I want to
have custom control over how my application does it.

bootstrap-rst
-------------
https://github.com/rougier/bootstrap-rst

NOTE:
    see this for how to interact w/ docutils writers!
https://github.com/rougier/bootstrap-rst/blob/master/bootstrap.py


basicstrap
----------
https://github.com/tell-k/sphinxjp.themes.basicstrap/tree/master/src
"""

# To use a custom writer, you'll also probably have to define a special builder
# class that specifically uses that builder.

from docutils.writers.html4css1 import HTMLTranslator as docutils_HTMLTranslator
from docutils import nodes

from sphinx.writers.html import HTMLTranslator as sphinx_HTMLTranslator


class BootstrapTranslator(sphinx_HTMLTranslator):
    """
    Inherits from sphinx.writers.html.HTMLTranslator which extends docutils'
    docutils.writers.html4css1.HTMLTranslator
    """

    def __init__(self, *args, **kwargs):
        sphinx_HTMLTranslator.__init__(self, *args, **kwargs)

    def visit_literal(self, node):
        # docutils uses <code></code> instead of a bunch of junk like sphinx
        return docutils_HTMLTranslator.visit_literal(self, node)

    def depart_literal(self, node):
        # docutils uses <code></code> instead of a bunch of junk like sphinx
        return docutils_HTMLTranslator.depart_literal(self, node)

    def visit_literal_block(self, node):
        # docutils uses <code></code> instead of a bunch of junk like sphinx
        return docutils_HTMLTranslator.visit_literal_block(self, node)

    def depart_literal_block(self, node):
        # docutils uses <code></code> instead of a bunch of junk like sphinx
        return docutils_HTMLTranslator.depart_literal_block(self, node)
