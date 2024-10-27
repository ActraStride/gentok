# app/cli/cli.py

import click
from app.scraper import Scraper
from app.utils import setup_logging

# Configura el logging al iniciar la CLI
setup_logging()

# Definir un grupo de comandos. Esto permite agrupar múltiples comandos bajo un solo CLI.
@click.group()
def cli():
    """Grupo de comandos para la aplicación."""
    pass  # Este grupo de comandos no tiene una funcionalidad propia, solo sirve como agrupador.

# Definir un comando dentro del grupo CLI.
@cli.command()
def webos():
    # Este comando imprimirá el mensaje '¿Apoco si mi todo pendejo?' cuando se ejecute.
    click.echo('¿Apoco si mi todo pendejo?')

# Definir un comando dentro del grupo CLI.
@cli.command()
def hello():
    #Este comando abrirá la web de 'https://www.google.com/'
    scraper = Scraper()
    scraper.open_page('https://www.google.com/')

# Punto de entrada de la aplicación.
if __name__ == '__main__':
    # Ejecuta la CLI cuando se ejecuta el script.
    cli()
