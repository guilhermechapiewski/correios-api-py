# encoding: UTF-8
import os
import unittest

from mockito import *

from packtrack.scraping import CorreiosWebsiteScraper
from packtrack.dhl_gm import DhlGmTracker

class CorreiosWebsiteScraperTest(unittest.TestCase):
    
    def test_should_get_data_from_correios_website(self):
        example_file = open('%s/tests/correios_website/exemplo_rastreamento_correios1.html' % os.getcwd())
        sample_html = example_file.read()
        example_file.close()
        
        urllib2_mock = Mock()
        request_mock = Mock()
        when(urllib2_mock).urlopen('http://websro.correios.com.br/sro_bin/txect01$.QueryList?P_ITEMCODE=&P_LINGUA=001&P_TESTE=&P_TIPO=001&P_COD_UNI=ES446391025BR').thenReturn(request_mock)
        when(request_mock).read().thenReturn(sample_html)
        
        correios_website_scraper = CorreiosWebsiteScraper(urllib2_mock)
        encomenda = correios_website_scraper.get_encomenda_info('ES446391025BR')
        assert encomenda.numero == 'ES446391025BR'
        
        assert encomenda.status[0].data == u'27/01/2009 16:35'
        assert encomenda.status[0].local == u'ACF FENIX - ITAPECERICA DA SERRA/SP'
        assert encomenda.status[0].situacao == u'Postado'
        assert encomenda.status[0].detalhes == None
        
        assert encomenda.status[1].data == u'27/01/2009 18:51'
        assert encomenda.status[1].local == u'ACF FENIX - ITAPECERICA DA SERRA/SP'
        assert encomenda.status[1].situacao == u'Encaminhado'
        assert encomenda.status[1].detalhes == u'Em tr\xc3\xa2nsito para CTE JAGUARE - SAO PAULO/SP'
        
        assert encomenda.status[2].data == u'28/01/2009 03:36'
        assert encomenda.status[2].local == u'CTE JAGUARE - SAO PAULO/SP'
        assert encomenda.status[2].situacao == u'Encaminhado'
        assert encomenda.status[2].detalhes == u'Encaminhado para CTE SAUDE - SAO PAULO/SP'
        
        assert encomenda.status[3].data == u'28/01/2009 06:40'
        assert encomenda.status[3].local == u'CTE SAUDE - SAO PAULO/SP'
        assert encomenda.status[3].situacao == u'Encaminhado'
        assert encomenda.status[3].detalhes == u'Encaminhado para CEE MOEMA - SAO PAULO/SP'
        
        assert encomenda.status[4].data == u'28/01/2009 14:17'
        assert encomenda.status[4].local == u'CEE MOEMA - SAO PAULO/SP'
        assert encomenda.status[4].situacao == u'Saiu para entrega'
        assert encomenda.status[4].detalhes == None
        
        assert encomenda.status[5].data == u'28/01/2009 17:49'
        assert encomenda.status[5].local == u'CEE MOEMA - SAO PAULO/SP'
        assert encomenda.status[5].situacao == u'Entregue'
        assert encomenda.status[5].detalhes == None

class DhlGmBaseTest(object):

    expected = {
            'GM555113775306714774': [{
                                'atividade': 'ARRIVAL ORIGIN DHL GLOBAL MAIL FACILITY',
                                'data': '10/11/2012',
                                'hora': '01:18 AM CT',
                                'localizacao': 'Des Plaines, IL'
            }]
    }

class DhlGmTrackerTest(unittest.TestCase, DhlGmBaseTest):

    def setUp(self):
        self.tracker = DhlGmTracker()

    def get_info(self, codigo):
        return self.tracker.track(codigo)

    def assertInfo(self, codigo):

        result = self.get_info(codigo)
        expected = self.expected.get(codigo, [])

        self.assertEqual(len(expected), len(result))

        for e, r in zip(expected, result):
            for key, value in e.itens():
                self.assertIn(key, r)
                self.assertEqual(value, r[key])
