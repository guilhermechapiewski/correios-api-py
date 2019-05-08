# coding: UTF-8
from setuptools import setup
import sys

install_requires = [
    'requests >= 0.14.2',
    'lxml >= 3.0.0',
    'zeep >= 1.6.0',
]
if sys.version_info >= (3, 0):
    install_requires.append('beautifulsoup4 >= 4.3.2')
else:
    install_requires.append('BeautifulSoup >= 3.1.0')

tests_require = [
    'mockito',
]


setup(
    name='packtrack',
    version='1.6',
    packages=['packtrack'],
    author='Ale Borba',
    author_email='ale.borba@codingforchange.com',
    description='API Python para obter informacoes de encomendas',
    license='LGPLv3',
    keywords='encomendas track api',
    url='https://github.com/aleborba/packtrack',
    long_description='API Python para obter informacoes de encomendas. Para mais detalhes veja a documentacao no Github: https://github.com/aleborba/packtrack/blob/master/README.textile',
    install_requires=install_requires,
    tests_require=tests_require,
)
