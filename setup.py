# coding: UTF-8
from setuptools import setup

setup(
    name = 'correios-api-py',
    version = '0.1.1',
    packages = ['correios'],
    author = 'Guilherme Chapiewski',
    author_email = 'guilherme.chapiewski@gmail.com',
    description = 'API Python para obter informacoes de encomendas/Sedex dos Correios.',
    license = 'Apache License 2.0',
    keywords = 'correios brasil api',
    url = 'http://github.com/guilhermechapiewski/correios-api-py/',
    long_description = 'API Python para obter informacoes de encomendas/Sedex dos Correios. Para mais detalhes veja a documentacao no Github: http://github.com/guilhermechapiewski/correios-api-py/blob/master/README.textile',
    install_requires = ['BeautifulSoup >= 3.1.0'],
)
