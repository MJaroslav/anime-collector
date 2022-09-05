import argparse
import sys

import anime_collector.anime365 as anime365
import anime_collector.matcher as matcher
import anime_collector.nyaasi as nyaasi


def init():
    parser = argparse.ArgumentParser(description='Anime collector')
    parser.add_argument('-n', '--nyaa', action='store_true', help='Test nyaa parser')
    parser.add_argument('-a', '--anime365', action='store_true', help='Test anime365 parser')
    parser.add_argument('-p', '--page', default='0', metavar='page', help='Page for anime365 recent')
    parser.add_argument('-r', '--request', metavar='request', help='Search request')
    parser.add_argument('-c', '--compile', action='store_true', help='Show parsed and matched subs with raws')
    return parser.parse_args(sys.argv[1:])


def main():
    args = init()

    if args.compile:
        results = matcher.compile_recent()
        if results:
            [print(item) for item in results]
    if args.anime365:
        if args.page != '0':
            subs = anime365.parse_recent_page(int(args.page))
            if subs:
                [print(sub) for sub in subs]
        else:
            results = anime365.parse_search_page(args.request)
            if results:
                [print(item) for item in results]
    elif args.nyaa:
        raws = nyaasi.parse_search_rss(args.request)
        if raws:
            [print(raw) for raw in raws]


if __name__ == "__main__":
    main()
