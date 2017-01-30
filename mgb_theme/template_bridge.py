import os

from sphinx.application import TemplateBridge
from sphinx.util.osutil import mtimes_of_files

from mako.template import Template
from mako.lookup import TemplateLookup


class MakoTemplateBridge(TemplateBridge):
    # class MakoTemplateBridge(object):

    def init(self, builder, theme=None, dirs=None):
        """
        called by builder to initialize the template system

        *builder* is the builder object

        *theme* is a :class:`sphinx.theming.Theme` object or None

        *dirs* is a list of fixed template directories when theme is None

        This class is based on sphinx.jinja2glue:BuiltinTemplateLoader
        """
        if theme is not None:
            # the theme's own dir and it's bases' dirs
            template_dirs = theme.get_dirchain()
        elif dirs is not None:
            template_dirs = list(dirs)
        else:
            template_dirs = list()

        # prepend the explicit template paths
        if builder.config.templates_path:
            cfg_templates_path = [os.path.join(builder.confdir, tp)
                                  for tp in builder.config.templates_path]
            template_dirs = cfg_templates_path + template_dirs

        # create a mako template lookup based on template directories
        self.template_lookup = TemplateLookup(directories=template_dirs)

    def newest_template_mtime(self):
        """
        Called by the builder to determine if output files are outdated because
        of template changes.

        Return mtime of thenewest template file that was changed.
        """
        mtimes = list()
        mtimes += mtimes_of_files(self.template_lookup.directories, ".html")
        mtimes += mtimes_of_files(self.template_lookup.directories, ".mako")
        return max(mtimes)

    def render(self, template, context):
        """
        Called by the builder to render a template given as a filename with a
        specified context (a Python dictionary)
        """
        for mako_keyword in ["body", "next", "self", "parent"]:
            if mako_keyword in context:
                context['sphinx_' + mako_keyword] = context.pop(mako_keyword)

        tmpl = self.template_lookup.get_template(template)
        return tmpl.render(**context)

    def render_string(self, template, context):
        """Called by the builder to render a template given as a string with a
        specified context"""
        for mako_keyword in ["body", "next", "self", "parent", "locals"]:
            if mako_keyword in context:
                context['sphinx_' + mako_keyword] = context.pop(mako_keyword)
        tmpl = Template(template)
        return tmpl.render(sphinx_context=context)
