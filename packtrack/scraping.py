import os
import re
from html.parser import HTMLParser

from bs4 import BeautifulSoup
import requests
from requests.exceptions import RequestException
from zeep import Client as Zeep
from zeep.cache import InMemoryCache
from zeep.transports import Transport

from .correios import Encomenda, Status


class CorreiosWebsiteScraper(object):
    url = os.getenv(
        "CORREIOS_WWW2_URL",
        'https://www2.correios.com.br/sistemas/rastreamento/ctrl/ctrlRastreamento.cfm'
    )
    auth = False

    def __init__(self, http_client=requests, timeout=None):
        self.http_client = http_client
        self.timeout = timeout

    def get_encomenda_info(self, numero):
        data = {
            'acao': 'track',
            'objetos': numero,
            'btnPesq': 'Buscar',
        }
        headers = {
            'Referer': self.url,  # page refuses the call without this referer
            'Content-Type': "application/x-www-form-urlencoded",
        }
        kwargs = {}
        if self.timeout is not None:
            kwargs['timeout'] = self.timeout

        try:
            response = self.http_client.post(
                self.url,
                data=data,
                headers=headers,
                **kwargs)
        except RequestException:
            return None

        html = response.text
        if html:
            encomenda = Encomenda(numero)
            for status in self._get_all_status_from_html(html):
                encomenda.adicionar_status(status)
            return encomenda

    def _text(self, value):
        return BeautifulSoup(value.strip(), 'html.parser').text

    def _get_all_status_from_html(self, html):
        status = []
        html_parser = HTMLParser()
        # O bs4 converte o &nbsp; para \xa0 ao invés de espaço.
        clean_html = html.replace('&nbsp;', ' ')
        soup = BeautifulSoup(clean_html, 'html.parser')
        for tr in soup.select('table.sro tr'):
            try:
                tds = tr.findAll('td')
            except AttributeError:
                continue
            for td in tds:
                content = td.encode_contents().decode().replace('\r', ' ').split('<br/>')
                class_ = td['class']
                if 'sroDtEvent' in class_:
                    data = '%s %s' % (content[0].strip(), content[1].strip())
                    local = '/'.join(self._text(content[2]).rsplit(' / ', 1)).upper()
                elif 'sroLbEvent' in class_:
                    situacao = html_parser.unescape(self._text(content[0]))
                    detalhes = html_parser.unescape(self._text(content[1]))
                    if detalhes:
                        detalhes = u'%s %s' % (situacao, detalhes)
                    status.append(Status(data=data, local=local,
                                         situacao=situacao, detalhes=detalhes))
        return status


class CorreiosRastroService(object):
    url = 'http://webservice.correios.com.br/service/rastro/Rastro.wsdl'
    default_kwargs = {
        "tipo": "L",  # lista de objetos
        "resultado": "T",  # todos os eventos do objeto
        "lingua": "101",  # pt-br
    }
    auth = True

    def __init__(self, timeout=None):
        self.client = Zeep(
            wsdl=self.url,
            transport=Transport(cache=InMemoryCache()),
        )
        if timeout is not None:
            self.client.operation_timeout = self.client.timeout = timeout

    def get_encomenda_info(self, numero, auth=None):
        if auth is None:
            auth = ("ECT", "SRO")

        kwargs = dict(
            self.default_kwargs,
            objetos=numero,
            usuario=auth[0],
            senha=auth[1])

        response = self.client.service.buscaEventos(**kwargs)
        objeto = response.objeto[0]

        encomenda = Encomenda(numero)
        if objeto.erro:
            pass
        else:
            for evento in objeto.evento:
                data = u"{} {}".format(evento.data, evento.hora)
                status = Status(
                    data=data,
                    local=evento.local,
                    situacao=evento.descricao,
                    detalhes=evento.detalhe)
                encomenda.adicionar_status(status)
        return encomenda
