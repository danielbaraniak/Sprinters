#!/usr/bin/python3

import argparse

from ml.src import orchestrator


def main():
    parser = argparse.ArgumentParser(description='Launch processes.')
    parser.add_argument(
        '--train', action='store_true', help='Create machine learning model.'
    )
    parser.add_argument('--web', action='store_true', help='Start web server.')

    args = parser.parse_args()

    if args.train:
        orchestrator.main()
    elif args.web:
        from webservice.app import app
        app.run(debug=True)

    else:
        parser.print_help()


if __name__ == '__main__':
    main()
