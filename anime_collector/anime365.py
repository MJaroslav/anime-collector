# TODO: Move to docs
"""
bs4-based parser for anime365 (smotret-anime.com)

Episode URL pattern:
/catalog/yofukashi-no-uta-25758/9-seriya-281418/russkie-subtitry-3981287
/catalog/[ORIGINAL_NAME]-[AMIME_ID]/[EPISODE_TYPE]-seriya-[EPISODE_ID]/[TRANSLATION_TYPE]-[TRANSLATION_ID]
Where:
    [ORIGINAL_NAME] - Original anime name, may be first non russian name in "/" split of line from /recent
    [ANIME_ID] - anime ID on anime365, not similar with MAL/Shikimori :c
    [EPISODE_TYPE] - "ova-" or "ona-" or "film-" with episode number, common episode is just number
    [EPISODE_ID] - ID of episode on anime365
    [TRANSLATION_TYPE] - "ozvuchka" or "russkie-subtitry" or "angliyskie-subtitry"
    [TRANSLATION_ID] - ID of translation on anime365, can be used for ass subtitles direct download link resolving
"""
import re
from datetime import datetime

import requests
from bs4 import BeautifulSoup
from bs4.element import NavigableString

from anime_collector import requests_headers

url_base = 'https://smotret-anime.com'  # Similar anime365
url_recent = url_base + '/translations/recent?page=%s'
url_ass_download = url_base + '/translations/ass/%s?download=1'  # .ass - subtitles extension :)


def resolve_ass_url(url_episode):
    """
    Just resolving .ass subtitles download link from episode link.
    Resource on result URL can be not exist if episode is hardsub or something!
    """
    return url_ass_download % (url_episode.split("-")[-1])


def find_ass_url(url_episode):
    """
    Finds .ass subtitles download link on episode page.
    Not recommended because it's required episode page loading and parsing.
    """
    page = requests.get(url_base + url_episode, headers=requests_headers)
    if page.status_code == 200:
        soup = BeautifulSoup(page.text, 'html.parser')
        downloads = soup.findAll('div', class_='m-translation-view-download')[0].findAll('a', class_='btn')
        downloads = filter(lambda item: item.has_attr('download'), downloads)
        downloads = [item['href'] for item in downloads]
        return downloads


def parse_episode_number(episode_url):
    """
    Parses type and episode number from its url.
    """
    raw_part = episode_url[1:].split("/")[2].split("-")  # Equals [EPISODE_TYPE]-seriya-[EPISODE_ID] and split with -
    raw_part.remove('seriya')
    if len(raw_part) > 2:
        return raw_part[0], int(raw_part[1])  # ([EPISODE_TYPE], [EPISODE_ID])
    else:
        return "common", int(raw_part[0])  # For common episodes


def parse_recent_line(recent_line):
    """
    Parse one /recent line to tuple with episode type, number, name (Original),
    release date and resolved (!) ass subtitles url.
    """
    a = recent_line.find('a')
    episode_url = a['href']
    episode = parse_episode_number(episode_url)
    name = a.text.split("/")[1:]
    if len(name) > 1:
        name = name[0].strip()
    else:
        cyrillic_pos = re.search('[\u0400-\u04FF]', name[0]).start()  # Any cyrillic char
        name = name[0][:cyrillic_pos].strip()
    date = "".join([t for t in recent_line.contents if type(t) == NavigableString]).strip()
    date = datetime.strptime(date, '%d.%m.%Y %H:%M')
    return episode[0], episode[1], name, date, resolve_ass_url(episode_url)


def parse_recent_page(page=1):
    """
    Parses /recent page and returns only subtitles.
    """
    response = requests.get(url_recent % page, headers=requests_headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        translations = soup.findAll('div', class_='m-translation-item')
        # Only subtitles allowed without subscription
        translations = filter(lambda item: "субтитры" in item.text, translations)
        translations = [parse_recent_line(item) for item in translations]
        return translations
