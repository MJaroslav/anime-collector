import json
import os
import shutil
import time

import requests

from anime_collector import requests_headers


class Cacher(object):
    def __init__(self, directory='.'):
        self.__directory__ = directory + '/cache'
        self.__cache__ = self.__load_cache()

    def cache_torrent(self, torrent):
        if torrent not in self.__cache__['torrents']:
            filename = self.__directory__ + '/torrents/' + str(time.time_ns()) + ".torrent"
            response = requests.get(torrent, headers=requests_headers)
            if response.status_code == 200:
                with open(filename, 'wb') as file:
                    file.write(response.content)
                    self.__cache__['torrents'][torrent] = {
                        'filename': filename,
                        'date': time.time_ns(),
                    }
            else:
                self.__cache__['torrents'][torrent] = {
                    'filename': None,
                    'date': time.time_ns(),
                }
            self.__save_cache__()

    def cache_subs(self, subs):
        if subs not in self.__cache__['subs']:
            filename = self.__directory__ + '/subs/' + str(time.time_ns()) + ".ass"
            response = requests.get(subs, headers=requests_headers)
            if response.status_code == 200:
                with open(filename, 'wb') as file:
                    file.write(response.content)
                    self.__cache__['subs'][subs] = {
                        'filename': filename,
                        'date': time.time_ns(),
                    }
            else:
                self.__cache__['subs'][subs] = {
                    'filename': None,
                    'date': time.time_ns(),
                }
            self.__save_cache__()

    def clear_cache(self):
        shutil.rmtree(self.__directory__)
        self.__cache__ = {'torrents': {}, 'subs': {}}
        self.__save_cache__()

    def refresh_cache(self):
        temp = []
        now = time.time_ns()
        for item in self.__cache__['torrents']:
            if now - item['date'] >= 1_000_000_000 * 60 * 60 * 24 * 3:  # Cache lives 3 days
                temp.append(item)
                if item['filename']:
                    os.remove(item['filename'])
        self.__cache__['torrents'] = {k: v for k, v in self.__cache__['torrents'] if k not in temp}
        temp.clear()
        for item in self.__cache__['subs']:
            if now - item['date'] >= 1_000_000_000 * 60 * 60 * 24 * 3:  # Cache lives 3 days
                temp.append(item)
                if item['filename']:
                    os.remove(item['filename'])
        self.__cache__['subs'] = {k: v for k, v in self.__cache__['subs'] if k not in temp}
        self.__save_cache__()

    def get_torrent(self, torrent):
        pass

    def get_subs(self, subs):
        pass

    def __save_cache__(self):
        with open(self.__directory__ + '/cache.json', 'w') as file:
            json.dump(self.__cache__, file)

    def __load_cache(self):
        filename = self.__directory__ + '/cache.json'
        if os.path.exists(filename):
            with open(filename, 'r') as file:
                return json.load(file)
        else:
            return {'torrents': {}, 'subs': {}}
