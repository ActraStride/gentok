import pytest
import logging.config
from unittest.mock import patch, MagicMock
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
    # Crea un mock del WebDriver
    mock_driver = MagicMock()
    # Configura un valor simulado para current_url
    mock_driver.current_url = "https://www.google.com/"
    return Scraper(driver=mock_driver)

class TestScraper:

    def test_open_page(self, scraper):
        # Llama al método open_page
        scraper.open_page("https://www.google.com")
        # Verifica que se llamó al método get con la URL correcta
        scraper.driver.get.assert_called_once_with("https://www.google.com")
        # Verifica que la URL actual es la esperada
        assert scraper.driver.current_url == "https://www.google.com/"


    def test_maximize_window(self, caplog, scraper):

        scraper.open_page("https://google.com")
        
        with caplog.at_level(logging.INFO):
            scraper.maximize_window()
            
            # Verifica que se llamó al método maximize_window
            scraper.driver.maximize_window.assert_called_once()
            
            assert "Maximizando ventana del navegador." in caplog.text



    def test_wait(self, caplog, scraper):
        
        scraper.open_page("https://google.com")
        
        with caplog.at_level(logging.INFO):
            scraper.wait(2)
            
            # Aquí, como `wait` probablemente es un `time.sleep`, no es necesario simular nada del driver.
            assert "Esperando 2 Segundos." in caplog.text


    def test_close_browser(self, scraper):
        
        scraper.open_page("https://google.com")
        scraper.wait(2)
        
        with patch.object(scraper.driver, 'quit', wraps=scraper.driver.quit) as mock_quit:
            scraper.close_browser()
            
            # Verifica que el método quit fue llamado
            mock_quit.assert_called_once()
            
            # Verifica que el driver se estableció a None
            assert scraper.driver is None



    def test_get_element(self, scraper):
        # Configura un tipo de búsqueda y un locator
        by = By.ID
        locator = "example"
        mock_element = MagicMock()
        
        # Configura el mock del WebDriver para devolver un elemento simulado
        scraper.driver.find_element.return_value = mock_element
        
        # Llama al método get_element
        element = scraper.get_element(by, locator)
        
        # Verifica que se llamó a find_element con los parámetros correctos
        scraper.driver.find_element.assert_called_once_with(by, locator)
        
        # Verifica que el elemento devuelto es el esperado
        assert element == mock_element

    
    def test_get_element_timeout_exception(self, scraper):
        # Configura el mock para lanzar una excepción TimeoutException
        scraper.driver.find_element.side_effect = TimeoutException
        
        # Verifica que se lanza TimeoutException al buscar el elemento
        with pytest.raises(TimeoutException):
            scraper.get_element(By.ID, "example")

    ## ESCRIBIR PARA EL RESTO DE CASOS DE EXCEPCIONES 

