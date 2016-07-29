import requests
import os
from constants import *


class JIMSFetcher(object):
    @staticmethod
    def read():
        return requests.get(JIMS_1058_URL).text

    @staticmethod
    def save(date, directory=DATA_DIR):
        file_path = JIMSFetcher.build_file_path(date, directory)
        with open(file_path, 'w+') as f:
            f.write(JIMSFetcher.read())
        return file_path

    @staticmethod
    def build_file_path(date, directory):
        fileName = "%s.accdb" % date.strftime('%Y-%m-%d')
        return os.path.join(directory, str(date.year), fileName)
