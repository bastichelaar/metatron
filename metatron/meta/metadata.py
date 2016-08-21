# -*- coding: utf-8 -*-

import re

from pyhocon import ConfigFactory
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
