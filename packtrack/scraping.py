import re
import urllib
import urllib2

from BeautifulSoup import BeautifulSoup
from zeep import Client as Zeep
from zeep.cache import InMemoryCache
from zeep.transports import Transport

from correios import Encomenda, Status


class _CorreiosWebsiteScraperBase(object):

    def __init__(self, http_client=urllib2, timeout=None):
        self.http_client = http_client
        self.timeout = timeout

    def get_encomenda_info(self, numero):
        req = self._req(numero)
        kwargs = {}
        if self.timeout is not None:
            kwargs['timeout'] = self.timeout

        try:
            request = self.http_client.urlopen(req, **kwargs)
        except urllib2.HTTPError:
            return None

        html = request.read()
        request.close()
        if html:
            try:
                html = html.decode('latin-1')
            except UnicodeDecodeError:
                pass
            encomenda = Encomenda(numero)
            for status in self._get_all_status_from_html(html):
                encomenda.adicionar_status(status)
            return encomenda


class CorreiosWebsiteScraper(_CorreiosWebsiteScraperBase):
    url = 'http://www2.correios.com.br/sistemas/rastreamento/resultado.cfm'

    def _req(self, numero):
        data = {
            'P_LINGUA': '001',
            'P_TIPO': '001',
            'objetos': numero,
        }
        headers = {
            'Referer': self.url,  # page refuses the call without this referer
        }
        req = self.http_client.Request(self.url,
                                       data=urllib.urlencode(data),
                                       headers=headers)
        return req

    def _text(self, value):
        value = BeautifulSoup(value.strip()).text
        return value.replace('&nbsp;', ' ')

    def _get_all_status_from_html(self, html):
        status = []
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
                    situacao = self._text(content[0])
                    detalhes = self._text(content[1])
                    if detalhes:
                        detalhes = u'%s %s' % (situacao, detalhes)
                    status.append(Status(data=data, local=local,
                                         situacao=situacao, detalhes=detalhes))
        return status


class CorreiosWebsroScraper(_CorreiosWebsiteScraperBase):
    url = 'http://websro.correios.com.br/sro_bin/txect01$.QueryList?P_ITEMCODE=&P_LINGUA=001&P_TESTE=&P_TIPO=001&P_COD_UNI='

    def _req(self, numero):
        url = '%s%s' % (self.url, numero)
        req = self.http_client.Request(url)
        return req

    def _get_all_status_from_html(self, html):
        status = []
        if "<table" not in html:
            return status
        html_info = re.search('.*(<table.*</TABLE>).*', html, re.S)
        if not html_info:
            return status

        table = html_info.group(1)
        soup = BeautifulSoup(table)

        count = 0
        for tr in soup.table:
            if count > 4 and str(tr).strip() != '':
                content = tr.contents[0].renderContents()
                if re.match(r'\d{2}\/\d{2}\/\d{4} \d{2}:\d{2}', content):
                    status.append(
                        Status(data=unicode(tr.contents[0].string),
                               local=unicode(tr.contents[1].string),
                               situacao=unicode(tr.contents[2].font.string))
                    )
                else:
                    status[len(status) - 1].detalhes = content.decode("utf-8")

            count = count + 1

        return status


class CorreiosRastroService(object):
    url = 'http://webservice.correios.com.br/service/rastro/Rastro.wsdl'
    default_kwargs = {
        "usuario": "ECT",
        "senha": "SRO",
        "tipo": "L",  # lista de objetos
        "resultado": "T",  # todos os eventos do objeto
        "lingua": "101",  # pt-br
    }

    def __init__(self, timeout=None):
        self.client = Zeep(
            wsdl=self.url,
            transport=Transport(cache=InMemoryCache()),
        )
        if timeout is not None:
            self.client.operation_timeout = self.client.timeout = timeout

    def get_encomenda_info(self, numero):
        kwargs = dict(self.default_kwargs, objetos=numero)

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
