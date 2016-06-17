#! ../env/bin/python
# -*- coding: utf-8 -*-
import unittest
import sys

from insynsregistret.client import Session
from insynsregistret.cache import Cache
from nose.tools import assert_is_none, assert_is_not_none, assert_raises


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


def test_get_insiders_for_date_range():
    Session().search_insiders('2015-11-18', '2015-12-18')


def test_get_transactions_for_date_range():
    date_xml = Session().search_transactions(from_date='2015-11-18', to_date='2015-12-18')
    for i, table in enumerate(date_xml):
        for data in table:
            print data.tag, data.text
        if i == 0:
            break
    assert_is_not_none(date_xml)


def test_get_company_search_by_name():
    Session().search_company(company_name='tobii')


def test_get_company_transactions_by_company_name():
    insynsok = Session()
    volvo = insynsok.search_company(company_name='volvo')
    insynsok.get_company_transactions(volvo, '2015-11-18', '2015-12-18')


def test_get_company_transactions_by_org_number():
    insynsok = Session()
    lucara = insynsok.search_company(org_number='556880-1277')
    insynsok.get_company_transactions(lucara, '2015-11-18', '2015-12-18')


def test_get_company_insider_current_holdings():
    insynsok = Session()
    clas_ohlson = insynsok.search_company(company_name='clas ohlson')
    insynsok.get_company_insider_current_holdings(clas_ohlson)


def test_get_company_insider_historical_holdings():
    insynsok = Session()
    avanza = insynsok.search_company(company_name='avanza')
    insynsok.get_company_insider_historical_holdings(avanza)


def test_get_company_insiders_people():
    insynsok = Session()
    ssab = insynsok.search_company(company_name='ssab')
    insynsok.get_company_insiders_people(ssab)


def test_get_company_insider_position_changes():
    insynsok = Session()
    ssab = insynsok.search_company(company_name='ssab')
    insynsok.get_company_insider_position_changes(ssab)


def test_search_results_several():
    Session().search_company(company_name='co')


def test_search_results_no_hits():
    Session().search_company(company_name='this-search-will-not-return-any-hits')