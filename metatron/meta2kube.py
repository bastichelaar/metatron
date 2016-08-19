import click

@click.command()
@click.option('--template', default="kubernetes", help='The deployment descriptor template to use.')
@click.argument('image')
def generate(template, image):
    click.echo('Hello World!')


def main():
    generate()

if __name__ == '__main__':
    main()
