#!/usr/bin/env python

from datetime import date
from harris_county_bookings import *


# lambda handler
def save_today_as_commit():
    print(JIMSFetcher.save_to_github_commit(date.today()))


if __name__ == '__main__':
    print(JIMSFetcher.save_to_file(date.today()))
