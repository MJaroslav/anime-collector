# TODO: Match accuracy increasing required!!!
"""
Matcher for subtitle and torrent files.
"""
import anime_collector.anime365 as anime365
import anime_collector.nyaasi as nyaasi


def find_torrent(recent_item):
    """
    Tries finds torrent file by anime365 /recent item. Don't works properly.
    """
    request = recent_item['title']
    if recent_item['episode_type'] == 'common':
        request += " " + str(recent_item['episode_number'])
    result = nyaasi.parse_search_rss(request)
    if result:
        return result


def compile_recent():
    """
    Returns first anime365 /recent page with matched nyaa items. Don't works properly.
    """
    result = []
    for item in anime365.parse_recent_page():
        torrent = find_torrent(item)
        if torrent:
            result.append((item, torrent))
    return result
