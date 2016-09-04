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
    SCRUBBED_HEADERS = ['SEX', 'RACE', 'ARREST DATE', 'BOOKING DATE', 'ADDRESS NUMBER', 'ADDRESS PREFIX',
                        'ADDRESS STREET', 'ADDRESS SUFFIX', 'ADDRESS ALI', 'ADDRESS CITY', 'ADDRESS STATE',
                        'ADDRESS ZIP', 'CHARGE CODE', 'CHARGE WORDING', 'CHARGE LEVEL', 'DISPOSITION']
    ALL_HEADERS = SCRUBBED_HEADERS + ['BOOKING NUMBER', 'NAME', 'DATE OF BIRTH', 'CASE NUMBER']

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
    def save_to_file(date, modes=ALL_MODES, dialects=ALL_DIALECTS):
        data = JIMSRecorder.parse()
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
        # specifying ignore will skip the entries not in HEADERS_TO_SAVE
        writer = JIMSRecorder._build_dict_writer(output, mode, dialect)
        writer.writeheader()
        writer.writerows(data)
        return output

    @staticmethod
    def _build_dict_writer(output, mode, dialect):
        headers = JIMSRecorder.ALL_HEADERS if mode == RAW else JIMSRecorder.SCRUBBED_HEADERS
        return csv.DictWriter(output, headers, extrasaction='ignore', dialect=dialect)

    @staticmethod
    def save_to_github_commit(date, modes=ALL_MODES, dialects=ALL_DIALECTS):
        # Do the import here so the rest of the methods work without defining settings
        import settings

        data = JIMSRecorder.parse()
        results = []
        for mode in modes:
            directory = DATA_DIRS[mode]
            repo_info = settings.GITHUB_REPOS[mode]
            for dialect in dialects:
                file_path = JIMSRecorder.build_file_path(date, directory, dialect)
                output = JIMSRecorder.write_csv(io.BytesIO(), data, mode, dialect)
                publisher = GitHubPublisher(repo_info['name'], settings.GITHUB_API_TOKEN)
                # TODO verify the token has commit access to the repo
                result = publisher.publish(file_path, repo_info['branch'], output.getvalue())
                results.append(result)

        return results

    @staticmethod
    def build_file_path(date, directory, dialect=CSV):
        extension = 'csv' if dialect == CSV else dialect
        filename = '%s.%s' % (date.strftime('%Y-%m-%d'), extension)
        return os.path.join(directory, str(date.year), filename)
