from urllib.parse import quote

import requests
from bs4 import BeautifulSoup

from anime_collector import requests_headers

url_base = 'https://nyaa.si'
url_search_rss = url_base + '/?page=rss&q=%s&c=1_4&f=0'


def resolve_torrent_url(view_url):
    return view_url.replace('view', 'download') + ".torrent"


def parse_search_rss(request):
    response = requests.get(url_search_rss % quote(request), headers=requests_headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'lxml')
        return [(item.find('title').text, resolve_torrent_url(item.find('guid').text)) for item in soup.findAll('item')]