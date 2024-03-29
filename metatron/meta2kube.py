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
    if pull:
        dockerPull(image, gcloud) # TODO: handle errors

    metadata = Metadata(image)

    # click.echo('Project: %s' % metadata['meta.attributes.project'])
    # click.echo('Name:    %s' % metadata['meta.attributes.id'])
    # click.echo('Version: %s' % metadata['meta.attributes.version'])
    # click.echo('')

    # click.echo('')
    # flattened = metadata.flatten(key_filter = lambda k: not(k.startswith('attributes')))
    # for annotation in flattened:
    #     click.echo('%s' % annotation)

    click.echo(descriptorFor('kubernetes', metadata))


    # TODO:
    # - add option to specify output directory? output file name?
    #
    # Maybe later:
    # - output format option? (yaml or json)
    # - specify a kubernetes label/annotation namespace? Of make this optional and have a default?


def main():
    generate()

if __name__ == '__main__':
    main()
