class EncomendaRepository(object):
        
    def __init__(self):
        from scraping import CorreiosWebsiteScraper
        self.correios_website_scraper = CorreiosWebsiteScraper()
    
    def get(self, numero):
        return self.correios_website_scraper.get_encomenda_info(numero)

class Encomenda(object):
    
    def __init__(self, numero):
        self.numero = numero
        self.status = []
    
    def adicionar_status(self, status):
        self.status.append(status)
        self.status.sort(lambda x, y: 1 if x.data > y.data else -1)
    
    def ultimo_status_disponivel(self):
        return self.status[len(self.status) - 1] if len(self.status) > 0 else None

    def primeiro_status_disponivel(self):
        return self.status[0] if len(self.status) > 0 else None

class Status(object):
    
    def __init__(self, **kwargs):
        self.data = kwargs.get('data')
        self.local = kwargs.get('local')
        self.situacao = kwargs.get('situacao')
        self.detalhes = kwargs.get('detalhes')
