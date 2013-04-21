#!/usr/bin/env python

import json
import re
from urllib import urlopen


api = 'http://www.google.com/ig/calculator?hl=en&q={}{}=?{}'


def convert(value, src_units, dst_units):
    url = api.format(value, src_units, dst_units)
    data = urlopen(url).read().decode('utf-8', 'ignore')
    # Convert to valid JSON: {foo: "1"} -> {"foo" : "1"}
    data = re.sub('([a-z]+):', '"\\1" :', data)
    data = json.loads(data)
    if len(data['error']) > 0:
        raise Exception(data['error'])

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
