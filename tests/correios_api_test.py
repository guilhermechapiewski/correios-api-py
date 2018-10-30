import unittest

from mock import Mock
from mockito import when

from packtrack import Correios


class CorreiosTest(unittest.TestCase):

    def test_should_use_repository_to_get_encomenda(self):
        encomenda_repository_mock = Mock()
        when(encomenda_repository_mock).get('123', auth=None) \
            .thenReturn('encomenda123')

        Correios._backends[None] = encomenda_repository_mock

        assert Correios.track('123') == 'encomenda123'

    def test_service_should_receive_auth(self):
        auth = ('mi', 'mimi')
        encomenda_repository_mock = Mock()
        when(encomenda_repository_mock).get('123', auth=auth) \
            .thenReturn('encomenda123')

        Correios._backends['service'] = encomenda_repository_mock

        assert Correios.track(
            '123', backend='service', auth=auth) == 'encomenda123'
