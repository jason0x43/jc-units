import logging

LOG = logging.getLogger(__name__)

# special cases to try, like when a user asks to convert 25 pints to oz
SPECIAL = {
    'ounce': 'floz',
    'boltzmann_constant': 'km'
}


class Converter(object):
    def __init__(self, definitions=None, separator='>', precision=None):
        from pint import UnitRegistry

        self.ureg = UnitRegistry()
        self.ureg.load_definitions('unit_defs.txt')
        self.load_definitions(definitions)
        self.separator = separator
        self.precision = precision

    def load_definitions(self, definitions):
        if not definitions:
            return

        if not isinstance(definitions, (list, tuple)):
            definitions = [definitions]
        for d in definitions:
            LOG.info('loading definitions from %s', d)
            self.ureg.load_definitions(d)

    def convert(self, query):
        from pint.unit import DimensionalityError
        import re

        Q_ = self.ureg.Quantity

        # step 1: split the query into an input value and output units at a
        # self.separator
        value, sep, units = query.partition(self.separator)
        value = re.sub(r'([A-Za-z]) ([A-Za-z])', r'\1_\2', value.strip())
        units = re.sub(r'(\w) (\w)', r'\1_\2', units.strip())

        LOG.debug('query: %s', query)
        LOG.debug('input: %s', value)
        LOG.debug('units: %s', units)

        in_val = Q_(value)
        out_units = Q_(units.replace(' ', '_'))

        try:
            out_val = in_val.to(out_units)
        except DimensionalityError, e:
            if str(e.units1) in SPECIAL:
                in_val2 = in_val.magnitude * Q_(SPECIAL[str(e.units1)])
                out_val = in_val2.to(out_units)
            elif str(e.units2) in SPECIAL:
                out_units2 = Q_(SPECIAL[str(e.units2)])
                out_val = in_val.to(out_units2)
            else:
                raise

        LOG.debug(u'converted {0} to {1:P}'.format(in_val, out_val))

        magnitude = out_val.magnitude
        units = out_val.units

        if self.precision:
            from decimal import Decimal
            rval = Decimal('1.' + '0'*self.precision)
            magnitude = Decimal(out_val.magnitude).quantize(rval)

        return (magnitude, u'{0} {1}'.format(magnitude, units))


if __name__ == '__main__':
    from sys import argv
    print Converter().convert(argv[1])
