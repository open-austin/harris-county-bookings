import hashlib
from datetime import datetime

__all__ = ['Utils']


class Utils(object):
    @staticmethod
    def filter_keys_from_dict(dictionary, keys):
        """Strips a set of keys from a dictionary"""
        return {k: v for k, v in filter(lambda t: t[0] in keys, dictionary.items())}

    @staticmethod
    def generate_hash(string):
        """Builds a SHA-1 hash from the string provided"""
        hash_object = hashlib.sha1(string.encode())
        return hash_object.hexdigest()

    @staticmethod
    def standardize_date(date, incoming_format):
        """
        Returns dates in the format '12/24/2017'
        :param date: The date object
        :param incoming_format: Format of the date object, can be something like '%m/%d/%y'
        """
        dt = datetime.strptime(date, incoming_format)

        # Fixes a bug in which dates before 1970 might not be inferred correctly
        if dt.year > datetime.now().year:
            dt = dt.replace(year=dt.year - 100)
        return dt.strftime('%m/%d/%Y')

    @staticmethod
    def strip_whitespace_from_values(dictionary):
        return {k: v.strip() for k, v in dictionary.items()}
