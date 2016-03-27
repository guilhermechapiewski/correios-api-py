import re
import urllib2

from BeautifulSoup import BeautifulSoup

from correios import Encomenda, Status


class CorreiosWebsiteScraper(object):

    def __init__(self, http_client=urllib2):
        self.url = 'http://websro.correios.com.br/sro_bin/txect01$.QueryList?P_ITEMCODE=&P_LINGUA=001&P_TESTE=&P_TIPO=001&P_COD_UNI='
        self.http_client = http_client

    def get_encomenda_info(self, numero):
        url = '%s%s' % (self.url, urllib2.quote(numero))
        try:
            request = self.http_client.urlopen(url)
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

    def _get_all_status_from_html(self, html):
        html_info = re.search('.*(<table.*</TABLE>).*', html, re.S)
        status = []
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
