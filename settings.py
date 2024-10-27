import logging
import logging.config
from pathlib import Path

# Constantes
LOG_DIR_NAME = 'logs'
LOG_FILE_NAME = 'application.log'
LOG_FORMAT = '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
LOG_LEVEL_FILE = 'INFO'
LOG_LEVEL_CONSOLE = 'DEBUG'

# Definir el directorio para los logs
LOG_DIR = Path(__file__).resolve().parent / LOG_DIR_NAME
try:
    LOG_DIR.mkdir(exist_ok=True)
except OSError as e:
    print(f"Error creando el directorio de logs: {e}")

# Configuración de los formateadores
formatters = {
    'standard': {
        'format': LOG_FORMAT
    },
}

# Configuración de los manejadores (handlers)
handlers = {
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
}

# Configuración de los loggers
loggers = {
    '': {
        'handlers': ['file_handler', 'console'],
        'level': 'DEBUG',
        'propagate': True,
    },
}

# Configuración completa de logging
LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': formatters,
    'handlers': handlers,
    'loggers': loggers,
}

# Aplicar la configuración
logging.config.dictConfig(LOGGING_CONFIG)
