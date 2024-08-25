import pytest
import logging.config
from settings import LOGGING_CONFIG
from app.scraper.scraper import Scraper
from selenium.webdriver.common.by import By
from selenium.common.exceptions import (
    TimeoutException, 
    ElementClickInterceptedException, 
    StaleElementReferenceException,
    NoSuchElementException
)



# Configura logging
logging.config.dictConfig(LOGGING_CONFIG)

@pytest.fixture(autouse=True)
def scraper():
    return Scraper()


@pytest.mark.e2e
class TestScraperEndToEnd:
    def test_click_element(self, scraper):
        
        
        # Navega a la URL donde se encuentra el elemento
        url = "https://www.google.com/"
        scraper.open_page(url)

        try:
            # Encuentra el elemento al que se le hará clic
            element = scraper.get_element(By.XPATH, "/html/body/div[1]/div[3]/form/div[1]/div[1]/div[4]/center/input[2]")
            
            # Espera hasta que el elemento sea clicable y haz clic en él
            scraper.click_element(element)
            
            # Verifica que el click tuvo el efecto esperado (puedes ajustar esta verificación según tu caso)
            assert scraper.driver.current_url == "https://doodles.google/", "La URL no es la esperada."
        
        except TimeoutException:
            pytest.fail("Se agotó el tiempo de espera para que el elemento sea clicable.")
        
        except ElementClickInterceptedException:
            pytest.fail("No se pudo hacer clic en el elemento porque otro elemento lo interceptó.")
        
        except StaleElementReferenceException:
            pytest.fail("El elemento ya no es adjunto al DOM, no se pudo hacer clic.")
        
        except NoSuchElementException:
            pytest.fail("No se encontró el elemento en la página.")
        
        except Exception as e:
            pytest.fail(f"Error inesperado: {str(e)}")
        
        finally:
            # Cierra el navegador al final del test
            scraper.close_browser()