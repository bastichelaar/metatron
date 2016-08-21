# -*- coding: utf-8 -*-

from jinja2 import *

def descriptorFor(template, metadata):
    env = Environment(loader=PackageLoader('metatron', 'templates'))
    env.trim_blocks = True

    template = env.get_template('%s.jinja2' % template)

    return template.render(metadata=metadata)





#   portMappings = getPortMappings(annotations)
#   servicePorts = portMappings.collect { name, mappings ->
#     """\
#   - name: ${name}
#     port: ${mappings['service']}
#     targetPort: ${mappings['container']}"""
#   }
#   podPorts = portMappings.collect { name, mappings ->
#     """\
#         - name: ${name}
#           containerPort: ${mappings['container']}"""
#   }

#   // TODO:
#   // - add other deploy time metadata annotations (build time?, jenkins build number?)
#   // - add metadata support for number of replicas

#   """\
#   """
