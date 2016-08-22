# -*- coding: utf-8 -*-

from jinja2 import *

def descriptorFor(template, metadata):
    env = Environment(loader=PackageLoader('metatron', 'templates'))
    env.trim_blocks = True

    template = env.get_template('%s.jinja2' % template)

    return template.render(metadata=metadata)
