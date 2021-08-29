from web_scrape_tab_com_au import *
import argparse


def main():
    parser = argparse.ArgumentParser(description='Running The Crawler For Football matches')
    parser.add_argument('--nameleague', type=str, default='spanish primera division')
    parser.add_argument('--verbose', type=bool, default=False)

    args = parser.parse_args()
    crawler = WebScrapping(args.nameleague, verbose=args.verbose)
    crawler.crawl()


if __name__ == '__main__':
    main()



