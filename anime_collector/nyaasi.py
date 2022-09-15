"""
bs4-based parser for nyaa (nyaa.si)
"""
from urllib.parse import quote

import requests
from bs4 import BeautifulSoup

from anime_collector import requests_headers

url_base = 'https://nyaa.si'
url_search_rss = url_base + '/?page=rss&q=%s&c=1_4&f=0'


def resolve_torrent_url(view_url):
    """
    Resolves direct download url for torrent from view url .
    """
    return view_url.replace('view', 'download') + ".torrent"


def parse_search_item(item):
    return {
        "title": item.find('title').text,
        'url': resolve_torrent_url(item.find('guid').text)
    }


def parse_search_rss(request):
    """
    Parses RSS for raw category with search results.
    """
    response = requests.get(url_search_rss % quote(request), headers=requests_headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'lxml')
        return [parse_search_item(item) for item in soup.findAll('item')]
