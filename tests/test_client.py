#! ../env/bin/python
# -*- coding: utf-8 -*-
from insynsregistret.client import Session
from insynsregistret.cache import Cache
from nose.tools import assert_is_none, assert_is_not_none, assert_raises


def test_valid_date_should_not_return_none():
    assert_is_not_none(Session().get(from_date='2001-12-18', to_date='2001-12-18'))


def test_invalid_date_in_the_1900s_should_return_none():
    assert_is_none(Session().get(from_date='1901-05-12', to_date='1901-05-15'))


def test_list_cache_files():
    print Cache().purge_cache()
    print Cache().list_cache_files()


def test_making_invalid_dir():
    with assert_raises(OSError):
        Cache().mkdir_p('/')
