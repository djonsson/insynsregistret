#! ../env/bin/python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from cache import Cache
import zipfile
import StringIO
import requests
import xml.etree.ElementTree as ET


class Session(object):

    DEFAULT_SETTINGS = {
        'cache_directory': '~/.cache-insyn/'
    }

    def __init__(self):
        self.__session = requests.Session()
        self.__cache = Cache(self.DEFAULT_SETTINGS)
        self.__cache_dir = self.__cache.get_cache_directory()

    def search_transactions(self, from_date, to_date):
        filename = self.__cache_dir + ('_Transaktioner_%s_%s__(sv-SE).xml' % (from_date, to_date))
        url = 'http://insynsok.fi.se/SearchPage.aspx'
        e, v = self.__get_request_to_setup_asp_fields(url)

        if not self.__cache.file_exist(filename):
            response = self.__session.post(url, data=self.__request_payload(e, v, drop_down='Transaktioner', from_date=from_date, to_date=to_date))
            z = zipfile.ZipFile(StringIO.StringIO(response.content))
            z.extractall(path=self.__cache_dir)
        if self.__cache.is_empty(filename):
            return None
        return ET.parse(filename).getroot()

    def search_insiders(self):
        filename = self.__cache_dir + '_Insyn__(sv-SE).xml'
        url = 'http://insynsok.fi.se/SearchPage.aspx'
        e, v = self.__get_request_to_setup_asp_fields(url)
        response = self.__session.post(url, data=self.__request_payload(e, v, drop_down='Insyn', from_date='2015-11-18', to_date='2015-12-18'))

        z = zipfile.ZipFile(StringIO.StringIO(response.content))
        z.extractall(path=self.__cache_dir)
        return ET.parse(filename).getroot()

    def search_company(self, company_name=None, org_number=None):
        url = 'http://insynsok.fi.se/Startpage.aspx?searchtype=0&culture=sv-SE'
        response = self.__session.post(url, data=self.__search_payload(url, company_name=company_name, org_number=org_number))
        e, v = self.__get_asp_fields_from_response(response)

        if company_name is 'co':
            print response.content

        response = self.__session.post(response.url, data=self.__request_payload(e, v, drop_down='Transaktioner', from_date='2015-11-18', to_date='2015-12-18'))
        z = zipfile.ZipFile(StringIO.StringIO(response.content))
        z.extractall(path=self.__cache_dir)

        response2 = self.__session.post(response.url, data=self.__request_payload(e, v, drop_down='Innehav', from_date='2015-11-18', to_date='2015-12-18'))
        z = zipfile.ZipFile(StringIO.StringIO(response2.content))
        z.extractall(path=self.__cache_dir)

        response2 = self.__session.post(response.url, data=self.__request_payload(e, v, drop_down='HistorisktInnehav', from_date='2016-01-01', to_date='2016-05-30'))
        z = zipfile.ZipFile(StringIO.StringIO(response2.content))
        z.extractall(path=self.__cache_dir)

        response2 = self.__session.post(response.url, data=self.__request_payload(e, v, drop_down='Insyn', from_date='2015-11-18', to_date='2015-12-18'))
        z = zipfile.ZipFile(StringIO.StringIO(response2.content))
        z.extractall(path=self.__cache_dir)

        response2 = self.__session.post(response.url, data=self.__request_payload(e, v, drop_down='Befattningsforandringar', from_date='2015-11-18', to_date='2015-12-18'))
        z = zipfile.ZipFile(StringIO.StringIO(response2.content))
        z.extractall(path=self.__cache_dir)

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
    def __request_payload(e, v, drop_down, from_date, to_date):
        return {
            '__EVENTVALIDATION':            e,
            '__VIEWSTATE':                  v,
            '__VIEWSTATEGENERATOR':         '53A94410',
            'ctl00$main$DropDownList1':     drop_down,
            'ctl00$main$ImageButton1.x':    '14',
            'ctl00$main$ImageButton1.y':    '14',
            'ctl00$main$ResultFormatGroup': 'optExport',
            'ctl00$main$fromDate':          from_date,
            'ctl00$main$tomDate':           to_date
        }

    def __search_payload(self, url, company_name=None, org_number=None):
        e, v = self.__get_request_to_setup_asp_fields(url)
        return {
            '__EVENTVALIDATION':            e,
            '__VIEWSTATE':                  v,
            '__VIEWSTATEGENERATOR':         'C8125695',
            'ctl00$main$txtNamn':           company_name,
            'ctl00$main$txtOrgNr':          org_number,
            'ctl00$main$btnSeekkBolag.x':   '18',
            'ctl00$main$btnSeekkBolag.y':   '5',
        }

