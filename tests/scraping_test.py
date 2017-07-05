# encoding: UTF-8
import os
import unittest

import mock

from packtrack.scraping import CorreiosWebsiteScraper
from packtrack.dhl_gm import DhlGmTracker


class CorreiosWebsiteScraperTest(unittest.TestCase):

    def _assert_status(self, status, data, local, situacao, detalhes):
        self.assertEqual(data, status.data)
        self.assertEqual(local, status.local)
        self.assertEqual(situacao, status.situacao)
        self.assertEqual(detalhes, status.detalhes)

    def test_should_get_data_from_correios_website(self):
        example_file = open('%s/tests/correios_website/exemplo_rastreamento_correios1.html' % os.getcwd())
        sample_html = example_file.read()
        example_file.close()

        http_client_mock = mock.Mock()
        response_mock = mock.Mock()
        http_client_mock.post.return_value = response_mock
        response_mock.content = sample_html

        correios_website_scraper = CorreiosWebsiteScraper(http_client_mock)
        numero = 'PJ859656941BR'
        encomenda = correios_website_scraper.get_encomenda_info(numero)
        self.assertEqual(numero, encomenda.numero)

        detalhes = u'Objeto encaminhado de Unidade Operacional em Sao Paulo / SP para Unidade de Distribuição em SAO JOSE DOS CAMPOS / SP'
        self._assert_status(encomenda.status[0], u'01/07/2016 15:51',
                            u'SAO PAULO/SP', u'Objeto encaminhado', detalhes)

        self._assert_status(encomenda.status[1], u'07/06/2016 13:17',
                            u'SANTO ANDRE/SP', u'Objeto postado', u'')

        detalhes = u'Objeto encaminhado de Agéncia dos Correios em Santo Andre / SP para Unidade Operacional em Sao Paulo / SP'
        self._assert_status(encomenda.status[2], u'07/06/2016 13:55',
                            u'SANTO ANDRE/SP', u'Objeto encaminhado', detalhes)


class CorreiosTimeoutTest(unittest.TestCase):

    def test_timeout_undefined(self):

        http_client_mock = mock.Mock()
        response_mock = mock.Mock()
        http_client_mock.post.return_value = response_mock
        response_mock.content = ''
        TIMEOUT = 3
        scraper = CorreiosWebsiteScraper(http_client_mock, timeout=TIMEOUT)
        scraper.get_encomenda_info('ES446391025BR')
        assert http_client_mock.post.call_args[1]['timeout'] == 3


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
