#!/usr/bin/python
# -*- coding: utf-8 -*-
import unittest

from insynsregistret import clientcache
from insynsregistret.client import Client, Company
from nose.tools import assert_is_none, assert_is_not_none, assert_raises


class Tests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = Client()

    def test_invalid_date_in_the_1900s_should_return_none(self):
        assert_is_none(self.client.search_transactions(from_date='1901-05-12', to_date='1901-05-15'))

    def test_list_cache_files(self):
        clientcache.Cache().purge_cache()
        clientcache.Cache().list_cache_files()

    @unittest.skip("Does not raise an OSError in Travis")
    def test_making_invalid_dir(self):
        with assert_raises(OSError):
            clientcache.Cache().mkdir_p('/')

    def test_get_insiders_for_date_range(self):
        self.client.search_insiders('2015-11-18', '2015-12-18')

    def test_get_transactions_for_date_range(self):
        date_xml = Client().search_transactions(from_date='2015-11-18', to_date='2015-12-18')
        for i, table in enumerate(date_xml):
            for data in table:
                print(data.tag, data.text)
            if i == 0:
                break
        assert_is_not_none(date_xml)

    def test_get_company_search_by_name(self):
        self.client.search_company(company_name='tobii')

    def test_get_company_transactions_by_company_name(self):
        volvo = self.client.search_company(company_name='volvo')
        self.client.get_company_transactions(volvo, '2015-11-18', '2015-12-18')

    def test_get_company_transactions_by_org_number(self):
        lucara = self.client.search_company(org_number='556880-1277')
        self.client.get_company_transactions(lucara, '2015-11-18', '2015-12-18')

    def test_get_company_insider_current_holdings(self):
        clas_ohlson = self.client.search_company(company_name='clas ohlson')
        self.client.get_company_insider_current_holdings(clas_ohlson)

    def test_get_company_insider_historical_holdings(self):
        avanza = self.client.search_company(company_name='avanza')
        self.client.get_company_insider_historical_holdings(avanza)

    def test_get_company_insiders_people(self):
        ssab = self.client.search_company(company_name='ssab')
        self.client.get_company_insiders_people(ssab)

    def test_get_company_insider_position_changes(self):
        ssab = self.client.search_company(company_name='ssab')
        self.client.get_company_insider_position_changes(ssab)

    def test_search_results_several(self):
        result = self.client.search_company(company_name='co')

    def test_search_results_no_hits(self):
        self.client.search_company(company_name='this-search-will-not-return-any-hits')

    def test_company_get_current_insider(self):
        xml = Company(company_name='volvo').get_current_holdings()
        for table in xml.findall('Table'):
            print (table.find('Person').text)

if __name__ == '__main__':
    unittest.main()
