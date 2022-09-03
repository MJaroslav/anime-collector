import anime_collector.anime365 as anime365


def main():
    subs = anime365.parse_recent_page()
    if subs:
        for sub in subs:
            print(sub)


if __name__ == "__main__":
    main()
