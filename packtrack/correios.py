# coding: utf-8
class EncomendaRepository(object):

    def __init__(self, backend=None):
        self.correios_website_scraper = self._init_scraper(backend)

    def get(self, numero):
        return self.correios_website_scraper.get_encomenda_info(numero)

    def _init_scraper(self, backend):
        from scraping import CorreiosWebsiteScraper, CorreiosWebsroScraper, \
            CorreiosRastroService
        if backend is None:
            # usa websro como default, que é mais eficiente
            backend = 'websro'

        backends = {
            'websro': CorreiosWebsroScraper,
            'www2': CorreiosWebsiteScraper,
            'service': CorreiosRastroService,
        }
        Scraper = backends[backend]
        return Scraper()


class Encomenda(object):

    def __init__(self, numero):
        self.numero = numero
        self.status = []

    def adicionar_status(self, status):
        self.status.append(status)
        self.status.sort(lambda x, y: 1 if x.data > y.data else -1)

    def ultimo_status_disponivel(self):
        return self.status[-1] if self.status else None

    def primeiro_status_disponivel(self):
        return self.status[0] if self.status else None


class Status(object):

    def __init__(self, **kwargs):
        self.data = kwargs.get('data')
        self.local = kwargs.get('local')
        self.situacao = kwargs.get('situacao')
        self.detalhes = kwargs.get('detalhes')
