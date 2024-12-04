# app/scraper/scraper.py

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import (
    TimeoutException, 
    ElementClickInterceptedException, 
    StaleElementReferenceException,
    NoSuchElementException,
    ElementNotInteractableException
)
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import logging
import time
# from app.utils.logging_setup import setup_logging

class Scraper:

    # Constructor que inicializa el scraper y configura el driver de Chrome.
    def __init__(self, driver=None, driver_path=None, headless=False, auto_start=False):
        """
        Inicializa la clase Scraper, pero no el navegador a menos que `auto_start` sea True.
        """
        self.logger = logging.getLogger(__name__)
        self.logger.info("Iniciando Scraper...")

        self.driver = driver  # Almacena un controlador existente si se proporciona
        self.driver_path = driver_path  # Ruta del driver (si aplica)
        self.headless = headless  # Modo sin interfaz gráfica
        self.driver_service = None  # Servicio de Chrome (inicializado más tarde)

        # Si auto_start es True, inicia el navegador inmediatamente
        if auto_start:
            self.start_driver()
        else:
            self.logger.info("Navegador no iniciado automáticamente.")
            

    def start_driver(self):
        """
        Inicializa el navegador cuando sea necesario.
        """
        if self.driver:
            self.logger.warning("El navegador ya está iniciado.")
            return

        chrome_options = Options()
        if self.headless:
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--disable-gpu")

        # Configura el servicio de ChromeDriver
        if self.driver_path:
            self.driver_service = ChromeService(executable_path=self.driver_path)
        else:
            self.driver_service = ChromeService()  # Usa el PATH por defecto

        self.driver = webdriver.Chrome(service=self.driver_service, options=chrome_options)
        self.logger.info("Navegador iniciado correctamente.")



    # Método para abrir una página web a partir de una URL.
    def open_page(self, url):
        self.logger.info(f"Navegando a la URL: {url}")
        self.driver.get(url)

    # Método para maximizar la ventana del navegador.
    def maximize_window(self):
        self.logger.info("Maximizando ventana del navegador.")
        self.driver.maximize_window()

    # Método para cerrar el navegador y liberar el recurso del driver.
    def close_browser(self):
        self.logger.info("Cerrando navegador.")
        self.driver.quit()  # Cierra el navegador y finaliza la sesión.
        self.driver = None  # Limpia la referencia al driver.



    # Método para esperar una cantidad específica de segundos.
    def wait(self, seconds):
        self.logger.info(f"Esperando {seconds} Segundos.")
        time.sleep(seconds)  # Pausa la ejecución durante el tiempo especificado.


    # Método para obtener un elemento de la página con un tiempo de espera determinado.
    def get_element(self, by, locator, timeout=1):
        try:
            # Espera hasta que el elemento esté presente en el DOM, dentro del tiempo 'timeout'.
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, locator))
            )
            return element  # Devuelve el elemento encontrado.
        
        # Manejo de excepción cuando se agota el tiempo de espera para encontrar el elemento.
        except TimeoutException:
            self.logger.error(f"Error: Se agotó el tiempo de espera al buscar el elemento con {by} = '{locator}'")
            raise
        
        # Manejo de excepción cuando el elemento no se encuentra.
        except NoSuchElementException:
            self.logger.error(f"Error: No se encontró el elemento con {by} = '{locator}'")
            raise
        
        # Manejo de cualquier otra excepción que ocurra durante la búsqueda del elemento.
        except Exception as e:
            self.logger.critical(f"Error inesperado: {str(e)}")
            raise

    # Método para hacer clic en un elemento, asegurándose de que sea clicable.
    def click_element(self, element, timeout=5):
        try:
            # Espera hasta que el elemento sea clicable, dentro del tiempo 'timeout'.
            WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable(element))
            
            # Intenta hacer clic en el elemento.
            element.click()
            self.logger.info("El elemento fue clicado exitosamente.")
        
        # Manejo de excepción cuando se agota el tiempo de espera para que el elemento sea clicable.
        except TimeoutException:
            self.logger.error("Error: Se agotó el tiempo de espera para que el elemento sea clicable.")
            raise
        
        # Manejo de excepción cuando otro elemento intercepta el clic.
        except ElementClickInterceptedException:
            self.logger.error("Error: No se pudo hacer clic en el elemento porque otro elemento lo interceptó.")
            raise
        
        # Manejo de excepción cuando el elemento ya no está adjunto al DOM.
        except StaleElementReferenceException:
            self.logger.error("Error: El elemento ya no es adjunto al DOM, no se pudo hacer clic.")
            raise
        
        # Manejo de cualquier otra excepción durante la interacción con el elemento.
        except Exception as e:
            self.logger.critical(f"Error inesperado al intentar hacer clic en el elemento: {str(e)}")
            raise

    # Método para llenar un campo de entrada con texto.
    def fill_input(self, element, content):
        try:
            # Limpia el campo de entrada antes de escribir.
            element.clear()
            
            # Escribe el contenido especificado en el campo de entrada.
            element.send_keys(content)
        
        # Manejo de excepción cuando el elemento de entrada no se encuentra.
        except NoSuchElementException:
            self.logger.error("El elemento de entrada no se encontró en la página.")
            raise 
        
        # Manejo de excepción cuando el elemento de entrada no es interactuable.
        except ElementNotInteractableException:
            self.logger.error("El elemento de entrada no es interactuable.")
            raise 

        # Manejo de excepción cuando la operación tarda demasiado y genera un timeout.
        except TimeoutException:
            self.logger.error("La operación tomó demasiado tiempo y falló por un timeout.")
            raise 

        # Manejo de cualquier otra excepción que ocurra durante el llenado del campo.
        except Exception as e:
            self.logger.critical(f"Error al intentar rellenar el campo de entrada: {str(e)}")
            raise


    # Método para procesar las opciones de un elemento <select>.
    # Aplica un callback a cada opción dentro del select.
    def process_select(self, select_element, callback):
        # Crear un objeto Select que represente el elemento <select>.
        select = Select(select_element)

        # Iterar sobre cada opción dentro del <select> y aplicar el callback.
        for option in select.options:
            try:
                callback(option)  # Ejecuta el callback en cada opción del select.
            except Exception as e:
                # Si ocurre un error al procesar una opción, se captura y se muestra.
                print(f"Error processing option {option.text}: {e}")

    # Método para obtener el HTML de un elemento de la página.
    def get_html(self, element):
        try:
            # Intentar obtener el atributo 'outerHTML' del elemento, que contiene su HTML completo.
            element_html = element.get_attribute('outerHTML')
            self.logger.info(f'Se obtuvo el Código: {element_html}')  # Registra el HTML obtenido.
            return element_html
        except AttributeError as e:
            # Si ocurre un AttributeError, significa que el elemento no tiene el método get_attribute.
            self.logger.error(f'Error al obtener outerHTML del elemento: {e}')
            return None  # Devuelve None si ocurre un error.
        except Exception as e:
            # Manejo general para cualquier otro tipo de excepción.
            self.logger.error(f'Error inesperado al obtener outerHTML del elemento: {e}')
            return None  # Devuelve None si ocurre un error inesperado.

    # Método especial para usar el scraper dentro de un bloque 'with'.
    def __enter__(self):
        return self  # Retorna la instancia del scraper para que pueda ser usada en el bloque 'with'.

    # Método especial para manejar la salida de un bloque 'with'.
    def __exit__(self, exc_type, exc_value, traceback):
        self.close_browser()  # Cierra el navegador automáticamente al finalizar el bloque 'with'.
