import requests
import base64

__all__ = ['GitHubPublisher']


class GitHubPublisher(object):
    def __init__(self, repo_name, token):
        self._contents_url = 'https://api.github.com/repos/{}/contents'.format(repo_name)
        self._token = token

    def __build_url_for_path(self, path):
        return '{}/{}'.format(self._contents_url, path.strip('/'))

    def __build_auth_header(self):
        return {'authorization': 'token {}'.format(self._token)}

    def publish(self, path, branch, content):
        payload = self.__build_update_payload(path, branch, content)

        # If there is no payload to send, that means the file exists and it is identical.
        # So don't push a commit in that scenario.
        if not payload:
            print('Not updating {} since file exists and the content is identical'.format(path))
            return False

        return self.__push_commit(path, payload)

    def get_file_info(self, path, branch):
        params = {'ref': branch}
        res = requests.get(self.__build_url_for_path(path), params=params, headers=self.__build_auth_header())
        print("Searched for {}, received following response: {}".format(path, res.text))
        res.raise_for_status()
        return res.json()

    def __build_update_payload(self, path, branch, content):
        encoded_content = base64.b64encode(content)
        data = {
            'content': encoded_content,
            'branch': branch,
            'message': GitHubPublisher.__build_commit_message(path),
        }
        try:
            existing_file = self.get_file_info(path, branch)
            if encoded_content == existing_file['content'].replace('\n', ''):
                # the file already exists as is. no need to build a payload for an update
                return False
            data['sha'] = existing_file['sha']
        except requests.exceptions.HTTPError as e:
            # swallow the 404s since that means the file does not already exist, and thus our payload does not need
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
