import requests
import re

class DhlGmTracker():
    
    def __init__(self):
        self.url = 'http://webtrack.dhlglobalmail.com/?mobile=&trackingnumber='
        
    def _get_infos_(self, codigo):
        from lxml.html import fromstring

        response = requests.get(self.url+codigo)
        html = fromstring(response.text)
        tabela = html.cssselect("#tracking_table")

        resultado = []

        for tb in tabela:
            tbody = tb.find('tbody')

        tr = tbody.findall('tr')

        for linha in tr:
            resultado.append([a.text for a in linha.findall('td')])

        return resultado

    def get(self, codigo):
        itens = self._get_infos_(codigo)
        result = []

        for item in itens:

            data = dict()
            key = ['data', 'hora', 'local', 'atividade']

            count = 0

            for value in item:

                value = re.sub('\s+', ' ', value.strip())

                data[key[count]] = value
                count = count + 1

            result.append(data)

        return result
