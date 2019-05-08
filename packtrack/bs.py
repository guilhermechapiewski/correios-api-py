import functools

try:
    from bs4 import BeautifulSoup
except ImportError:
    from BeautifulSoup import BeautifulSoup


BeautifulSoup = functools.partial(BeautifulSoup, features="lxml")
