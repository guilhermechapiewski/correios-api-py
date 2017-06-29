# coding: utf-8
class EncomendaRepository(object):
    def __init__(self, backend=None):
        self.correios_website_scraper = self._init_scraper(backend)

    def get(self, numero, auth=None):
        func = self.correios_website_scraper.get_encomenda_info
        kwargs = {}
        if self.correios_website_scraper.auth:
            kwargs['auth'] = auth
        return func(numero, **kwargs)

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


class Status(dict):

    def __init__(self, **kwargs):
        self.data = kwargs.pop('data', None)
        self.local = kwargs.pop('local', None)
        self.situacao = kwargs.pop('situacao', None)
        self.detalhes = kwargs.pop('detalhes', None)
        self.update(kwargs)

    def __getattr__(self, key):
        return self[key]

    def __setattr__(self, key, value):
        self[key] = value
