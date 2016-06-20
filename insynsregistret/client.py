#! ../env/bin/python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from . import clientcache
import zipfile

from io import BytesIO

import requests
import xml.etree.ElementTree as ET


class Client(object):
    __default_settings = {
        'cache_directory': '~/.cache-insyn/'
    }

    __base_url = 'http://insynsok.fi.se'
    __params = {'culture': 'en-GB'}

    def __init__(self):
        self.__session = requests.Session()
        self.__cache = clientcache.Cache(self.__default_settings)
        self.__cache_dir = self.__cache.get_cache_directory()

    def search_transactions(self, from_date, to_date):
        url = self.__base_url + '/SearchPage.aspx'
        filename = self.__cache_dir + (
        '_Transaktioner_%s_%s__(%s).xml' % (from_date, to_date, self.__params.get('culture')))
        e, v = self.__get_request_to_setup_asp_fields(url)

        if not self.__cache.file_exist(filename):
            response = self.__session.post(url, params=self.__params,
                                           data=self.__request_payload(e, v, drop_down='Transaktioner',
                                                                       from_date=from_date, to_date=to_date))
            z = zipfile.ZipFile(BytesIO(response.content))
            z.extractall(path=self.__cache_dir)
        if self.__cache.is_empty(filename):
            return None
        return ET.parse(filename).getroot()

    def search_insiders(self, from_date, to_date):
        url = self.__base_url + '/SearchPage.aspx'
        filename = self.__cache_dir + '_Insyn__(%s).xml' % self.__params.get('culture')
        e, v = self.__get_request_to_setup_asp_fields(url)
        response = self.__session.post(url, params=self.__params,
                                       data=self.__request_payload(e, v, drop_down='Insyn', from_date=from_date,
                                                                   to_date=to_date))

        z = zipfile.ZipFile(BytesIO(response.content))
        z.extractall(path=self.__cache_dir)
        return ET.parse(filename).getroot()

    def search_company(self, company_name=None, org_number=None):
        search_term = ''.join(filter(None, (company_name, org_number)))

        url = self.__base_url + '/Startpage.aspx?searchtype=0'
        response = self.__session.post(url, params=self.__params,
                                       data=self.__search_payload(url, company_name=company_name,
                                                                  org_number=org_number))
        e, v = self.__get_asp_fields_from_response(response)
        search_result = {'search term': search_term, 'asp_fields': {'e': e, 'v': v}, 'response': response}

        # If 'bolag' is not present in url, we either got 0 results for the search or a list of results
        if 'bolag' not in response.url:
            soup = BeautifulSoup(response.content, 'lxml')
            table = soup.find('table', {'id': 'ctl00_main_grdBolag'})

            # If the table is not present we got 0 hits
            if not table:
                return search_result.update({'search result': None})

            # Parsing the table containing company information
            rows = table.find_all('tr')
            for row in rows:
                cols = row.find_all('td')
                cols = [ele.text.strip() for ele in cols]
                search_result.update({'search result': cols})
        return search_result

    def get_company_transactions(self, company, from_date, to_date):
        e, v, response = self.__get_company_asp_fields(company)
        response = self.__session.post(response.url, data=self.__request_payload(e, v, drop_down='Transaktioner',
                                                                                 from_date=from_date,
                                                                                 to_date=to_date))
        return self.__xml_response_from_file(response)

    def get_company_insider_current_holdings(self, company):
        e, v, response = self.__get_company_asp_fields(company)
        response = self.__session.post(response.url, data=self.__request_payload(e, v, drop_down='Innehav'))
        return self.__xml_response_from_file(response)

    def get_company_insider_historical_holdings(self, company):
        e, v, response = self.__get_company_asp_fields(company)
        response = self.__session.post(response.url, data=self.__request_payload(e, v, drop_down='HistorisktInnehav'))
        return self.__xml_response_from_file(response)

    def get_company_insiders_people(self, company):
        e, v, response = self.__get_company_asp_fields(company)
        response = self.__session.post(response.url, data=self.__request_payload(e, v, drop_down='Insyn'))
        return self.__xml_response_from_file(response)

    def get_company_insider_position_changes(self, company):
        e, v, response = self.__get_company_asp_fields(company)
        response = self.__session.post(response.url,
                                       data=self.__request_payload(e, v, drop_down='Befattningsforandringar'))
        return self.__xml_response_from_file(response)

    def __xml_response_from_file(self, response):
        z = zipfile.ZipFile(BytesIO(response.content))
        z.extractall(path=self.__cache_dir)
        for name in z.namelist():
            if '.xml' in name:
                return ET.parse(self.__cache_dir + name)

    @staticmethod
    def __get_company_asp_fields(company):
        response = company['response']
        e = company['asp_fields']['e']
        v = company['asp_fields']['v']
        return e, v, response

    def __get_request_to_setup_asp_fields(self, url):
        response = self.__session.get(url)
        return self.__get_asp_fields_from_response(response)

    @staticmethod
    def __get_asp_fields_from_response(response):
        soup = BeautifulSoup(response.content, 'lxml')
        event_validation = soup.find("input", {"id": "__EVENTVALIDATION"}).get('value')
        view_state = soup.find("input", {"id": "__VIEWSTATE"}).get('value')
        return event_validation, view_state

    @staticmethod
    def __request_payload(e, v, drop_down, from_date=None, to_date=None):
        return {
            '__EVENTVALIDATION': e,
            '__VIEWSTATE': v,
            '__VIEWSTATEGENERATOR': '53A94410',
            'ctl00$main$DropDownList1': drop_down,
            'ctl00$main$ImageButton1.x': '14',
            'ctl00$main$ImageButton1.y': '14',
            'ctl00$main$ResultFormatGroup': 'optExport',
            'ctl00$main$fromDate': from_date,
            'ctl00$main$tomDate': to_date
        }

    def __search_payload(self, url, company_name=None, org_number=None):
        e, v = self.__get_request_to_setup_asp_fields(url)
        return {
            '__EVENTVALIDATION': e,
            '__VIEWSTATE': v,
            '__VIEWSTATEGENERATOR': 'C8125695',
            'ctl00$main$txtNamn': company_name,
            'ctl00$main$txtOrgNr': org_number,
            'ctl00$main$btnSeekkBolag.x': '18',
            'ctl00$main$btnSeekkBolag.y': '5',
        }


class Company(Client):
    def __init__(self, company_name=None, org_number=None):
        super(Company, self).__init__()
        self.company = self.search_company(company_name, org_number)

    def get_current_holdings(self):
        return self.get_company_insider_current_holdings(self.company)

    def get_current_insiders(self):
        return self.get_company_insiders_people(self.company)

    def get_historical_transactions(self, from_date, to_date):
        return self.get_company_transactions(self.company, from_date, to_date)

    def get_historical_holdings(self):
        return self.get_company_insider_historical_holdings(self.company)

    def get_historical_position_changes(self):
        return self.get_company_insider_position_changes(self.company)
