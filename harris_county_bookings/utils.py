import hashlib

__all__ = ['Utils']


class Utils(object):
    @staticmethod
    def filter_dict_keys(dictionary, keys):
        return {k: v for k, v in filter(lambda t: t[0] in keys, dictionary.items())}

    @staticmethod
    def generate_hash(string):
        hash_object = hashlib.sha1(string.encode())
        return hash_object.hexdigest()

    @staticmethod
    def strip_whitespace_from_values(dictionary):
        return {k: v.strip() for k, v in dictionary.items()}
