# -*- coding: utf-8 -*-

import re

from pyhocon import *
from .docker import dockerInspect


class Metadata(object):

    def __init__(self, image):
        def imageAttributes(image):
            pattern = re.compile('(?:(.+)/)?(.+):(.+)')
            matched = pattern.match(image)

            # TODO: raise an error if matched is None

            return matched.groups()

        def parse(image):
            inspected = dockerInspect(image)
            parsed = ConfigFactory.parse_string(inspected)
            registry, project, version = imageAttributes(image)

            parsed.put('meta.attributes.image', image)
            parsed.put('meta.attributes.project', project)
            parsed.put('meta.attributes.version', version)
            parsed.put('meta.attributes.registry', registry)

            return parsed

        self.__meta__ = parse(image)


    # Add some ConfigTree/dict-like passthrough methods

    def items(self):
        return self.__meta__.items()

    def iterkeys(self):
        return self.__meta__.iterkeys()

    def __getitem__(self, key):
        return self.__meta__[key]


    # Support for getting out a flattened set of filtered properties

    def flatten(self, key_filter = lambda x: x):
        return self.__flatten__(config = self.__meta__, key_filter = key_filter)

    @staticmethod
    def __flatten__(config, prefix = '', key_filter = lambda x: x):
        def concat(prefix, suffix):
            return suffix if prefix == '' else '%s.%s' % (prefix, suffix)

        list_of_results = [
            flatten(value, concat(prefix, key), key_filter) if isinstance(value, ConfigTree)
                else [concat(prefix, key) + '=' + value]

            for key, value in config.items()
            if key_filter(key)
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
