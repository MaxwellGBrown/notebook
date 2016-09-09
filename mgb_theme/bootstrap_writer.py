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
from sphinx.locale import _, admonitionlabels


admonition_card_cls = {
        # matches admonition with key name to it's bootstrap helper class
        "note": "primary",
        "warning": "danger",
        "danger": "danger",
        "error": "danger",
        "hint": "info",
        "important": "warning",
        "tip": "success",
        "todo": "warning",
        }


class BootstrapTranslator(sphinx_HTMLTranslator):
    """
    Inherits from sphinx.writers.html.HTMLTranslator which extends docutils'
    docutils.writers.html4css1.HTMLTranslator
    """

    def __init__(self, *args, **kwargs):
        sphinx_HTMLTranslator.__init__(self, *args, **kwargs)

        # this "hack" works to FINALLY get the theme's options
        self.theme_options = self.builder.theme.get_options({})
        print(self.theme_options)

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

    def visit_admonition(self, node, name=''):
        """ These are the notes, warnings, etc.

        Theses are also implemented as bootstrap cards.
        """
        admonition_classes = ["card", "admonition", name]
        helper_cls = admonition_card_cls.get(name, "primary")

        # Set this admonition up with a card-outline or as an inverse card
        # print(self.theme_options.get('outlined_admonitions'))
        if self.theme_options.get('outlined_admonitions', True) is True:
            admonition_classes.append("card-outline-{}".format(helper_cls))
        else:
            admonition_classes.extend(["card-inverse", "card-" + helper_cls])

        node_cls = " ".join(admonition_classes)
        self.body.append(self.starttag(node, "div", CLASS=node_cls))
        node.bootstrap_cls = helper_cls

        # add a card header if available
        if name:
            node.insert(0, nodes.title(name, admonitionlabels[name]))

        # self.set_first_last(node)

    def depart_admonition(self, node=None):
        self.body.append("</div>\n")  # terminate card-body
        self.body.append("</div>\n")  # terminate card

    def visit_title(self, node):
        """ If parent is node.Admonition then add a card-header """
        if isinstance(node.parent, nodes.Admonition):
            # set up card-header classes
            card_header_classes = ['card-header', 'admonition-title']

            if self.theme_options.get('outlined_admonitions', True) is True:
                bg_class = "bg-{}".format(node.parent.bootstrap_cls)
                card_header_classes.append(bg_class)
            else:
                card_header_classes.append("card-title")

            title_cls = " ".join(card_header_classes)
            self.body.append(self.starttag(dict(), "div", CLASS=title_cls))
            self.context.append("</div>\n")  # depart title closes w/ this
        else:
            super().visit_title(node)

    def visit_paragraph(self, node):
        if isinstance(node.parent, nodes.Admonition) is True:
            # begin the card-body
            self.body.append(self.starttag(dict(), "div", CLASS="card-block"))

            # begin the card-text
            card_text_classes = ['card-text']

            # give contextual text-class if outlined
            if self.theme_options.get('outlined_admonitions', True) is True:
                text_cls = "text-{}".format(node.parent.bootstrap_cls)
                card_text_classes.append(text_cls)
            else:
                pass  # no extra classes for backgrounded!

            card_text_cls = ' '.join(card_text_classes)
            self.body.append(self.starttag(dict(), "p", CLASS=card_text_cls))

            # set the closing tag for both .card-text & .card-body
            self.context.append("</p>\n</div>\n")
        else:
            super().visit_paragraph(node)


