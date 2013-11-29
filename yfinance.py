#
# This module uses YQL to download the current currency exchange rates from Yahoo! Finance.
#
import logging
import requests

LOG = logging.getLogger(__name__)
API = 'http://query.yahooapis.com/v1/public/yql'


def get_rates(currencies):
    from urllib import quote
    if isinstance(currencies, (list, tuple)):
        currencies = ','.join(currencies)
    query = "select Name, Rate from yahoo.finance.xchange where pair='{0}'".format(currencies)
    params = {
        'q': query,
        'format': 'json',
        'env': 'store://datatables.org/alltableswithkeys'
    }

    response = requests.get(API, params=params)
    rate_data = response.json()['query']['results']['rate']
    rates = {}

    for r in rate_data:
        name = str(r['Name'])
        if '=X' in name:
            name = name.split('=')[0]
            rate = 'Invalid'
        else:
            name = name.split('/')[1]
            rate = float(r['Rate'])
        rates[name] = rate

    return rates

if __name__ == '__main__':
    from sys import argv
    print get_rates(argv[1:])
