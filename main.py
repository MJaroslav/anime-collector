from bs4.element import NavigableString
from bs4 import BeautifulSoup
from datetime import datetime
import requests
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0'
}

url_base = 'https://smotret-anime.com'
url_recent = url_base + '/translations/recent?page=%s'
url_ass_download = url_base + '/translations/ass/%s?download=1'


def parse_sub_file(url_episode):
    # page = requests.get(url_base + url_episode, headers=headers)
    # if page.status_code == 200:
    #     soup = BeautifulSoup(page.text, 'html.parser')
    #     downloads = soup.findAll('div', class_='m-translation-view-download')[0].findAll('a', class_='btn')
    #     print(downloads)
    #     downloads = filter(lambda item: item.has_attr('download'), downloads)
    #     downloads = [item['href'] for item in downloads]
    #     return downloads
    return url_ass_download % (url_episode.split("-")[-1])


def parse_translation(translation):
    a = translation.find('a')
    url = a['href']
    episode = a.text.split()[0]
    raw_name = a.text.split(" / ")[-1]
    info_pos = re.search('[\u0400-\u04FF]', raw_name).start()  # Any cyrillic
    name = raw_name[:info_pos].strip()
    date = "".join([t for t in translation.contents if type(t) == NavigableString]).strip()
    date = datetime.strptime(date, '%d.%m.%Y %H:%M')
    return episode, name, date, parse_sub_file(url)


def main():
    page = requests.get(url_recent % (2), headers=headers)
    if page.status_code == 200:
        soup = BeautifulSoup(page.text, 'html.parser')
        translations = soup.findAll('div', class_='m-translation-item')
        translations = filter(lambda item: "субтитры" in item.text, translations)
        translations = [parse_translation(item) for item in translations]
        for translation in translations:
            print(translation)


if __name__ == "__main__":
    main()
