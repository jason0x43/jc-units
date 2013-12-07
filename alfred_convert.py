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
    'EUR',
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
        self.currencies_file = os.path.join(self.cache_dir, 'currencies.txt')
        self.load_currencies()
        self.separator = self.config.get('separator') or '>'
        self.precision = self.config.get('precision') or None
        self.config['separator'] = self.separator
        self.config['precision'] = self.precision
        self.converter = Converter(self.currencies_file,
            separator=self.separator, precision=self.precision)

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
        query = query.strip()
        try:
            value, text = self.converter.convert(query)
        except Exception, e:
            LOG.exception('Error converting')
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

    def tell_command(self, query=None):
        return [
            Item('Open config file...', arg='open|' + self.config_file,
                valid=True),
            Item('Open debug log...', arg='open|' + self.log_file,
                valid=True),
        ]

    def do_command(self, query=None):
        '''Open the config file.'''
        LOG.debug('doing command ' + query)
        cmd, sep, arg = query.partition('|')

        if cmd == 'open':
            LOG.debug('opening ' + arg)
            from subprocess import call
            call(['open', arg])

if __name__ == '__main__':
    from sys import argv
    ap = UnitsWorkflow()
    getattr(ap, argv[1])(*argv[2:])
