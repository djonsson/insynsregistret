#! ../env/bin/python
# -*- coding: utf-8 -*-

import errno
import os
import shutil


class Cache(object):
    """
    This class controls the local cache. If will look in the cache directory to see if the xml file we are requesting
    already is persisted on disk.

    """
    __directory__ = None

    def __init__(self, cache_directory=None):
        if cache_directory is None:
            cache_directory = {'cache_directory': '~/.cache-insyn/'}

        self.__directory__ = os.path.expanduser(cache_directory['cache_directory'])
        self.mkdir_p(self.__directory__)

    def get_cache_directory(self):
        return self.__directory__

    @staticmethod
    def file_exist(path):
        return os.path.isfile(path)

    def list_cache_files(self):
        return os.listdir(self.__directory__)

    def purge_cache(self):
        return shutil.rmtree(self.__directory__)

    @staticmethod
    def is_empty(path):
        # On dates without inside trades we receive a xml file containing no interesting data.
        # This file is always 53 bytes.
        if os.path.getsize(path) == 53:
            return True
        return False

    @staticmethod
    def mkdir_p(path):
        try:
            os.makedirs(path)
        except OSError as exc:  # Python >2.5
            if exc.errno == errno.EEXIST and os.path.isdir(path):
                pass
            else:
                raise
