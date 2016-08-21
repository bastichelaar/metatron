# -*- coding: utf-8 -*-

import click

from metatron.meta import *
from metatron.descriptors import *

@click.command()
# @click.option('--template', default="kubernetes", help='The deployment descriptor template to use.')
@click.option('--pull', is_flag=True, default=False, help="Perform a docker pull before attempting to read image metadata. Defaults to False.")
@click.option('--gcloud', is_flag=True, default=False, help="Use 'gcloud docker' instead of 'docker' when pulling images. Defaults to False.")
@click.argument('image', metavar='IMAGE:TAG')
def generate(pull, gcloud, image):
    """
    Generate Kubernetes deployment descriptors from docker IMAGE metadata.
    """
    _, project, version = imageNameAndVersion(image) # TODO: handle errors

    if pull:
        dockerPull(image, gcloud) # TODO: handle errors

    metadata = imageMetadata(image) # TODO: validate some actual metadata was found

    click.echo('Project:       %s' % project)
    click.echo('Name:          %s' % metadata.get_string('meta.attributes.id'))
    click.echo('Version:       %s' % version)
    click.echo('Attributes:    %s' % metadata.get_config('meta.attributes').items())
    click.echo('Health check:  %s' % metadata.get_config('meta.checks.health').items())
    click.echo('Port mappings: %s' % metadata.get_config('meta.ports').items())

    descriptor = descriptorFor('kubernetes', metadata)

    click.echo('Descriptor:\n\n%s' % descriptor)

    # TODO:
    # - generate the k8s file(s)
    #   - labels
    #   - annotations
    #   - health checks
    #   - port mappings
    # - add option to specify output directory? output file name?
    # - support more metadata features

    # Maybe later:
    # - output format option? (yaml or json)
    # - specify a kubernetes label/annotation namespace? Of make this optional and have a default?





def main():
    generate()

if __name__ == '__main__':
    main()
