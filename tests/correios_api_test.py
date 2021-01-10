from unittest import TestCase
from unittest.mock import Mock

from packtrack import Correios


class CorreiosTest(TestCase):

    def test_should_use_repository_to_get_encomenda(self):
        encomenda_repository_mock = Mock()
        encomenda_repository_mock.get.return_value = 'encomenda123'
        Correios._backends[None] = encomenda_repository_mock

        assert Correios.track('123') == 'encomenda123'
        encomenda_repository_mock.get.assert_called_with('123', auth=None)

    def test_service_should_receive_auth(self):
        auth = ('mi', 'mimi')
        encomenda_repository_mock = Mock()
        encomenda_repository_mock.get.return_value = 'encomenda123'
        Correios._backends['service'] = encomenda_repository_mock

        assert Correios.track(
            '123', backend='service', auth=auth) == 'encomenda123'
        encomenda_repository_mock.get.assert_called_with('123', auth=auth)
