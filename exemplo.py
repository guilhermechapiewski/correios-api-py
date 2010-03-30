from correios import *

encomenda = Correios.encomenda("ES446391025BR")
print encomenda.numero

for status in encomenda.status:
    print "Data: %s" % status.data
    print "Local: %s" % status.local
    print "Situacao: %s" % status.situacao
    print "Detalhes: %s" % status.detalhes
    print