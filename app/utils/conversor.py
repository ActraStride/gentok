from bs4 import BeautifulSoup
import json
import logging

# Configuración del logger
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def table_to_list(html):
    """
    Convierte el contenido HTML de una tabla en una lista de listas.
    
    Args:
        html (str): Contenido HTML que contiene una tabla.
    
    Returns:
        list: Una lista de listas donde cada sublista representa una fila de la tabla.
    """
    try:
        # Parsear el contenido HTML usando BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')
        
        # Encontrar la primera tabla en el HTML
        table = soup.find('table')
        if not table:
            raise ValueError("No se encontró ninguna tabla en el HTML proporcionado.")
        
        # Inicializar una lista para almacenar los datos de la tabla
        table_data = []
        
        # Iterar sobre cada fila en la tabla
        for row in table.find_all('tr'):
            # Extraer los datos de cada celda en la fila
            cells = row.find_all(['th', 'td'])
            # Convertir los datos en texto, eliminar espacios y saltos de línea
            row_data = [cell.get_text(strip=True) for cell in cells]
            # Agregar la fila a la lista de datos de la tabla
            table_data.append(row_data)
        
        # Mostrar el resultado en el log
        logger.info(f"Datos de la tabla extraídos exitosamente. {table_data}")
        return table_data

    except Exception as e:
        # Loggear cualquier excepción que ocurra
        logger.error("Se produjo un error al procesar la tabla: %s", e)
        return None

def list_to_x(list_table, outputFormat):
    # Conversión a una lista de diccionarios
    result = [
        {f"col_{i+1}": value for i, value in enumerate(row)}
        for row in list_table
    ]

    # Convertir a JSON
    json_result = json.dumps(result, ensure_ascii=False, indent=4)
    # Mostrar el JSON
    return(json_result)

