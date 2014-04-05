from correios import EncomendaRepository
from royal import RoyalMail
from dhl_gm import DhlGmTracker

class Correios(object):
    
    encomenda_repository = EncomendaRepository()
    
    @staticmethod
    def track(numero):
        return Correios.encomenda_repository.get(numero)


class Royal(object):
    
    royal = RoyalMail()

    @staticmethod
    def track(numero):
        return Royal.royal.get(numero)


class DhlGm(object):

    dhl = DhlGmTracker()

    @staticmethod
    def track(numero):
        return DhlGm.dhl.get(numero)
