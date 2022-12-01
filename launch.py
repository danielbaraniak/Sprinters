#!/usr/bin/python3
import argparse

def main():
    parser = argparse.ArgumentParser(description='Launch processes.')

    parser.add_argument('--train', action='store_true', help='Create machine learning model.')
    parser.add_argument('--web', action='store_true', help='Start web server.')
    parser.add_argument('--scrape', action='store_true', help='Invoke scraping worker.')
    
    args = parser.parse_args()

    if args.train:
        from ml.src import orchestrator
        orchestrator.main()
    elif args.web:
        from webservice.app import app
        app.run(debug=True)
    elif args.scrap:
        from scraper import scraper
        scraper.main()

    else:
        parser.print_help()


if __name__ == '__main__':
    main()
