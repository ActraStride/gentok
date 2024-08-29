# run_scraper.py

import logging.config
from settings import LOGGING_CONFIG
from app.scraper import Scraper

# Configura logging
logging.config.dictConfig(LOGGING_CONFIG)

def main():

    logger = logging.getLogger(__name__)
    logger.info('Esto es un mensaje de prueba para el archivo de log.')
    # Código principal para ejecutar el scraper
    with Scraper() as scraper:
        scraper.open_page("https://google.com")
        scraper.wait(2)
        scraper.maximize_window()
        # Realizar otras acciones

if __name__ == "__main__":
    main()
