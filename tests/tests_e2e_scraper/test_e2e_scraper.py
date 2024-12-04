import pytest
import logging.config
from app.utils import setup_logging
from app.scraper import Scraper
from selenium.webdriver.common.by import By
from selenium.common.exceptions import (
    TimeoutException, 
    ElementClickInterceptedException, 
    StaleElementReferenceException,
    NoSuchElementException,
    ElementNotInteractableException
)



# Configura logging
setup_logging()

@pytest.fixture(autouse=True)
def scraper():
    return Scraper(auto_start=True)


@pytest.mark.e2e
class TestScraperEndToEnd:

    def test_click_element(self, scraper):
        # Navega a la URL donde se encuentra el elemento
        url = "https://www.google.com/"
        scraper.open_page(url)

        try:
            # Encuentra el elemento al que se le hará clic
            element = scraper.get_element(By.XPATH, '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[4]/center/input[2]')
            
            # Espera hasta que el elemento sea clicable y haz clic en él
            scraper.click_element(element)
            
            # Verifica que el click tuvo el efecto esperado (puedes ajustar esta verificación según tu caso)
            assert scraper.driver.current_url == 'https://doodles.google/', 'La URL no es la esperada.'
        
        except TimeoutException:
            pytest.fail('Se agotó el tiempo de espera para que el elemento sea clicable.')
        
        except ElementClickInterceptedException:
            pytest.fail('No se pudo hacer clic en el elemento porque otro elemento lo interceptó.')
        
        except StaleElementReferenceException:
            pytest.fail('El elemento ya no es adjunto al DOM, no se pudo hacer clic.')
        
        except NoSuchElementException:
            pytest.fail('No se encontró el elemento en la página.')
        
        except Exception as e:
            pytest.fail(f'Error inesperado: {str(e)}')
        
        finally:
            # Cierra el navegador al final del test
            scraper.close_browser()


    def test_fill_input(self, scraper):
        # Navega a la URL donde se encuentra el elemento
        url = 'https://www.google.com/'
        scraper.open_page(url)

        try:
            # Intenta obtener el elemento de entrada usando XPATH
            element = scraper.get_element(By.XPATH, '//*[@id="APjFqb"]')

            # Define el contenido que deseas ingresar en el campo de texto
            content = 'RADEX SCRAPER'

            # Intenta rellenar el campo de entrada con el contenido
            scraper.fill_input(element, content)

            # Verifica que el valor en el campo de entrada sea el esperado
            assert element.get_attribute('value') == content, "El campo de entrada no se rellenó correctamente."

        except NoSuchElementException:
            # Maneja el caso donde el elemento no se encuentra en la página
            pytest.fail("El elemento de entrada no se encontró en la página.", pytrace=True)

        except ElementNotInteractableException:
            # Maneja el caso donde el elemento no es interactuable
            pytest.fail("El elemento de entrada no es interactuable.", pytrace=True)

        except TimeoutException:
            # Maneja el caso donde la operación tomó demasiado tiempo
            pytest.fail("La operación tomó demasiado tiempo y falló por un timeout.", pytrace=True)

        except Exception as e:
            # Maneja cualquier otra excepción que pueda ocurrir
            pytest.fail(f"Test falló debido a: {str(e)}", pytrace=True)


    def test_get_html(self, scraper):
        # Navega a la URL donde se encuentra el elemento
        url = 'https://prep2015.ine.mx/Nacional/VotosPorPartido/'
        scraper.open_page(url)

        try:
            
            element = scraper.get_element(By.XPATH, '/html/body/div[2]/div[7]/div[1]/div/section/div/div/div/table[1]')

            html = scraper.get_html(element)

            assert html != None
        
        except Exception as e:
            # Maneja cualquier otra excepción que pueda ocurrir
            pytest.fail(f"Test falló debido a: {str(e)}", pytrace=True)
