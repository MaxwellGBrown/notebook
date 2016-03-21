from mako.template import Template
from mako.lookup import TemplateLookup
import os.path

this_dir = os.path.dirname(os.path.realpath(__file__))
lookup = TemplateLookup(directories=[this_dir])

t = Template(filename="template_file.mako", lookup=lookup)
print t.render(header_1="Hello World")
