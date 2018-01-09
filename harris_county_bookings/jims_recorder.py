import csv
import io
import json
import os

import requests

from .constants import *
from .dialects import ACCDB, CSV, ALL_DIALECTS
from .dataworld_publisher import DataWorldPublisher
from .github_publisher import GitHubPublisher
from .s3_publisher import S3Publisher
from .utils import *

RAW = 'raw'
SCRUB = 'scrub'
ALL_MODES = [RAW, SCRUB]
DATA_DIRS = {RAW: 'raw-data', SCRUB: 'data'}


class JIMSRecorder(object):
    # The headers left out of this list are the headers that contain personal data
    # https://github.com/open-austin/harris-county-bookings/issues/4
    SCRUBBED_HEADERS = ['ARRESTEE ID', 'SEX', 'RACE', 'ARREST DATE', 'BOOKING DATE', 'ADDRESS CITY',
                        'ADDRESS STATE', 'ADDRESS ZIP', 'CHARGE CODE', 'CHARGE WORDING', 'CHARGE LEVEL',
                        'DISPOSITION']
    ALL_HEADERS = SCRUBBED_HEADERS + ['BOOKING NUMBER', 'NAME', 'DATE OF BIRTH', 'CASE NUMBER']

    @staticmethod
    def clean(data):
        """Processes to prepare the raw data"""
        data = map(Utils.strip_whitespace_from_values, data)

        # Creates a unique identifier for each person for anonymizing purposes
        def generate_identifier(row):
            row['ARRESTEE ID'] = Utils.generate_hash(row['NAME'] + row['DATE OF BIRTH'])
            return row
        data = map(generate_identifier, data)

        # Standardizes the three date columns to the 'mm/dd/yyyy' format
        def standardize_dates(row):
            row['ARREST DATE'] = Utils.standardize_date(row['ARREST DATE'], '%m%d%Y')
            row['BOOKING DATE'] = Utils.standardize_date(row['BOOKING DATE'], '%m%d%Y')
            row['DATE OF BIRTH'] = Utils.standardize_date(row['DATE OF BIRTH'], '%m/%d/%y')
            return row
        data = map(standardize_dates, data)

        # TODO reduce granularity on the raw addresses & add it to scrubbed data

        return list(data)

    @staticmethod
    def fetch_and_clean_data(s3=False, date=None):
        """
        :param date: Today's date
        :param s3: If true, the original file will be saved to an s3 bucket
        """
        from . import settings

        raw_data = requests.get(JIMS_1058_URL)
        if s3:
            filename = '{}.txt'.format(date.strftime('%Y-%m-%d'))
            bucket_info = settings.S3_BUCKETS[RAW]
            publisher = S3Publisher(bucket_info)
            # TODO verify access to the bucket
            publisher.publish('original-files/' + filename, raw_data.content)

        raw_data = raw_data.text.split('\n')
        headers = raw_data[0].split(';')
        data = list(csv.DictReader(raw_data[1:], fieldnames=headers, dialect=ACCDB))
        return JIMSRecorder.clean(data)

    @staticmethod
    def build_file_path(date, directory, dialect=CSV):
        extension = 'csv' if dialect == CSV else dialect
        filename = '{}.{}'.format(date.strftime('%Y-%m-%d'), extension)
        return os.path.join(directory, str(date.year), filename)

    @staticmethod
    def save_to_file(data, date, modes=ALL_MODES, dialects=ALL_DIALECTS):
        file_paths = []
        for mode in modes:
            for dialect in dialects:
                file_path = JIMSRecorder.build_file_path(date, DATA_DIRS[mode], dialect)
                dirname = os.path.dirname(file_path)
                if not os.path.exists(dirname):
                    os.makedirs(dirname)
                with open(file_path, 'w+') as f:
                    JIMSRecorder.write_csv(f, data, mode, dialect)
                file_paths.append(file_path)

        return file_paths

    @staticmethod
    def write_csv(output, data, mode=SCRUB, dialect=CSV):
        writer = JIMSRecorder.build_dict_writer(output, mode, dialect)
        writer.writeheader()
        writer.writerows(data)
        return output

    @staticmethod
    def get_headers(mode):
        return JIMSRecorder.ALL_HEADERS if mode == RAW else JIMSRecorder.SCRUBBED_HEADERS

    @staticmethod
    def build_dict_writer(output, mode, dialect):
        headers = JIMSRecorder.get_headers(mode)
        return csv.DictWriter(output, headers, extrasaction='ignore', dialect=dialect)

    @staticmethod
    def save_to_s3(data, date, modes=ALL_MODES, dialects=ALL_DIALECTS):
        # Do the import here so the rest of the methods work without defining settings
        from . import settings

        results = []
        for mode in modes:
            directory = DATA_DIRS[mode]
            bucket_info = settings.S3_BUCKETS[mode]
            for dialect in dialects:
                file_path = JIMSRecorder.build_file_path(date, directory, dialect)
                output = JIMSRecorder.write_csv(io.StringIO(), data, mode, dialect)
                publisher = S3Publisher(bucket_info)
                result = publisher.publish(file_path, output.getvalue())
                if result:
                    results.append(result)

        return results

    @staticmethod
    def save_to_github(data, date, modes=ALL_MODES, dialects=ALL_DIALECTS):
        # Do the import here so the rest of the methods work without defining settings
        from . import settings

        results = []
        for mode in modes:
            directory = DATA_DIRS[mode]
            repo_info = settings.GITHUB_REPOS[mode]
            for dialect in dialects:
                file_path = JIMSRecorder.build_file_path(date, directory, dialect)
                output = JIMSRecorder.write_csv(io.StringIO(), data, mode, dialect)
                publisher = GitHubPublisher(repo_info, settings.GITHUB_API_TOKEN)
                # TODO verify the token has commit access to the repo
                result = publisher.publish(file_path, output.getvalue())
                if result:
                    results.append(result)

        return results

    @staticmethod
    def prepare_jsonl(mode, data):
        headers = JIMSRecorder.get_headers(mode)
        data = (Utils.filter_keys_from_dict(e, headers) for e in data)
        return '\n'.join((json.dumps(e) for e in data))

    @staticmethod
    def save_to_dataworld(data, date, modes=ALL_MODES):
        # Do the import here so the rest of the methods work without defining settings
        from . import settings

        results = []
        for mode in modes:
            stream_name = date.year
            dataset_info = settings.DATAWORLD_DATASETS[mode]
            output = JIMSRecorder.prepare_jsonl(mode, data)
            publisher = DataWorldPublisher(dataset_info, settings.DATAWORLD_API_TOKEN)
            # TODO verify the token has access to the dataset
            result = publisher.publish(stream_name, output)
            if result:
                publisher.sync()
                results.append(result)

        return results
