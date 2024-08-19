# scraper/core/scraper.py

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
import logging
import time

class Scraper:
    def __init__(self, driver_path=None, headless=False):
        self.logger = logging.getLogger(__name__)
        self.logger.info("Iniciando Scraper...")

        chrome_options = Options()
        if headless:
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--disable-gpu")
        
        if driver_path:
            self.driver_service = ChromeService(executable_path=driver_path)
        else:
            self.driver_service = ChromeService()

        self.driver = webdriver.Chrome(service=self.driver_service, options=chrome_options)
        self.logger.info("Navegador iniciado correctamente.")

    def open_page(self, url):
        self.logger.info(f"Navegando a la URL: {url}")
        self.driver.get(url)

    def maximize_window(self):
        self.logger.info("Maximizando ventana del navegador.")
        self.driver.maximize_window()                                   

    def close_browser(self):
        self.logger.info("Cerrando navegador.")
        self.driver.quit()
        self.driver = None  

    def wait(self, seconds):
        self.logger.info(f"Esperando {seconds} Segundos.")
        time.sleep(seconds)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close_browser()
