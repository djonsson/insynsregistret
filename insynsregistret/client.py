#! ../env/bin/python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import zipfile
import StringIO
import requests


class Session(object):
    """
    Sets up a session object that is used to interact with the insynssok. In order to produce valid requests
    we need a session cookie (which is automatically registered by using requests.Session() in the __init__ method
    and using it to perform the __event_validation__ method.

    The cookie that is required for the api is acquired by simply performing a GET request to SearchPage.apsx.

    'cookie': ASP.NET_SessionId=2hp0ly45dz2ceh45bbia2ufw;
              WT_FPC=id=f9b0b3db-5600-4c8c-a920-48cace6b052dlv=1463047439657ss=1463045836001;
              insynsok=ffffffffc3a01c7b45525d5f4f58455e445a4a423660

    The cookie is stored in the Session() object and applied to all requests. In order to perform valid requests to
    insynssok we also require the asp.net parameters (__EVENTVALIDATION and __VIEWSTATE).

    These parameters are stored in hidden input fields as values on the page. Why are they there?
    The short answer is event validation is designed to protect the web site from having values injected into the page
    that can be used to exploit the application in some way.

    You can read more about it here:
    https://msdn.microsoft.com/en-us/library/system.web.ui.page.enableeventvalidation.aspx

    We add these parameters by calling the private method __event_validation__, which parses the html, finds the fields
    and store them in ASP_NET_FIELDS(dict).

    """

    DEFAULT_SETTINGS = {
        'url': 'http://insynsok.fi.se/SearchPage.aspx'
    }

    ASP_NET_FIELDS = {}

    def __init__(self):
        self.session = requests.Session()
        self.__event_validation__()

    def __event_validation__(self):
        get_response = self.session.get(self.DEFAULT_SETTINGS['url'])
        soup = BeautifulSoup(get_response.content, 'lxml')
        self.ASP_NET_FIELDS['__EVENTVALIDATION'] = soup.find("input", {"id": "__EVENTVALIDATION"}).get('value')
        self.ASP_NET_FIELDS['__VIEWSTATE'] = soup.find("input", {"id": "__VIEWSTATE"}).get('value')

    def __payload__(self, from_date, to_date):
        return {
                '__EVENTVALIDATION':            self.ASP_NET_FIELDS['__EVENTVALIDATION'],
                '__VIEWSTATE':                  self.ASP_NET_FIELDS['__VIEWSTATE'],
                '__VIEWSTATEGENERATOR':         '53A94410',
                'ctl00$main$DropDownList1':     'Transaktioner',
                'ctl00$main$ImageButton1.x':    '14',
                'ctl00$main$ImageButton1.y':    '14',
                'ctl00$main$ResultFormatGroup': 'optExport',
                'ctl00$main$fromDate':          from_date,
                'ctl00$main$tomDate':           to_date
                }

    def get(self, from_date='2016-01-02', to_date='2016-05-12'):
        response = self.session.post(self.DEFAULT_SETTINGS['url'], data=self.__payload__(from_date, to_date))
        z = zipfile.ZipFile(StringIO.StringIO(response.content))
        for file in z.namelist():
            print(file)
        z.extractall()