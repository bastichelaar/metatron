# -*- coding: utf-8 -*-

from pyhocon import ConfigFactory
from .docker import dockerInspect

def imageMetadata(image):
    inspected = dockerInspect(image)
    parsed = ConfigFactory.parse_string(inspected)

    return parsed
