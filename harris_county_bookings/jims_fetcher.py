import os

import requests

from constants import *
from github_publisher import GitHubPublisher


class JIMSFetcher(object):
    @staticmethod
    def read():
        return requests.get(JIMS_1058_URL).text

    @staticmethod
    def save_to_file(date, directory=DATA_DIR):
        file_path = JIMSFetcher.build_file_path(date, directory)
        dirname = os.path.dirname(file_path)
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        with open(file_path, 'w+') as f:
            f.write(JIMSFetcher.read())
        return file_path

    @staticmethod
    def save_to_github_commit(date):
        file_path = JIMSFetcher.build_file_path(date, DATA_DIR)
        # Do the import here so the rest of the methods work without defining settings
        import settings
        publisher = GitHubPublisher(settings.GITHUB_REPO_NAME, settings.GITHUB_API_TOKEN)
        # TODO verify the token has commit access to the repo
        return publisher.publish(file_path, settings.GITHUB_BRANCH, JIMSFetcher.read())

    @staticmethod
    def build_file_path(date, directory):
        fileName = "%s.accdb" % date.strftime('%Y-%m-%d')
        return os.path.join(directory, str(date.year), fileName)
