﻿"""
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
from sphinx.locale import _, admonitionlabels


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
        parent_is_container = isinstance(node.parent, nodes.container)
        if parent_is_container is False:
            card = self.starttag(dict(), "div", "", CLASS='card')
            self.body.append(card)

        self.body.append(self.starttag(dict(), 'div', CLASS='card-block'))
        self.body.append(self.starttag(node, 'pre', CLASS='literal-block'))

    def depart_literal_block(self, node):
        self.body.append("</pre>\n")
        self.body.append("</div>\n")

        parent_is_container = isinstance(node.parent, nodes.container)
        if parent_is_container is False:
            self.body.append("</div>\n")  # terminate card

    def visit_container(self, node):
        """ Add .card to all containers making them bootstrap cards """
        self.body.append(self.starttag(node, 'div', CLASS='card'))

    def depart_container(self, node):
        self.body.append('</div>\n')

    def visit_caption(self, node):
        parent_is_container = isinstance(node.parent, nodes.container)
        if parent_is_container is True:
            card_header = self.starttag(node, 'div', '', CLASS='card-header')
            self.body.append(card_header)

        if parent_is_container and node.parent.get('literal_block'):
            self.body.append('<div class="code-block-caption">')
        else:
            docutils_HTMLTranslator.visit_caption(self, node)
        self.add_fignumber(node.parent)

    def depart_caption(self, node):
        # self.body.append("</div>\n")

        # append permalink if available
        if isinstance(node.parent, nodes.container) and \
                node.parent.get('literal_block'):
            self.add_permalink_ref(node.parent, _('Permalink to this code'))
        elif isinstance(node.parent, nodes.figure):
            image_nodes = node.parent.traverse(nodes.image)
            target_node = image_nodes and image_nodes[0] or node.parent
            self.add_permalink_ref(target_node, _('Permalink to this image'))
        elif node.parent.get('toctree'):
            self.add_permalink_ref(node.parent.parent,
                    _('Permalink to this toctree'))

        if isinstance(node.parent, nodes.container) and \
                node.parent.get('literal_block'):
            self.body.append('</div>\n')
        else:
            BaseTranslator.depart_caption(self, node)

        self.body.append('</div>\n')

    # --- all admonitions -----------------------------------------------------
    def visit_admonition(self, node, name=''):
        """ These are the notes, warnings, etc.

        Theses are also implemented as bootstrap cards.
        """
        # create admonition card
        node_cls = " ".join(["card", "admonition", name])
        self.body.append(self.starttag(node, "div", CLASS=node_cls))

        # add a card header if available
        if name:
            node.insert(0, nodes.title(name, admonitionlabels[name]))

        # self.set_first_last(node)

    def visit_title(self, node):
        """ If parent is node.Admonition then add a card-header """
        if isinstance(node.parent, nodes.Admonition):
            card_head_cls = " ".join(["card-header", "admonition-title"])
            self.body.append(self.starttag(dict(), "div", CLASS=card_head_cls))
            self.context.append("</div>\n")  # depart title closes w/ this
        else:
            super().visit_title(node)

    def visit_paragraph(self, node):
        if isinstance(node.parent, nodes.Admonition) is True:
            # begin the card-body
            self.body.append(self.starttag(dict(), "div", CLASS="card-block"))
            self.context.append("</div>\n")
        else:
            super().visit_paragraph(node)

    def depart_admonition(self, node=None):
        self.body.append("</div>\n")  # terminate card-body
        self.body.append("</div>\n")  # terminate card

    def visit_note(self, node):
        self.visit_admonition(node, 'note')

    def depart_note(self, node):
        self.depart_admonition(node)

    def visit_warning(self, node):
        self.visit_admonition(node, 'warning')

    def depart_warning(self, node):
        self.depart_admonition(node)

    def visit_attention(self, node):
        self.visit_admonition(node, 'attention')

    def visit_danger(self, node):
        self.visit_admonition(node, 'danger')

    def visit_error(self, node):
        self.visit_admonition(node, 'error')

    def visit_hint(self, node):
        self.visit_admonition(node, 'hint')

    def visit_important(self, node):
        self.visit_admonition(node, 'important')

    def visit_tip(self, node):
        self.visit_admonition(node, 'tip')
    # --- end admonitions -----------------------------------------------------


