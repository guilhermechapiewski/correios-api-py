from correios import EncomendaRepository

class Correios(object):
    
    encomenda_repository = EncomendaRepository()
    
    @staticmethod
    def encomenda(numero):
        return Correios.encomenda_repository.get(numero)