import pytest
import logging.config
from unittest.mock import patch, MagicMock
from settings import LOGGING_CONFIG
from app.scraper.scraper import Scraper

# Configura logging
logging.config.dictConfig(LOGGING_CONFIG)

@pytest.fixture
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


    def test_maximize_window(self, caplog):
        mock_driver = MagicMock()
        scraper = Scraper(mock_driver)
        
        scraper.open_page("https://google.com")
        
        with caplog.at_level(logging.INFO):
            scraper.maximize_window()
            
            # Verifica que se llamó al método maximize_window
            mock_driver.maximize_window.assert_called_once()
            
            assert "Maximizando ventana del navegador." in caplog.text



    def test_wait(self, caplog):
        mock_driver = MagicMock()
        scraper = Scraper(mock_driver)
        
        scraper.open_page("https://google.com")
        
        with caplog.at_level(logging.INFO):
            scraper.wait(2)
            
            # Aquí, como `wait` probablemente es un `time.sleep`, no es necesario simular nada del driver.
            assert "Esperando 2 Segundos." in caplog.text


    def test_close_browser(self):
        mock_driver = MagicMock()
        scraper = Scraper(mock_driver)
        
        scraper.open_page("https://google.com")
        scraper.wait(2)
        
        with patch.object(scraper.driver, 'quit', wraps=scraper.driver.quit) as mock_quit:
            scraper.close_browser()
            
            # Verifica que el método quit fue llamado
            mock_quit.assert_called_once()
            
            # Verifica que el driver se estableció a None
            assert scraper.driver is None



    def test_get_element(self, scraper):
        pass
        
