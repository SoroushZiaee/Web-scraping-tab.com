from web_scrape_tab_com_au import *
import argparse


def main():
    parser = argparse.ArgumentParser(description='Running The Crawler For Football matches')
    parser.add_argument('--nameleague', type=str, default='spanish primera division')
    parser.add_argument('--verbose', type=bool, default=False)
    parser.add_argument('--history', type=bool, default=False)
    parser.add_argument('--season', type=str, default='2020-2021')
    

    args = parser.parse_args()

    if args.history:
        crawler = WebScrappingHistory(args.nameleague, season=args.season, verbose=args.verbose)
        crawler.crawl()
    
    else:
        crawler = WebScrapping(args.nameleague, verbose=args.verbose)
        crawler.crawl()


if __name__ == '__main__':
    main()



