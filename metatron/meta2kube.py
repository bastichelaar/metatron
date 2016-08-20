# -*- coding: utf-8 -*-

import click

from metatron.meta import *

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
        dockerPull(image, gcloud)

    metadata = getImageMetadata(image)

    click.echo('Metadata: %s' % metadata)






def main():
    generate()

if __name__ == '__main__':
    main()
