from correios import EncomendaRepository
from royal import RoyalMail
from dhl_gm import DhlGmTracker


class Correios(object):

    encomenda_repository = None

    _backends = {
        None: EncomendaRepository(),
    }

    @classmethod
    def track(cls, numero, backend=None, auth=None):
        if backend is None and cls.encomenda_repository:
            return cls.encomenda_repository

        try:
            repository = cls._backends[backend]
        except KeyError:
            repository = EncomendaRepository(backend)
            cls._backends[backend] = repository

        return repository.get(numero, auth=auth)


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
