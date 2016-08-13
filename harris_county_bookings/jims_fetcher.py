import csv
import io
import os

import requests

from constants import *
from github_publisher import GitHubPublisher


class JIMSFetcher(object):
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
        raw_data = JIMSFetcher.read().split('\n')
        headers = raw_data[0].split(';')
        data = list(csv.DictReader(raw_data[1:], fieldnames=headers, delimiter=';'))
        return map(JIMSFetcher.strip_whitespace_from_values, data)

    @staticmethod
    def strip_whitespace_from_values(dictionary):
        return {k: v.strip() for k, v in dictionary.iteritems()}

    @staticmethod
    def save_to_file(date, directory=DATA_DIR):
        file_path = JIMSFetcher.build_file_path(date, directory)
        dirname = os.path.dirname(file_path)
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        data = JIMSFetcher.parse()
        with open(file_path, 'w+') as f:
            JIMSFetcher.write_csv(f, data)
        return file_path

    @staticmethod
    def write_csv(output, data):
        # specifying ignore will skip the entries not in HEADERS_TO_SAVE
        writer = csv.DictWriter(output, JIMSFetcher.HEADERS_TO_SAVE, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(data)
        return output

    @staticmethod
    def save_to_github_commit(date):
        # Do the import here so the rest of the methods work without defining settings
        import settings

        file_path = JIMSFetcher.build_file_path(date, DATA_DIR)
        data = JIMSFetcher.parse()
        output = JIMSFetcher.write_csv(io.BytesIO(), data)
        publisher = GitHubPublisher(settings.GITHUB_REPO_NAME, settings.GITHUB_API_TOKEN)
        # TODO verify the token has commit access to the repo
        return publisher.publish(file_path, settings.GITHUB_BRANCH, output.getvalue())

    @staticmethod
    def build_file_path(date, directory):
        fileName = "%s.csv" % date.strftime('%Y-%m-%d')
        return os.path.join(directory, str(date.year), fileName)
