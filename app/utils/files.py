import json
import logging

# Configuración del logger
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def save_json_to_file(data, file_path):
    """
    Guarda un diccionario en un archivo JSON.

    Args:
        data (dict): Diccionario con datos a guardar.
        file_path (str): Ruta del archivo donde se guardará el JSON.
    """
    # Abre el archivo en modo escritura
    with open(file_path, 'w') as file:
        # Escribe el diccionario como JSON en el archivo
        json.dump(data, file)
