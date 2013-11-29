#!/usr/bin/env python
# coding=UTF-8

import logging
import re
import os.path
from jcalfred import Workflow, Item
from convert import Converter


LOG = logging.getLogger(__name__)

CURRENCIES = [
    'AUD',
    'BGN',
    'BRL',
    'CAD',
    'CHF',
    'CNY',
    'CZK',
    'DKK',
    'GBP',
    'HKD',
    'HRK',
    'HUF',
    'IDR',
    'ILS',
    'INR',
    'JPY',
    'KRW',
    'LTL',
    'LVL',
    'MXN',
    'MYR',
    'NOK',
    'NZD',
    'PHP',
    'PLN',
    'RON',
    'RUB',
    'SEK',
    'SGD',
    'THB',
    'TRY',
    'ZAR'
]


class UnitsWorkflow(Workflow):
    def __init__(self):
        super(UnitsWorkflow, self).__init__()
        #self.log_level = 'DEBUG'
        self.currencies_file = os.path.join(self.cache_dir, 'currencies.txt')
        self.load_currencies()
        self.converter = Converter(self.currencies_file)

    def load_currencies(self):
        import datetime

        lines = []
        last_refresh = None
        today = datetime.date.today()

        if os.path.exists(self.currencies_file):
            with open(self.currencies_file, 'rt') as cf:
                lines = cf.readlines()

        if len(lines) > 0 and lines[0].startswith('# date:'):
            last_refresh = lines[0].split(':')[1].strip()
            last_refresh = datetime.datetime.strptime(last_refresh, '%Y-%m-%d').date()

        if not last_refresh or last_refresh != today:
            import yfinance
            rates = yfinance.get_rates(CURRENCIES)
            with open(self.currencies_file, 'wt') as cf:
                cf.write('# date: ' + today.strftime('%Y-%m-%d') + '\n')
                cf.write('USD = [currency] = usd\n')
                for k, v in rates.items():
                    cf.write('{0} = USD / {1} = {2}\n'.format(k, v, k.lower()))

    def _convert(self, query):
        try:
            value, text = self.converter.convert(query)
        except Exception, e:
            if e.message.startswith('Parse error in query'):
                return [Item('Waiting for input...')]
            else:
                try:
                    int(e.message)
                    return [Item('Waiting for input...')]
                except:
                    pass
            raise e

        return [Item(text, arg=str(value), valid=True,
                              subtitle='Action this item to copy %s to the '
                                       'clipboard' % value)]

    def tell_convert(self, query):
        '''Perform a simple conversion query.'''
        LOG.debug('called with query "%s"', query)

        try:
            return self._convert(query)
        except:
            return [Item('Waiting for input...')]


if __name__ == '__main__':
    from sys import argv
    ap = UnitsWorkflow()
    getattr(ap, argv[1])(*argv[2:])
