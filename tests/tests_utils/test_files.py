import pytest
import json
import logging.config
from unittest.mock import patch, MagicMock
from settings import LOGGING_CONFIG
from app.utils.files import save_json_to_file

# Configura logging
logging.config.dictConfig(LOGGING_CONFIG)


class TestFiles:

    def test_save_json_to_file(self, tmpdir):
        # Datos de prueba
        data = [
			{
				"col_1": "",
				"col_2": "",
				"col_3": ""
			},
			{
				"col_1": "Total de votos",
				"col_2": "7,651,270",
				"col_3": "10,660,241"
			},
			{
				"col_1": "Porcentaje",
				"col_2": "20.89%",
				"col_3": "29.10%"
			}   
		]

        data = json.dumps(data, sort_keys=True, indent=4)
        
        # Crear una ruta de archivo temporal proporcionada por pytest
        file_path = tmpdir.join("test.json")
        
        # Llamar a la función
        save_json_to_file(data, file_path)
        
        # Leer el contenido del archivo y verificar
        with open(file_path, 'r') as file:
            result = json.load(file)
        
        # Aserción para verificar que el contenido del archivo es el esperado
        assert result == data
   