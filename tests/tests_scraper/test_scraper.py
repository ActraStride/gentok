import pytest
import logging.config
from unittest.mock import patch, MagicMock
from settings import LOGGING_CONFIG
from app.scraper.scraper import Scraper

# Configura logging
logging.config.dictConfig(LOGGING_CONFIG)

@pytest.fixture
def scraper():
    # Crea una instancia de Scraper para usar en las pruebas
    return Scraper()

class TestScraper:

    def test_open_page(self, scraper):
        scraper.open_page("https://www.google.com")
        assert scraper.driver.current_url == "https://www.google.com/"

    def test_maximize_window(self, scraper, caplog):
        scraper.open_page("https://google.com")
        with caplog.at_level(logging.INFO):
            scraper.maximize_window()
            assert "Maximizando ventana del navegador." in caplog.text


    def test_wait(self, scraper, caplog):
        scraper.open_page("https://google.com")
        with caplog.at_level(logging.INFO):
            scraper.wait(2)
            assert "Esperando 2 Segundos." in caplog.text

    def test_close_browser(self, scraper):
        with patch.object(scraper.driver, 'quit') as mock_quit:
            scraper.open_page("https://google.com")
            scraper.wait(2)
            scraper.close_browser()
            mock_quit.assert_called_once()
            assert scraper.driver is None
