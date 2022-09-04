import argparse
import sys

import anime_collector.anime365 as anime365
import anime_collector.nyaasi as nyaasi


def init():
    parser = argparse.ArgumentParser(description='Anime collector')
    parser.add_argument('-n', '--nyaa', required=False, action='store_true', help="Test nyaa parser")
    parser.add_argument('-a', '--anime365', required=False, action='store_true', help="Test anime365 parser")
    parser.add_argument('-r', '--request', metavar='request', help="Request (page for anime365 or search for nyaa)")
    return parser.parse_args(sys.argv[1:])


def main():
    args = init()

    if args.anime365:
        page = int(args.request)
        subs = anime365.parse_recent_page(page)
        if subs:
            for sub in subs:
                print(sub)
    elif args.nyaa:
        raws = nyaasi.parse_search_rss(args.request)
        if raws:
            for raw in raws:
                print(raw)


if __name__ == "__main__":
    main()
