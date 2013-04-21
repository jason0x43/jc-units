#!/usr/bin/env python
# coding=UTF-8

from sys import stdout
import alfred
import gconvert as convert
import logging
import re
import os.path


FORMAT = '%(levelname)s [%(asctime)s] %(name)s - %(message)s'
LOG = logging.getLogger(__name__)
LOG_FILE = os.path.join(alfred.get_cache_dir(), 'debug.log')

logging.basicConfig(level=logging.ERROR, format=FORMAT, filename=LOG_FILE)


def _out(msg):
    '''Output a string'''
    stdout.write(msg.encode('utf-8'))


def tell_convert(query):
    LOG.debug('called with query "{}"'.format(query))
    match = re.match('(?P<value>\d+(\.\d+)?)\s*(?P<src>[a-zA-Z]+)(\s+\w+)?'
                     '\s+(?P<dst>[a-zA-Z]+)', query.strip())
    if not match:
        return [alfred.Item('Waiting for input...')]

    value = float(match.group('value'))
    src_units = match.group('src').lower()
    dst_units = match.group('dst').lower()

    try:
        value, text = convert.convert(value, src_units, dst_units)
    except Exception, e:
        if e.message.startswith('Parse error in query'):
            return [alfred.Item('Waiting for input...')]
        else:
            try:
                int(e.message)
                return [alfred.Item('Waiting for input...')]
            except:
                pass
        raise e

    return [alfred.Item(text, arg=value, valid=True,
                        subtitle='Action this item to copy {} to the '
                                 'clipboard'.format(value))]


def do_convert(value):
    _out(value)


def tell(name, query=''):
    '''Tell something'''
    try:
        cmd = 'tell_{}'.format(name)
        if cmd in globals():
            items = globals()[cmd](query)
        else:
            items = [alfred.Item('Invalid action "{}"'.format(name))]
    except Exception, e:
        LOG.exception('Exception during tell')
        items = [alfred.Item('Error: {}'.format(e))]

    _out(alfred.to_xml(items))


def do(name, query=''):
    '''Do something'''
    try:
        cmd = 'do_{}'.format(name)
        if cmd in globals():
            globals()[cmd](query)
        else:
            _out('Invalid command "{}"'.format(name))
    except Exception, e:
        LOG.exception('Exception during do')
        _out('Error: {}'.format(e))


if __name__ == '__main__':
    sh = logging.StreamHandler()
    sh.setFormatter(logging.Formatter(FORMAT))
    LOG.addHandler(sh)
    LOG.setLevel(logging.DEBUG)

    from sys import argv
    globals()[argv[1]](*argv[2:])
