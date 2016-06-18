import unittest

from mockito import when, Mock

from packtrack import Correios


class CorreiosTest(unittest.TestCase):

    def test_should_use_repository_to_get_encomenda(self):
        encomenda_repository_mock = Mock()
        when(encomenda_repository_mock).get('123').thenReturn('encomenda123')

        Correios._backends[None] = encomenda_repository_mock

        assert Correios.track('123') == 'encomenda123'
