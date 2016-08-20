# -*- coding: utf-8 -*-

import subprocess

def dockerPull(image, gcloud):
    if gcloud:
        return subprocess.check_call(['gcloud', 'docker', '--', 'pull', image])
    else:
        return subprocess.check_call(['docker', 'pull', image])

def getImageMetadata(image):
    template = """{{range $key, $value := .Config.Labels}}
{{$key}}="{{$value}}"{{end}}"""

    return subprocess.check_output(['docker', 'inspect', "--format='%s'" % template, image])
