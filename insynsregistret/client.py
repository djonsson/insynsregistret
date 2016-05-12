#! ../env/bin/python
# -*- coding: utf-8 -*-

import zipfile
import StringIO
import requests


class Session(object):

    DEFAULT_SETTINGS = {
        'url': 'http://insynsok.fi.se/SearchPage.aspx',
        'headers': {
            'origin': "http//insynsok.fi.se",
            'upgrade-insecure-requests': "1",
            'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 "
                          "(KHTML, like Gecko) Chrome/51.0.2704.36 Safari/537.36",
            'content-type': "application/x-www-form-urlencoded",
            'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            'referer': "http//insynsok.fi.se/SearchPage.aspx?reporttype=0&culture=sv-SE&",
            'accept-encoding': "gzip, deflate",
            'accept-language': "en-US,en;q=0.8,sv;q=0.6",
            'cookie': "ASP.NET_SessionId=2hp0ly45dz2ceh45bbia2ufw; "
                      "WT_FPC=id=f9b0b3db-5600-4c8c-a920-48cace6b052dlv=1463047439657ss=1463045836001; "
                      "insynsok=ffffffffc3a01c7b45525d5f4f58455e445a4a423660",
            'cache-control': "no-cache",
        }
    }

    def __init__(self):
        pass

    def get(self, from_date='2016-01-02', to_date='2016-05-12'):
        response = requests.post(self.DEFAULT_SETTINGS['url'],
                                 data=self.__payload__(from_date, to_date),
                                 headers=self.DEFAULT_SETTINGS['headers'])

        z = zipfile.ZipFile(StringIO.StringIO(response.content))
        for file in z.namelist():
            print(file)
        z.extractall()

    @staticmethod
    def __payload__(from_date, to_date):
        return {'__EVENTVALIDATION': '/wEWDQLz17mzCALupZC3DALVvMvkCALOkpvRAwLuqaGYAgLghIvcCQL/l4qFBQLYqZBBAoqhrtUD'
                                     'Arax8coKAsDa2ZEFAtmB4skKAv2novYCqE8dfHxmMAWpbDMiSQSWUuoHSlY=',
                '__VIEWSTATE': '/wEPDwULLTE5NTkzOTE5NjYPZBYCZg9kFgICAw9kFgQCAQ9kFiACAQ88KwANAQwUKwAFBQ8wOjAsMDoxLD'
                               'A6MiwwOjMUKwACFgIeBFRleHQFBUJvbGFnZBQrAAIWAh8ABQxJbnN5bnNwZXJzb25kFCsAAhYEHwAFBURh'
                               'dHVtHghJbWFnZVVybAUsfi9QYWdlVGVtcGxhdGVzL2ltYWdlcy9GSV9HcmVlbi1kb3QtMTBweC5wbmdkFC'
                               'sAAhYCHwAFGFJlZ2lzdHJlcmFkIGluc3luc2hhbmRlbGRkAgMPDxYCHwAFL1RyYW5zYWt0aW9uZXIgbWVs'
                               'bGFuICAyMDE2LTA1LTAyIG9jaCAyMDE2LTA1LTExZGQCBQ8QDxYEHwAFDkV4cG9ydGVyYSBkYXRhHgdDaG'
                               'Vja2VkZ2RkZGQCBw8PFgQfAAUUT3JnYW5pc2F0aW9uc251bW1lcjoeB1Zpc2libGVoZGQCDQ8QDxYEHwJo'
                               'HwAFD1Zpc2EgcMOlIHNrw6RybWRkZGQCDw8PFgIfAAUFVsOkbGpkZAIRDxBkEBUCDVRyYW5zYWt0aW9uZX'
                               'IOSW5zeW5zcGVyc29uZXIVAg1UcmFuc2FrdGlvbmVyBUluc3luFCsDAmdnFgFmZAITDw8WAh8ABQZGciBv'
                               'IG1kZAIVDw8WAh8ABQoyMDE2LTA1LTAyZGQCFw8PFgIfAAUFVCBvIG1kZAIZDw8WAh8ABQoyMDE2LTA1LT'
                               'ExZGQCGw8PFgIfA2hkZAIdDw8WAh8BBSh+L1BhZ2VUZW1wbGF0ZXMvaW1hZ2VzL2J1dHRvbl9zZWFyY2gu'
                               'Z2lmZGQCHw8PFgIfAAUNRsO2cmtsYXJpbmdhcmRkAiMPDxYCHwBlZGQCJQ8PFgIfAAUFRGF0dW1kZAICDw'
                               '8WAh8ABRFUZm4gMDgtNDA4IDk4MSA0NGRkGAIFHl9fQ29udHJvbHNSZXF1aXJlUG9zdEJhY2tLZXlfXxYE'
                               'BRRjdGwwMCRtYWluJG9wdEV4cG9ydAUUY3RsMDAkbWFpbiRvcHRTY3JlZW4FFGN0bDAwJG1haW4kb3B0U2'
                               'NyZWVuBRdjdGwwMCRtYWluJEltYWdlQnV0dG9uMQUUY3RsMDAkbWFpbiRHcmlkVmlldzEPPCsACgEIZmTd'
                               'qwx+nK5k/Krlp9V6aospAXXFWw==',
                '__VIEWSTATEGENERATOR': '53A94410',
                'ctl00$main$DropDownList1': 'Transaktioner',
                'ctl00$main$ImageButton1.x': '14',
                'ctl00$main$ImageButton1.y': '14',
                'ctl00$main$ResultFormatGroup': 'optExport',
                'ctl00$main$fromDate': from_date,
                'ctl00$main$tomDate': to_date}
