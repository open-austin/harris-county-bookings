#!/usr/bin/env python

import argparse
from datetime import date

from harris_county_bookings import *


# noinspection PyUnusedLocal
def lambda_handler(event, context):
    save_today_as_commit()


def save_today_as_commit():
    result = JIMSRecorder.save_to_github_commit(date.today())
    if result:
        urls = {r['content']['html_url'] for r in result}
        print ' '.join(urls)


def save_today_as_file():
    print ' '.join(JIMSRecorder.save_to_file(date.today()))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Save today\'s JIMS 1058 report')
    parser.add_argument('--commit', action='store_true',
                        help='If true, the file will be saved as a commit. Otherwise it is saved as a local file.')
    args = parser.parse_args()
    if args.commit:
        save_today_as_commit()
    else:
        save_today_as_file()
