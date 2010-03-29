import unittest

from mockito import *

from correios.correios import Encomenda, EncomendaRepository

class EncomendaRepositoryTest(unittest.TestCase):
    
    def test_should_get_encomenda_by_numero(self):
        encomenda_123 = Encomenda(data='2009-01-28 17:49:00')
        
        correios_website_scraper_mock = Mock()
        when(correios_website_scraper_mock).get_encomenda_info('123').thenReturn(encomenda_123)
        
        repository = EncomendaRepository()
        repository.correios_website_scraper = correios_website_scraper_mock
        encomenda = repository.get('123')
        assert encomenda
        assert encomenda.data == '2009-01-28 17:49:00'

class EncomendaTest(unittest.TestCase):
    
    def test_should_build_new_instance_with_kwargs(self):
        encomenda = Encomenda(data='2009-01-28 17:49:00', 
                local='CEE MOEMA - SAO PAULO/SP', 
                situacao='Encaminhado', 
                detalhes='Encaminhado para CEE MOEMA')
        
        assert encomenda.data == '2009-01-28 17:49:00'
        assert encomenda.local == 'CEE MOEMA - SAO PAULO/SP'
        assert encomenda.situacao == 'Encaminhado'
        assert encomenda.detalhes == 'Encaminhado para CEE MOEMA'
