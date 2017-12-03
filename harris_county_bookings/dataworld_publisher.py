import json
import requests

__all__ = ['DataWorldPublisher']


class DataWorldPublisher(object):
    def __init__(self, dataset, token):
        self._dataset_owner = dataset['owner']
        self._dataset_name = dataset['name']
        self._api_url = 'https://api.data.world/v0/{{}}/{0}/{1}/{{}}'.format(self._dataset_owner, self._dataset_name)
        self._token = token

    def __build_auth_header(self):
        return {'authorization': 'bearer ' + self._token}

    def sync(self):
        res = requests.get(self._api_url.format('datasets', 'sync'), headers=self.__build_auth_header())
        print("Updated {}, received following response: {}".format(self._dataset_name, res.text))

    def publish(self, stream_name, data):
        if self.data_exists(stream_name, data):
            print('Not updating {} since the data already exists'.format(self._dataset_name))
            return False

        headers = self.__build_auth_header()
        headers['content-type'] = 'application/json-l'
        res = requests.post(self._api_url.format('streams', stream_name), data=data, headers=headers)
        print("Pushed data to {}.jsonl, received following response: {}".format(stream_name, res.text))
        res.raise_for_status()
        return res.url

    def data_exists(self, stream_name, data):
        """
        Runs a SQL query to verify that today's data hasn't already been pushed.
        Currently checks a single entry
        """
        verification_sample = json.loads(data.split('\n')[0])
        arrestee_id = verification_sample['ARRESTEE ID']
        arrest_date = verification_sample['ARREST DATE']
        booking_date = verification_sample['BOOKING DATE']
        charge_code = verification_sample['CHARGE CODE']
        query_body = "SELECT * FROM {} WHERE arrestee_id = '{}' and arrest_date = '{}' " \
                     "and booking_date = '{}' and charge_code = '{}'"
        query = {'query': query_body.format(stream_name, arrestee_id, arrest_date, booking_date, charge_code)}

        res = requests.post(self._api_url.format('sql', ''), data=query, headers=self.__build_auth_header())
        print("Queried {} in {}, received following response: {}".format(stream_name, self._dataset_name, res.text))
        res.raise_for_status()

        if res.text:
            return True
        else:
            return False
