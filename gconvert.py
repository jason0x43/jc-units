#!/usr/bin/env python

import json
import re
from urllib import urlopen


api = 'http://www.google.com/ig/calculator?hl=en&q={}{}=?{}'


def convert(value, src_units, dst_units):
    url = api.format(value, src_units, dst_units)

    # read and preprocess the response
    resp = urlopen(url).read()
    resp = resp.replace(r'\x', r'\u00')
    resp = resp.replace('\xa0', '')
    resp = re.sub('([a-z]+):', '"\\1" :', resp)

    data = json.loads(resp)
    if len(data['error']) > 0:
        raise Exception(data['error'])

    # postprocess the answer from Google to deal with HTML-formatted scientific
    # notation
    rhs = data['rhs']
    rhs = re.sub(r'\s*&#215;\s*10\s*<sup>-(\d+)</sup>', 'e-\\1', rhs)
    rhs = re.sub(r'\s*&#215;\s*10\s*<sup>(\d+)</sup>', 'e+\\1', rhs)
    data['rhs'] = rhs

    value = data['rhs'].split(' ')[0]
    value = float(value) if '.' in value else int(value)
    return value, data['rhs']

if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('value', type=float)
    parser.add_argument('source_units')
    parser.add_argument('dest_units')
    args = parser.parse_args()

    print convert(args.value, args.source_units, args.dest_units)
