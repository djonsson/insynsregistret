#! ../env/bin/python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import zipfile
import StringIO
import requests


class Session(object):

    DEFAULT_SETTINGS = {
        'url': 'http://insynsok.fi.se/SearchPage.aspx'
    }

    ASP_NET_FIELDS = {}

    def __init__(self):
        self.session = requests.Session()
        self.__event_validation__()

    def get(self, from_date='2016-01-02', to_date='2016-05-12'):
        response = self.session.post(self.DEFAULT_SETTINGS['url'], data=self.__payload__(from_date, to_date))

        z = zipfile.ZipFile(StringIO.StringIO(response.content))
        for file in z.namelist():
            print(file)
        z.extractall()

    def __event_validation__(self):
        get_response = self.session.get(self.DEFAULT_SETTINGS['url'])
        soup = BeautifulSoup(get_response.content, 'lxml')
        self.ASP_NET_FIELDS['__EVENTVALIDATION'] = soup.find("input", {"id": "__EVENTVALIDATION"}).get('value')
        self.ASP_NET_FIELDS['__VIEWSTATE'] = soup.find("input", {"id": "__VIEWSTATE"}).get('value')

    def __payload__(self, from_date, to_date):
        return {'__EVENTVALIDATION':            self.ASP_NET_FIELDS['__EVENTVALIDATION'],
                '__VIEWSTATE':                  self.ASP_NET_FIELDS['__VIEWSTATE'],
                '__VIEWSTATEGENERATOR':         '53A94410',
                'ctl00$main$DropDownList1':     'Transaktioner',
                'ctl00$main$ImageButton1.x':    '14',
                'ctl00$main$ImageButton1.y':    '14',
                'ctl00$main$ResultFormatGroup': 'optExport',
                'ctl00$main$fromDate':          from_date,
                'ctl00$main$tomDate':           to_date
                }
