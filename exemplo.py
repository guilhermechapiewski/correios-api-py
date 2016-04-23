from correios import Correios

try:
  encomenda = Correios.encomenda("PJ514632791BR")
  for status in encomenda.status:
      print "Data: %s" % status.data
      print "Local: %s" % status.local
      print "Situacao: %s" % status.situacao
      print "Detalhes: %s" % status.detalhes
      print
except Exception as e:
  print e