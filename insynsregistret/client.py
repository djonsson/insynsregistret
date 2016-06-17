#! ../env/bin/python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from cache import Cache
import zipfile
import StringIO
import requests
import xml.etree.ElementTree as ET


class Session(object):

    __DEFAULT_SETTINGS = {
        'cache_directory': '~/.cache-insyn/'
    }

    __BASE_URL = 'http://insynsok.fi.se'

    def __init__(self):
        self.__session = requests.Session()
        self.__cache = Cache(self.__DEFAULT_SETTINGS)
        self.__cache_dir = self.__cache.get_cache_directory()

    def search_transactions(self, from_date, to_date):
        url = self.__BASE_URL + '/SearchPage.aspx'
        filename = self.__cache_dir + ('_Transaktioner_%s_%s__(sv-SE).xml' % (from_date, to_date))
        e, v = self.__get_request_to_setup_asp_fields(url)

        if not self.__cache.file_exist(filename):
            response = self.__session.post(url, data=self.__request_payload(e, v, drop_down='Transaktioner',
                                                                            from_date=from_date, to_date=to_date))
            z = zipfile.ZipFile(StringIO.StringIO(response.content))
            z.extractall(path=self.__cache_dir)
        if self.__cache.is_empty(filename):
            return None
        return ET.parse(filename).getroot()

    def search_insiders(self, from_date, to_date):
        url = self.__BASE_URL + '/SearchPage.aspx'
        filename = self.__cache_dir + '_Insyn__(sv-SE).xml'
        e, v = self.__get_request_to_setup_asp_fields(url)
        response = self.__session.post(url, data=self.__request_payload(e, v, drop_down='Insyn', from_date=from_date,
                                                                        to_date=to_date))

        z = zipfile.ZipFile(StringIO.StringIO(response.content))
        z.extractall(path=self.__cache_dir)
        return ET.parse(filename).getroot()

    def search_company(self, company_name=None, org_number=None):
        search_term = ''.join(filter(None, (company_name, org_number)))

        url = self.__BASE_URL + '/Startpage.aspx?searchtype=0&culture=sv-SE'
        response = self.__session.post(url, data=self.__search_payload(url, company_name=company_name,
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
        z = zipfile.ZipFile(StringIO.StringIO(response.content))
        z.extractall(path=self.__cache_dir)

    def get_company_insider_current_holdings(self, company):
        e, v, response = self.__get_company_asp_fields(company)
        response = self.__session.post(response.url, data=self.__request_payload(e, v, drop_down='Innehav'))
        z = zipfile.ZipFile(StringIO.StringIO(response.content))
        z.extractall(path=self.__cache_dir)

    def get_company_insider_historical_holdings(self, company):
        e, v, response = self.__get_company_asp_fields(company)
        response = self.__session.post(response.url, data=self.__request_payload(e, v, drop_down='HistorisktInnehav'))
        z = zipfile.ZipFile(StringIO.StringIO(response.content))
        z.extractall(path=self.__cache_dir)

    def get_company_insiders_people(self, company):
        e, v, response = self.__get_company_asp_fields(company)
        response = self.__session.post(response.url, data=self.__request_payload(e, v, drop_down='Insyn'))
        z = zipfile.ZipFile(StringIO.StringIO(response.content))
        z.extractall(path=self.__cache_dir)

    def get_company_insider_position_changes(self, company):
        e, v, response = self.__get_company_asp_fields(company)
        response = self.__session.post(response.url, data=self.__request_payload(e, v, drop_down='Befattningsforandringar'))
        z = zipfile.ZipFile(StringIO.StringIO(response.content))
        z.extractall(path=self.__cache_dir)

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

