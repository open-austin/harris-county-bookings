import base64

import requests

__all__ = ['GitHubPublisher']


class GitHubPublisher(object):
    def __init__(self, repo_info, token):
        self._name = repo_info['name']
        self._branch = repo_info['branch']
        self._contents_url = 'https://api.github.com/repos/{}/contents'.format(self._name)
        self._token = token

    def __build_url_for_path(self, path):
        return '{}/{}'.format(self._contents_url, path.strip('/'))

    def __build_auth_header(self):
        return {'authorization': 'token {}'.format(self._token)}

    def publish(self, path, content):
        payload = self.__build_update_payload(path, content)

        # If there is no payload to send, that means the file exists and it is identical;
        # don't push a commit in that scenario
        if not payload:
            print('Not updating {} since file exists and the content is identical'.format(path))
            return False

        return self.__push_commit(path, payload)

    def get_file_info(self, path):
        params = {'ref': self._branch}
        res = requests.get(self.__build_url_for_path(path), params=params, headers=self.__build_auth_header())
        print("Searched for {}, received following response: {}".format(path, res.text))
        res.raise_for_status()
        return res.json()

    def __build_update_payload(self, path, content):
        encoded_content = base64.b64encode(content)
        data = {
            'content': encoded_content,
            'branch': self._branch,
            'message': GitHubPublisher.__build_commit_message(path),
        }
        try:
            existing_file = self.get_file_info(path)
            if encoded_content == existing_file['content'].replace('\n', ''):
                # The file already exists so no need to build a payload
                return False
            data['sha'] = existing_file['sha']
        except requests.exceptions.HTTPError as e:
            # Swallow the 404s since that means the file does not already exist, and thus our payload does not need
            # the extra 'sha' parameter
            if e.response.status_code != 404:
                raise e
        return data

    def __push_commit(self, path, data):
        res = requests.put(self.__build_url_for_path(path), json=data, headers=self.__build_auth_header())
        print("Pushed commit for {}, received following response: {}".format(path, res.text))
        res.raise_for_status()
        return res.json()

    @staticmethod
    def __build_commit_message(path):
        return 'Automated commit {}'.format(path)
