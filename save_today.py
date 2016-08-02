#!/usr/bin/env python

from datetime import date
from harris_county_bookings import *

if __name__ == '__main__':
    print(JIMSFetcher.save(date.today()))
