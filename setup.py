# -*- coding: utf-8 -*-

import uuid

from setuptools import setup
from pip.req import parse_requirements

try:
    install_reqs = parse_requirements("requirements.txt", session=uuid.uuid1())
except TypeError:
    install_reqs = parse_requirements("requirements.txt")


reqs = [str(ir.req) for ir in install_reqs]

extra = {}

setup(
    name='metatron',
    version='0.1',
    description='Deploys metadata-enhanced docker containers to Kubernetes, Mesos/Marathon, and more.',
    include_package_data=True,
    packages=['metatron'],
    install_requires=reqs,
    entry_points={
        'console_scripts': ['meta2kube = metatron.meta2kube:main']
    },
    zip_safe=False,
    **extra
)
