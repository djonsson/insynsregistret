#! ../env/bin/python
# -*- coding: utf-8 -*-

import collections
import urllib
import zipfile

import StringIO
import requests

url = "http://insynsok.fi.se/SearchPage.aspx"

def transaction_payload(fromdate, todate):
    d = collections.OrderedDict()
    d['__EVENTVALIDATION'] = '/wEWDQLz17mzCALupZC3DALVvMvkCALOkpvRAwLuqaGYAgLghIvcCQL/l4qFBQLYqZBBAoqhrtUDArax8coKAsDa2ZEFAtmB4skKAv2novYCqE8dfHxmMAWpbDMiSQSWUuoHSlY='
    d['__VIEWSTATE'] = '/wEPDwULLTE5NTkzOTE5NjYPZBYCZg9kFgICAw9kFgQCAQ9kFiACAQ88KwANAQwUKwAFBQ8wOjAsMDoxLDA6MiwwOjMUKwACFgIeBFRleHQFBUJvbGFnZBQrAAIWAh8ABQxJbnN5bnNwZXJzb25kFCsAAhYEHwAFBURhdHVtHghJbWFnZVVybAUsfi9QYWdlVGVtcGxhdGVzL2ltYWdlcy9GSV9HcmVlbi1kb3QtMTBweC5wbmdkFCsAAhYCHwAFGFJlZ2lzdHJlcmFkIGluc3luc2hhbmRlbGRkAgMPDxYCHwAFL1RyYW5zYWt0aW9uZXIgbWVsbGFuICAyMDE2LTA1LTAyIG9jaCAyMDE2LTA1LTExZGQCBQ8QDxYEHwAFDkV4cG9ydGVyYSBkYXRhHgdDaGVja2VkZ2RkZGQCBw8PFgQfAAUUT3JnYW5pc2F0aW9uc251bW1lcjoeB1Zpc2libGVoZGQCDQ8QDxYEHwJoHwAFD1Zpc2EgcMOlIHNrw6RybWRkZGQCDw8PFgIfAAUFVsOkbGpkZAIRDxBkEBUCDVRyYW5zYWt0aW9uZXIOSW5zeW5zcGVyc29uZXIVAg1UcmFuc2FrdGlvbmVyBUluc3luFCsDAmdnFgFmZAITDw8WAh8ABQZGciBvIG1kZAIVDw8WAh8ABQoyMDE2LTA1LTAyZGQCFw8PFgIfAAUFVCBvIG1kZAIZDw8WAh8ABQoyMDE2LTA1LTExZGQCGw8PFgIfA2hkZAIdDw8WAh8BBSh+L1BhZ2VUZW1wbGF0ZXMvaW1hZ2VzL2J1dHRvbl9zZWFyY2guZ2lmZGQCHw8PFgIfAAUNRsO2cmtsYXJpbmdhcmRkAiMPDxYCHwBlZGQCJQ8PFgIfAAUFRGF0dW1kZAICDw8WAh8ABRFUZm4gMDgtNDA4IDk4MSA0NGRkGAIFHl9fQ29udHJvbHNSZXF1aXJlUG9zdEJhY2tLZXlfXxYEBRRjdGwwMCRtYWluJG9wdEV4cG9ydAUUY3RsMDAkbWFpbiRvcHRTY3JlZW4FFGN0bDAwJG1haW4kb3B0U2NyZWVuBRdjdGwwMCRtYWluJEltYWdlQnV0dG9uMQUUY3RsMDAkbWFpbiRHcmlkVmlldzEPPCsACgEIZmTdqwx+nK5k/Krlp9V6aospAXXFWw=='
    d['__VIEWSTATEGENERATOR'] = '53A94410'
    d['ctl00$main$DropDownList1'] = 'Transaktioner'
    d['ctl00$main$ImageButton1.x'] = '14'
    d['ctl00$main$ImageButton1.y'] = '14'
    d['ctl00$main$ResultFormatGroup'] = 'optExport'
    d['ctl00$main$fromDate'] = fromdate
    d['ctl00$main$tomDate'] = todate
    return str(urllib.urlencode(d))

headers = {
    'origin': "http//insynsok.fi.se",
    'upgrade-insecure-requests': "1",
    'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/51.0.2704.36 Safari/537.36",
    'content-type': "application/x-www-form-urlencoded",
    'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    'referer': "http//insynsok.fi.se/SearchPage.aspx?reporttype=0&culture=sv-SE&fromdate=2016-05-02&tomdate=2016-05-11",
    'accept-encoding': "gzip, deflate",
    'accept-language': "en-US,en;q=0.8,sv;q=0.6",
    'cookie': "ASP.NET_SessionId=2hp0ly45dz2ceh45bbia2ufw; "
              "WT_FPC=id=f9b0b3db-5600-4c8c-a920-48cace6b052dlv=1463047439657ss=1463045836001; "
              "insynsok=ffffffffc3a01c7b45525d5f4f58455e445a4a423660",
    'cache-control': "no-cache",
}

response = requests.request("POST", url, data=transaction_payload('2016-01-02', '2016-05-12'), headers=headers)
z = zipfile.ZipFile(StringIO.StringIO(response.content))
for file in z.namelist():
    print(file)

z.extractall()