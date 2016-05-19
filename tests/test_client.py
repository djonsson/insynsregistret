#! ../env/bin/python
# -*- coding: utf-8 -*-
import unittest
import sys

from insynsregistret.client import Session
from insynsregistret.cache import Cache
from nose.tools import assert_is_none, assert_is_not_none, assert_raises


def test_valid_date_should_not_return_none():
    date_xml = Session().search_transactions(from_date='2015-11-18', to_date='2015-12-18')
    for i, table in enumerate(date_xml):
        for data in table:
            print data.tag, data.text
        if i == 0:
            break
    assert_is_not_none(date_xml)


def test_invalid_date_in_the_1900s_should_return_none():
    assert_is_none(Session().search_transactions(from_date='1901-05-12', to_date='1901-05-15'))


def test_list_cache_files():
    Cache().purge_cache()
    Cache().list_cache_files()
    pass


@unittest.skipIf(sys.platform.startswith('win'), 'Only on nix')
def test_making_invalid_dir():
    with assert_raises(OSError):
        Cache().mkdir_p('/')


def test_get_insynpersoner():
    Session().search_insiders()


def test_company_search_by_name():
    Session().search_company(company_name='tobii')


def test_company_search_by_org_no():
    Session().search_company(org_number='556012-5790')


def test_get_several_search_results():
    Session().search_company(company_name='co')


def test_get_no_companies():
    Session().search_company(company_name='this-search-will-not-return-any-hits')

