class EncomendaRepository(object):
    
    correios_website_scraper = None
    
    def get(self, numero):
        return self.correios_website_scraper.get_encomenda_info(numero)

class Encomenda(object):
    
    def __init__(self, **kwargs):
        self.data = kwargs.get('data')
        self.local = kwargs.get('local')
        self.situacao = kwargs.get('situacao')
        self.detalhes = kwargs.get('detalhes')
