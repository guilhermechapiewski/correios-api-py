import unittest

from mockito import *

from correios import Correios

class CorreiosTest(unittest.TestCase):
    
    def test_should_use_repository_to_get_encomenda(self):
        encomenda_repository_mock = Mock()
        when(encomenda_repository_mock).get('123').thenReturn('encomenda123')
        
        Correios.encomenda_repository = encomenda_repository_mock
        
        assert Correios.encomenda('123') == 'encomenda123'