#!/usr/bin/env python

import argparse
from datetime import date

from harris_county_bookings import *


# noinspection PyUnusedLocal
def lambda_handler(event, context):
    save_to_github(ALL_MODES)
    save_to_dataworld(ALL_MODES)


def save_to_github(modes):
    result = JIMSRecorder.save_to_github(date.today(), modes)
    if result:
        urls = (r['content']['html_url'] for r in result)
        print(' '.join(urls))


def save_to_dataworld(modes):
    result = JIMSRecorder.save_to_dataworld(date.today(), modes)
    if result:
        print(result)
        urls = (r for r in result)
        print(' '.join(urls))


def save_to_file(modes):
    file_paths = JIMSRecorder.save_to_file(date.today(), modes)
    print(' '.join(file_paths))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Save today's JIMS 1058 report")
    data_mode_help = "Define which mode to use to scrub the data. '{}' will save the data as is. " \
                     "'{}' will scrub out personal data. 'both' will save files for " \
                     "each mode in separate directories.".format(RAW, SCRUB)
    parser.add_argument('--data_mode', default=SCRUB, choices=[RAW, SCRUB, 'both'], help=data_mode_help)
    parser.add_argument('--commit', action='store_true', help='Save the file to GitHub.')
    parser.add_argument('--dataset', action='store_true', help='Save the file to a data.world dataset.')

    args = parser.parse_args()
    data_modes = [args.data_mode] if args.data_mode != 'both' else ALL_MODES

    if args.commit:
        save_to_github(data_modes)

    if args.dataset:
        save_to_dataworld(data_modes)

    if not args.commit and not args.dataset:
        save_to_file(data_modes)
