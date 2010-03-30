import re
import urllib2

from BeautifulSoup import BeautifulSoup

from correios import Encomenda, Status

class CorreiosWebsiteScraper(object):
    
    def __init__(self, http_client=urllib2):
        self.url = 'http://websro.correios.com.br/sro_bin/txect01$.QueryList?P_ITEMCODE=&P_LINGUA=001&P_TESTE=&P_TIPO=001&P_COD_UNI='
        self.http_client = http_client
        
    def get_encomenda_info(self, numero):
        request = self.http_client.urlopen('%s%s' % (self.url, numero))
        html = request.read()
        request.close()
        if html:
            encomenda = Encomenda(numero)
            [encomenda.adicionar_status(status) for status in self._get_all_status_from_html(html)]
            return encomenda
    
    def _get_all_status_from_html(self, html):
        html_info = re.search('.*(<table.*</TABLE>).*', html, re.S)
        table = html_info.group(1)
        
        soup = BeautifulSoup(table)
        
        status = []
        count = 0
        for tr in soup.table:
            if count > 4 and str(tr).strip() != '':
                if re.match(r'\d{2}\/\d{2}\/\d{4} \d{2}:\d{2}', tr.contents[0].string):
                    status.append(
                            Status(data=unicode(tr.contents[0].string),
                                    local=unicode(tr.contents[1].string),
                                    situacao=unicode(tr.contents[2].font.string))
                    )
                else:
                    status[len(status) - 1].detalhes = unicode(tr.contents[0].string)
                    
            count = count + 1
        
        return status