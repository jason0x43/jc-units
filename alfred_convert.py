#!/usr/bin/env python
# coding=UTF-8

import gconvert as convert
import logging
import re
import jalf


LOG = logging.getLogger(__name__)


class Workflow(jalf.AlfredWorkflow):
    def _convert(self, value, src_units, dst_units):
        try:
            value, text = convert.convert(value, src_units, dst_units)
        except Exception, e:
            if e.message.startswith('Parse error in query'):
                return [jalf.Item('Waiting for input...')]
            else:
                try:
                    int(e.message)
                    return [jalf.Item('Waiting for input...')]
                except:
                    pass
            raise e

        return [jalf.Item(text, arg=value, valid=True,
                          subtitle='Action this item to copy {} to the '
                                   'clipboard'.format(value))]

    def tell_convert(self, query):
        LOG.debug('called with query "{}"'.format(query))

        # 1cm [in] ft
        match = re.match('(?P<value>\d+(\.\d+)?)\s*(?P<src>[a-zA-Z]+)(\s+\w+)?'
                         '\s+(?P<dst>[a-zA-Z]+)', query.strip())
        if match:
            value = float(match.group('value'))
            src_units = match.group('src').lower()
            dst_units = match.group('dst').lower()
            return self._convert(value, src_units, dst_units)

        return [jalf.Item('Waiting for input...')]

    def do_convert(self, value):
        self.puts(value)
