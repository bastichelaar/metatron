# -*- coding: utf-8 -*-

import re

from pyhocon import ConfigFactory
from .docker import dockerInspect

def imageMetadata(image):
    inspected = dockerInspect(image)
    parsed = ConfigFactory.parse_string(inspected)
    name, version = imageNameAndVersion(image)

    parsed.put('meta.attributes.name', name)
    parsed.put('meta.attributes.version', version)
    parsed.put('meta.attributes.image', image)

    return parsed

def imageNameAndVersion(image):
    pattern = re.compile('(.+):(.+)')
    matched = pattern.match(image)

    # TODO: raise an error if matched is None

    return matched.groups()
