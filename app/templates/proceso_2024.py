from app.scraper import Scraper

class Proceso2024(Scraper):

    def __init__(self, driver=None, driver_path=None, headless=False, auto_start=False):
        """
        Constructor para el scraper de un sitio específico.
        """
        super().__init__(driver, driver_path, headless, auto_start)  # Llama al constructor de la clase padre
    
    def mine_presidential_election(self, **kwargs):
        # https://computos2024.ine.mx
        # /html/body
        # /app-root/app-federal/div/div/div/div/div/div/div[4]/app-entidad/div/div/div[2]/app-mapa-diputaciones/div/div/div[4]/div/svg/g[2]/g[1]/g
        self.start_driver()
        self.open_page('https://actradev.com')
        self.wait(5)
        self.close_browser()
        print('🤨🤨🤨')
        pass

    