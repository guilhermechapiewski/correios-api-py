# coding: utf-8
from datetime import datetime
import re


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
        from scraping import CorreiosWebsiteScraper, CorreiosRastroService
        if backend is None:
            backend = 'www2'

        backends = {
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
        d = datetime
        self.status.append(status)
        t_format = self.validar_data(status.data)
        self.status.sort(lambda x, y: 1 if d.strptime(x.data, t_format) > d.strptime(y.data, t_format) else -1)

    def validar_data(self, data):
        if re.match('^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$', data):
            return '%Y-%m-%d %H:%M:%S'
        if re.match('^\d{2}/\d{2}/\d{4} \d{2}:\d{2}$', data):
            return '%d/%m/%Y %H:%M'
        raise ValueError('Formato de data desconhecido: {}'.format(data))

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
