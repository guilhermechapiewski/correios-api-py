import os
import re
from HTMLParser import HTMLParser

from BeautifulSoup import BeautifulSoup
import requests
from requests.exceptions import RequestException
from zeep import Client as Zeep
from zeep.cache import InMemoryCache
from zeep.transports import Transport

from correios import Encomenda, Status


class CorreiosWebsiteScraper(object):
    url = os.getenv(
        "CORREIOS_WWW2_URL",
        'http://www2.correios.com.br/sistemas/rastreamento/resultado_semcontent.cfm'
    )
    auth = False

    def __init__(self, http_client=requests, timeout=None):
        self.http_client = http_client
        self.timeout = timeout

    def get_encomenda_info(self, numero):
        data = {
            'P_LINGUA': '001',
            'P_TIPO': '001',
            'objetos': numero,
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

        html = response.content

        if html:
            try:
                html = html.decode('latin-1')
            except UnicodeDecodeError:
                pass
            encomenda = Encomenda(numero)
            for status in self._get_all_status_from_html(html):
                encomenda.adicionar_status(status)
            return encomenda

    def _text(self, value):
        value = BeautifulSoup(value.strip()).text
        return value.replace('&nbsp;', ' ')

    def _get_all_status_from_html(self, html):
        status = []
        html_parser = HTMLParser()
        if "<table" not in html:
            return status
        html_info = re.search('.*(<table.*</table>).*', html, re.S)
        if not html_info:
            return status

        table = html_info.group(1)
        soup = BeautifulSoup(table)

        for tr in soup.table:
            try:
                tds = tr.findAll('td')
            except AttributeError:
                continue
            for td in tds:
                content = td.renderContents().replace('\r', ' ') \
                    .split('<br />')
                class_ = td['class']
                if class_ == 'sroDtEvent':
                    data = '%s %s' % (content[0].strip(), content[1].strip())
                    local = '/'.join(self._text(content[2]).rsplit(' / ', 1)).upper()
                elif class_ == 'sroLbEvent':
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
