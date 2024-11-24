# app/cli/cli.py

import click
from app.scraper import Scraper
from app.utils import setup_logging
from app.cli.get_handlers import subprocess_functions
from app.cli.validate import validate

# Configura el logging al iniciar la CLI
setup_logging()

# Definir un grupo de comandos. Esto permite agrupar múltiples comandos bajo un solo CLI.
@click.group()
def radex():
    """Grupo de comandos para la aplicación."""
    pass  # Este grupo de comandos no tiene una funcionalidad propia, solo sirve como agrupador.

# Definir un comando dentro del grupo CLI.
@radex.command()
def webos():
    # Este comando imprimirá el mensaje '¿Apoco si mi todo pendejo?' cuando se ejecute.
    click.echo('¿Apoco si mi todo pendejo?')

# Definir un comando dentro del grupo CLI.
@radex.command()
def hello():
    #Este comando abrirá la web de 'https://www.google.com/'
    scraper = Scraper()
    scraper.open_page('https://www.google.com/')


@radex.command()
@click.argument('process')
@click.argument('state_tag', required=False, default=None)
@click.argument('district_tag', required=False, default=None)
@click.option('-e', 'grouping', flag_value='state', default=None, help='Groups the information by state.')
@click.option('-d', 'grouping', flag_value='district', help='Groups the information by district.')
@click.option('-s', 'grouping', flag_value='section', help='Groups the information by section.')
def trae(process, state_tag, district_tag, grouping):
    try:

        kwargs = {
            'process': process,
            'state_tag': state_tag,
            'district_tag': district_tag,
            'grouping': grouping
        }

        validate(**kwargs)

        print('HURRA!')
        
        subprocess_functions[process](**kwargs)
    except ValueError:
        print(f"Error: El proceso '{process}' no es válido.")
    except TypeError as e:
        print(f"Error: El estado '{state_tag}' no tiene una función asociada. {e}")


# Punto de entrada de la aplicación.
if __name__ == '__main__':
    # Ejecuta la CLI cuando se ejecuta el script.
    radex()

