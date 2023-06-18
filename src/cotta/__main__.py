__author__ = "Julián Arenas-Guerrero"
__credits__ = ["Julián Arenas-Guerrero"]

__license__ = "Apache-2.0"
__maintainer__ = "Julián Arenas-Guerrero"
__email__ = "julian.arenas.guerrero@upm.es"


import argparse

from .__init__ import *
from .utils import *


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='COTTA',
        description='Columnar triple table storage for efficient RDF management',
        epilog='Copyright © 2023 Julián Arenas-Guerrero')

    parser.add_argument('operation')
    parser.add_argument('arg1')
    parser.add_argument('arg2', nargs='?', default=None)
    parser.add_argument('arg3', nargs='?', default=None)

    args = parser.parse_args()

    if args.operation.lower() == 'search':
        results_df = search(args.arg1, args.arg2, args.arg3)

        print(results_df)

    elif args.operation.lower() == 'verify':
        print(verify(args.arg1))

    elif args.operation.lower() == 'info':
        print(info(args.arg1))

    elif args.operation.lower() == 'cat':
        cat(args.arg1, args.arg2, args.arg3)

    elif args.operation.lower() == 'diff':
        diff(args.arg1, args.arg2, args.arg3)

    elif args.operation.lower() == 'rdf2cotta':
        rdf_2_cotta(args.arg1, args.arg2)

    elif args.operation.lower() == 'cotta2rdf':
        cotta_2_rdf(args.arg1, args.arg2)

    elif args.operation.lower() == 'createid':
        create_id(args.arg1)

    elif args.operation.lower() == 'removeid':
        remove_id(args.arg1)

    else:
        print(
            'Invalid COTTA option, arg1 must be `search`, `verify`, `info`, `cat`, `diff`, '
            '`cotta2rdf`, `rdf2cotta`, `createID` or `removeID`.')
