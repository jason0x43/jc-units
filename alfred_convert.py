#!/usr/bin/env python
# coding=UTF-8

import convert as convert
import logging
import re
import jcalfred


LOG = logging.getLogger(__name__)


class Workflow(jcalfred.Workflow):
    def __init__(self):
        super(Workflow, self).__init__()
        #self.log_level = 'DEBUG'

    def _convert(self, query):
        try:
            value, text = convert.convert(query)
        except Exception, e:
            if e.message.startswith('Parse error in query'):
                return [jcalfred.Item('Waiting for input...')]
            else:
                try:
                    int(e.message)
                    return [jcalfred.Item('Waiting for input...')]
                except:
                    pass
            raise e

        return [jcalfred.Item(text, arg=str(value), valid=True,
                              subtitle='Action this item to copy %s to the '
                                       'clipboard' % value)]

    def tell_convert_simple(self, query):
        '''Perform a simple conversion query.'''
        LOG.debug('called with query "%s"', query)

        try:
            return self._convert(query)
        except:
            return [jcalfred.Item('Waiting for input...')]

    def tell_convert(self, query):
        '''Perform a general conversion query.'''
        LOG.debug('called with query "%s"', query)

        if len(query) == 0:
            return [
                jcalfred.Item('Perform a freeform conversion'),
                jcalfred.Item('Syntax', subtitle="'input > units'   (the '> "
                              "units' is optional)"),
                jcalfred.Item('Examples', subtitle='1cm * 1in,   '
                              '1cm * 1in > in^2,   1cm * 1in + 3in^2'),
                jcalfred.Item('Remember, units matter', subtitle="If "
                              "you multiple two lengths, you're going to get "
                              "an area"),
            ]
        else:
            return self._convert(query)


if __name__ == '__main__':
    from sys import argv
    ap = Workflow()
    getattr(ap, argv[1])(*argv[2:])
