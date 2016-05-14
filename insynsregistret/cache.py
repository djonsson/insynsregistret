import errno
import os


class Cache(object):
    """
    This class controls the local cache. If will look in the cache directory to see if the xml file we are requesting
    already is persisted on disk.

    """
    __directory__ = None

    def __init__(self, cache_directory):
        self.__directory__ = os.path.expanduser(cache_directory['cache_directory'])
        self.mkdir_p(self.__directory__)

    def get_cache_directory(self):
        return self.__directory__

    def get_expected_filename_of_xml(self, fromdate, todate):
        return self.get_cache_directory() + self.transaction_filename_xml(fromdate, todate)

    @staticmethod
    def transaction_filename_xml(fromdate, todate):
        return '_Transaktioner_%s_%s__(sv-SE).xml' % (fromdate, todate)

    @staticmethod
    def file_exist(path):
        return os.path.isfile(path)

    @staticmethod
    def mkdir_p(path):
        try:
            os.makedirs(path)
        except OSError as exc:  # Python >2.5
            if exc.errno == errno.EEXIST and os.path.isdir(path):
                pass
            else:
                raise
