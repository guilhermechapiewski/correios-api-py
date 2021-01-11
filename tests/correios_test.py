import unittest
from unittest.mock import Mock

from packtrack.correios import Encomenda, Status, EncomendaRepository


class EncomendaRepositoryTest(unittest.TestCase):
    
    def test_should_get_encomenda_by_numero(self):
        encomenda_123 = Status(data='2009-01-28 17:49:00')

        correios_website_scraper_mock = Mock()
        correios_website_scraper_mock.get_encomenda_info.return_value = encomenda_123

        repository = EncomendaRepository()
        repository.correios_website_scraper = correios_website_scraper_mock
        encomenda = repository.get('123')
        assert encomenda
        assert encomenda.data == '2009-01-28 17:49:00'
        correios_website_scraper_mock.get_encomenda_info.assert_called_with('123', auth=None)

    def test_select_default_backend(self):
        repository = EncomendaRepository()
        self.assertEqual('CorreiosWebsiteScraper',
                         repository.correios_website_scraper.__class__.__name__)

    def test_select_www2_backend(self):
        repository = EncomendaRepository(backend='www2')
        self.assertEqual('CorreiosWebsiteScraper',
                         repository.correios_website_scraper.__class__.__name__)


class EncomendaTest(unittest.TestCase):
    
    def test_should_inform_last_status_available(self):
        encomenda = Encomenda(numero='123')
        encomenda.adicionar_status(Status(data='2009-01-28 17:49:00', local='L1', situacao='Encaminhado'))
        encomenda.adicionar_status(Status(data='2009-01-29 17:49:00', local='L1', situacao='Encaminhado'))
        encomenda.adicionar_status(Status(data='2009-01-30 17:49:00', local='L1', situacao='Encaminhado'))
        
        assert encomenda.ultimo_status_disponivel().data == '2009-01-30 17:49:00'
    
    def test_should_inform_first_status_available(self):
        encomenda = Encomenda(numero='123')
        encomenda.adicionar_status(Status(data='2009-01-28 17:49:00', local='L1', situacao='Encaminhado'))
        encomenda.adicionar_status(Status(data='2009-01-29 17:49:00', local='L1', situacao='Encaminhado'))
        encomenda.adicionar_status(Status(data='2009-01-30 17:49:00', local='L1', situacao='Encaminhado'))

        assert encomenda.primeiro_status_disponivel().data == '2009-01-28 17:49:00'
    
    def test_should_return_none_when_theres_no_status_available(self):
        encomenda = Encomenda(numero='123')
        assert encomenda.primeiro_status_disponivel() is None
        assert encomenda.ultimo_status_disponivel() is None

class StatusTest(unittest.TestCase):
    
    def test_should_build_new_instance_with_kwargs(self):
        status = Status(data='2009-01-28 17:49:00', 
                local='CEE MOEMA - SAO PAULO/SP', 
                situacao='Encaminhado', 
                detalhes='Encaminhado para CEE MOEMA')
        
        assert status.data == '2009-01-28 17:49:00'
        assert status.local == 'CEE MOEMA - SAO PAULO/SP'
        assert status.situacao == 'Encaminhado'
        assert status.detalhes == 'Encaminhado para CEE MOEMA'
