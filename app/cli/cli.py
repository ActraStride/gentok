import click

@click.group()
def cli():
    """Grupo de comandos para la aplicación."""
    pass

@cli.command()
def webos():
    click.echo('¿Apoco si mi todo pendejo?')

if __name__ == '__main__':
    cli()
