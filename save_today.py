#!/usr/bin/env python

import argparse
from datetime import date

from harris_county_bookings import *
from harris_county_bookings.constants import *


# noinspection PyUnusedLocal
def lambda_handler(event, context):
    save_today_as_commit(ALL_MODES)


def save_today_as_commit(modes):
    result = JIMSRecorder.save_to_github_commit(date.today(), modes)
    if result:
        urls = {r['content']['html_url'] for r in result}
        print ' '.join(urls)


def save_today_as_file(modes):
    print ' '.join(JIMSRecorder.save_to_file(date.today(), modes))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Save today\'s JIMS 1058 report')
    parser.add_argument('--commit', action='store_true',
                        help='If true, the file will be saved as a commit. Otherwise it is saved as a local file.')
    data_mode_help = 'Define which mode to scrub the data. \'%s\' will save the data as is. ' \
                     '\'%s\' will scrub out personal data. \'both\' will save files for ' \
                     'each mode in separate directories.' % (RAW, SCRUB)
    parser.add_argument('--data_mode', help=data_mode_help, default=SCRUB, choices=[RAW, SCRUB, 'both'])
    args = parser.parse_args()
    data_modes = [args.data_mode] if args.data_mode != 'both' else ALL_MODES

    if args.commit:
        save_today_as_commit(data_modes)
    else:
        save_today_as_file(data_modes)
