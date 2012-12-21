# coding: UTF-8
from setuptools import setup

setup(
    name = 'packtrack',
    version = '0.1.0',
    packages = ['correios', 'dhl_gm'],
    author = 'Ale Borba',
    author_email = 'ale.borba@codingforchange.com',
    description = 'API Python para obter informacoes de encomendas',
    license = 'LGPLv3',
    keywords = 'encomendas track api',
    url = 'https://github.com/aleborba/packtrack',
    long_description = 'API Python para obter informacoes de encomendas. Para mais detalhes veja a documentacao no Github: https://github.com/aleborba/packtrack/blob/master/README.textile',
    install_requires = ['BeautifulSoup >= 3.1.0', 'requests >= 0.14.2'],
)
