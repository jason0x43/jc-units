import logging

LOG = logging.getLogger(__name__)

# special cases to try, like when a user asks to convert 25 pints to oz
SPECIAL = {
    'ounce': 'floz',
    'boltzmann_constant': 'km'
}


class Converter(object):
    def __init__(self, definitions=None, separator='>'):
        from pint import UnitRegistry

        self.ureg = UnitRegistry()
        self.ureg.load_definitions('unit_defs.txt')
        self.load_definitions(definitions)
        self.separator = separator

    def load_definitions(self, definitions):
        if not definitions:
            return

        if not isinstance(definitions, (list, tuple)):
            definitions = [definitions]
        for d in definitions:
            LOG.info('loading definitions from %s', d);
            self.ureg.load_definitions(d)

    def convert(self, query):
        from pint.unit import DimensionalityError

        Q_ = self.ureg.Quantity

        # step 1: split the query into an input value and output units at a
        # self.separator
        in_val, to, out_units = query.partition(self.separator)

        in_val = Q_(in_val)
        out_units = Q_(out_units)

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

        return (out_val.magnitude, u'{0:P}'.format(out_val))


if __name__ == '__main__':
    from sys import argv
    Converter().convert(argv[1])
