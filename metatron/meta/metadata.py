# -*- coding: utf-8 -*-

import re

from pyhocon import *
from .docker import dockerInspect

def imageMetadata(image):
    inspected = dockerInspect(image)
    parsed = ConfigFactory.parse_string(inspected)
    registry, project, version = imageNameAndVersion(image)

    parsed.put('meta.attributes.image', image)
    parsed.put('meta.attributes.project', project)
    parsed.put('meta.attributes.version', version)
    parsed.put('meta.attributes.registry', registry)

    return parsed


def imageNameAndVersion(image):
    pattern = re.compile('(?:(.+)/)?(.+):(.+)')
    matched = pattern.match(image)

    # TODO: raise an error if matched is None

    return matched.groups()


def flatten(config, prefix = '', keyFilter = lambda x: x):
    def concat(prefix, suffix):
        return suffix if prefix == '' else '%s.%s' % (prefix, suffix)

    list_of_results = [
        flatten(value, concat(prefix, key), keyFilter) if isinstance(value, ConfigTree)
            else [concat(prefix, key) + '=' + value]

        for key, value in config.items()
        if keyFilter(key)
    ]

    return [item for result in list_of_results
                 for item in result]


# def flatten(config, prefix = '', results = [], keyFilter = lambda x: x):
#     """
#     Takes a pyhocon ConfigTree and flattens it to a list of name
#     """
#     def concat(prefix, suffix):
#         return suffix if prefix == '' else '%s.%s' % (prefix, suffix)

#     out = results
#     for key in filter(keyFilter, config.iterkeys()):
#         value = config.get(key)
#         if not(isinstance(value, ConfigTree)):
#             out.extend([('%s="%s"' % (concat(prefix, key), value))])
#         else:
#             out.extend(flatten(value, concat(prefix, key), results, keyFilter))
#     return out
