import logging

LOG = logging.getLogger(__name__)

# special cases to try, like when a user asks to convert 25 pints to oz
SPECIAL = {
    'ounce': 'floz'
}

def convert(query):
    from pint import UnitRegistry
    from pint.unit import DimensionalityError

    ureg = UnitRegistry()
    ureg.load_definitions('unit_defs.txt')
    Q_ = ureg.Quantity

    # step 1: split the query into an input value and output units at a '>'
    in_val, to, out_units = query.partition('>')

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
    convert(argv[1])
