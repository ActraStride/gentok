# scraper/core/scraper.py

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import (
    TimeoutException, 
    ElementClickInterceptedException, 
    StaleElementReferenceException,
    NoSuchElementException
)
from selenium.webdriver.common.by import By
import logging
import time

class Scraper:
    def __init__(self, driver=None, driver_path=None, headless=False):
        self.logger = logging.getLogger(__name__)
        self.logger.info("Iniciando Scraper...")

        chrome_options = Options()
        if headless:
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--disable-gpu")
        
        if driver:
            self.driver = driver
        else:
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

    def get_element(self, by, locator, timeout=1):
        try:
            # Esperar hasta que el elemento esté presente
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, locator))
            )
            return element
        except TimeoutException:
            self.logger.error(f"Error: Se agotó el tiempo de espera al buscar el elemento con {by} = '{locator}'")
            raise
        except NoSuchElementException:
            self.logger.error(f"Error: No se encontró el elemento con {by} = '{locator}'")
            raise
        except Exception as e:
            self.logger.critical(f"Error inesperado: {str(e)}")
            raise
        

    def click_element(self, element, timeout=5):
        try:
            # Esperar hasta que el elemento sea clicable
            WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable(element))
            
            # Intentar hacer clic en el elemento
            element.click()
            self.logger.info("El elemento fue clicado exitosamente.")
        except TimeoutException:
            self.logger.error("Error: Se agotó el tiempo de espera para que el elemento sea clicable.")
            raise
        except ElementClickInterceptedException:
            self.logger.error("Error: No se pudo hacer clic en el elemento porque otro elemento lo interceptó.")
            raise
        except StaleElementReferenceException:
            self.logger.error("Error: El elemento ya no es adjunto al DOM, no se pudo hacer clic.")
            raise
        except Exception as e:
            self.logger.critical(f"Error inesperado al intentar hacer clic en el elemento: {str(e)}")
            raise

    

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close_browser()
