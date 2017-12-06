#!/usr/bin/env python

import argparse
from datetime import date as dt

from harris_county_bookings import *


# noinspection PyUnusedLocal
def lambda_handler(event, context):
    today = dt.today()
    data = JIMSRecorder.fetch_and_clean_data(s3=True, date=today)
    save_to_s3(data, today, ALL_MODES)
    save_to_github(data, today, ALL_MODES)
    save_to_dataworld(data, today, ALL_MODES)


def local_handler(args):
    today = dt.today()
    data = JIMSRecorder.fetch_and_clean_data(s3=args.s3, date=today)
    modes = [args.data_mode] if args.data_mode != 'both' else ALL_MODES

    if args.s3:
        save_to_s3(data, today, modes)

    if args.commit:
        save_to_github(data, today, modes)

    if args.dataset:
        save_to_dataworld(data, today, modes)

    if not args.s3 and not args.commit and not args.dataset:
        save_to_file(data, today, modes)


def save_to_s3(data, date, modes):
    result = JIMSRecorder.save_to_s3(data, date, modes)
    # if result:
    #     urls = (r['content']['html_url'] for r in result)
    #     print(' '.join(urls))


def save_to_github(data, date, modes):
    result = JIMSRecorder.save_to_github(data, date, modes)
    if result:
        urls = (r['content']['html_url'] for r in result)
        print(' '.join(urls))


def save_to_dataworld(data, date, modes):
    result = JIMSRecorder.save_to_dataworld(data, date, modes)
    if result:
        print(result)
        urls = (r for r in result)
        print(' '.join(urls))


def save_to_file(data, date, modes):
    file_paths = JIMSRecorder.save_to_file(data, date, modes)
    print(' '.join(file_paths))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Save today's JIMS 1058 report")
    mode_help = "Define which mode to use to scrub the data. '{}' will save the data as is. " \
                "'{}' will scrub out personal data. 'both' will save files for " \
                "each mode in separate directories.".format(RAW, SCRUB)
    parser.add_argument('--mode', default=SCRUB, choices=[RAW, SCRUB, 'both'], help=mode_help)
    parser.add_argument('--commit', action='store_true', help='Save the file to GitHub.')
    parser.add_argument('--dataset', action='store_true', help='Save the file to a data.world dataset.')

    local_handler(parser.parse_args())
