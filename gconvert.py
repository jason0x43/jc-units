#!/usr/bin/env python

import json
import re
import logging
from urllib import urlopen, quote_plus


LOG = logging.getLogger(__name__)

api = 'http://www.google.com/ig/calculator?hl=en&'


def _parse_response(response):
    resp = response.replace(r'\x', r'\u00')
    resp = resp.replace('\xa0', '')
    resp = re.sub('([a-z]+):', '"\\1" :', resp)

    data = json.loads(resp)
    if len(data['error']) > 0:
        raise Exception(data['error'])

    rhs = data['rhs']

    # scientific notation with a negative exponent
    rhs = re.sub(r'\s*&#215;\s*10\s*<sup>-(\d+)</sup>', 'e-\\1', rhs)
    # scientific notation with a non-negative exponent
    rhs = re.sub(r'\s*&#215;\s*10\s*<sup>(\d+)</sup>', 'e+\\1', rhs)
    # fractions
    rhs = re.sub(r'<sup>(-?\d+)</sup>&#8260;<sub>(-?\d+)</sub>', '\\1/\\2',
                 rhs)
    # simple exponents
    rhs = re.sub(r'<sup>(-?\d+)</sup>', '^\\1', rhs)

    data['rhs'] = rhs

    value = data['rhs'].split(' ')[0]
    value = float(value) if '.' in value else int(value)
    return value, data['rhs']


def convert(query):
    dst_units = None
    if '>' in query:
        query, sep, dst_units = query.partition('>')

    query = 'q=' + quote_plus(query)
    if dst_units:
        query += '=?' + quote_plus(dst_units)
    url = api + query
    LOG.debug('opening url: %s', url)
    resp = urlopen(url).read()
    return _parse_response(resp)


def convert_simple(value, src_units, dst_units):
    in_str = '{}{}>{}'.format(value, src_units, dst_units)
    return convert(in_str)


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)-15s %(message)s',
                        level=logging.DEBUG)

    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('query')
    args = parser.parse_args()
    print convert(args.query)
