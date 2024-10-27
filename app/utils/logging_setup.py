# app/utils/logging_setup.py

import logging.config
from pathlib import Path

# Constantes
LOG_DIR_NAME = 'logs'
LOG_FILE_NAME = 'application.log'
LOG_FORMAT = '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
LOG_LEVEL_FILE = 'INFO'
LOG_LEVEL_CONSOLE = 'DEBUG'

# Definir el directorio para los logs
LOG_DIR = Path(__file__).resolve().parent.parent.parent / LOG_DIR_NAME  # Dos niveles hacia arriba

try:
    # Definir el directorio para los logs en la raíz del proyecto
    LOG_DIR.mkdir(exist_ok=True)
except OSError as e:
    print(f"Error creando el directorio de logs: {e}")

# Configuración de logging
LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': LOG_FORMAT
        },
    },
    'handlers': {
        'file_handler': {
            'level': LOG_LEVEL_FILE,
            'formatter': 'standard',
            'class': 'logging.FileHandler',
            'filename': LOG_DIR / LOG_FILE_NAME,
        },
        'console': {
            'level': LOG_LEVEL_CONSOLE,
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        '': {  # Logger raíz
            'handlers': ['file_handler', 'console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

def setup_logging():
    """Configura el logging según LOGGING_CONFIG si aún no está configurado."""
    if not logging.getLogger().hasHandlers():
        try:
            logging.config.dictConfig(LOGGING_CONFIG)
            print(f"AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
            logging.getLogger().info("Logging configurado correctamente.")
        except Exception as e:
            print(f"Error configurando el logging: {e}")

