import csv
import io
import os

import requests

from constants import *
from github_publisher import GitHubPublisher
from utils import *
from dialects import ACCDB, CSV, ALL_DIALECTS


class JIMSRecorder(object):
    # The headers left out of this list are the headers that contain personal data
    # https://github.com/open-austin/harris-county-bookings/issues/4
    HEADERS_TO_SAVE = ['SEX', 'RACE', 'ARREST DATE', 'BOOKING DATE', 'ADDRESS NUMBER', 'ADDRESS PREFIX',
                       'ADDRESS STREET', 'ADDRESS SUFFIX', 'ADDRESS ALI', 'ADDRESS CITY', 'ADDRESS STATE',
                       'ADDRESS ZIP', 'CHARGE CODE', 'CHARGE WORDING', 'CHARGE LEVEL', 'DISPOSITION']

    @staticmethod
    def read():
        return requests.get(JIMS_1058_URL).text

    @staticmethod
    def parse():
        raw_data = JIMSRecorder.read().split('\n')
        headers = raw_data[0].split(';')
        data = list(csv.DictReader(raw_data[1:], fieldnames=headers, dialect=ACCDB))
        return map(Utils.strip_whitespace_from_values, data)

    @staticmethod
    def save_to_file(date, directory=DATA_DIR, dialects=ALL_DIALECTS):
        data = JIMSRecorder.parse()
        file_paths = []
        for dialect in dialects:
            file_path = JIMSRecorder.build_file_path(date, directory, dialect)
            dirname = os.path.dirname(file_path)
            if not os.path.exists(dirname):
                os.makedirs(dirname)
            with open(file_path, 'w+') as f:
                JIMSRecorder.write_csv(f, data, dialect)
            file_paths.append(file_path)

        return file_paths

    @staticmethod
    def write_csv(output, data, dialect=CSV):
        # specifying ignore will skip the entries not in HEADERS_TO_SAVE
        writer = csv.DictWriter(output, JIMSRecorder.HEADERS_TO_SAVE, extrasaction='ignore', dialect=dialect)
        writer.writeheader()
        writer.writerows(data)
        return output

    @staticmethod
    def save_to_github_commit(date, dialects=ALL_DIALECTS):
        # Do the import here so the rest of the methods work without defining settings
        import settings

        data = JIMSRecorder.parse()
        results = []
        for dialect in dialects:
            file_path = JIMSRecorder.build_file_path(date, DATA_DIR, dialect)
            output = JIMSRecorder.write_csv(io.BytesIO(), data, dialect)
            publisher = GitHubPublisher(settings.GITHUB_REPO_NAME, settings.GITHUB_API_TOKEN)
            # TODO verify the token has commit access to the repo
            result = publisher.publish(file_path, settings.GITHUB_BRANCH, output.getvalue())
            results.append(result)

        return results

    @staticmethod
    def build_file_path(date, directory, dialect=CSV):
        extension = 'csv' if dialect == CSV else dialect
        filename = '%s.%s' % (date.strftime('%Y-%m-%d'), extension)
        return os.path.join(directory, str(date.year), filename)
