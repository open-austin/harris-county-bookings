__all__ = ['Utils']


class Utils(object):
    @staticmethod
    def strip_whitespace_from_values(dictionary):
        return {k: v.strip() for k, v in dictionary.iteritems()}
