__author__ = "Julián Arenas-Guerrero"
__credits__ = ["Julián Arenas-Guerrero"]

__license__ = "Apache-2.0"
__maintainer__ = "Julián Arenas-Guerrero"
__email__ = "julian.arenas.guerrero@upm.es"


from argparse import ArgumentParser

from .__init__ import *


if __name__ == "__main__":
    parser = ArgumentParser(
        prog='COTTAS',
        description='Efficient RDF-star graph management in compressed space',
        epilog='Copyright © 2023 Julián Arenas-Guerrero')

    parser.add_argument('operation')
    parser.add_argument('arg1')
    parser.add_argument('arg2', nargs='?', default=None)
    parser.add_argument('arg3', nargs='?', default=None)

    args = parser.parse_args()

    if args.operation.lower() == 'rdf2cottas':
        rdf_2_cottas(args.arg1, args.arg2)

    elif args.operation.lower() == 'rdf2cottasnoid':
        rdf_2_cottas(args.arg1, args.arg2, create_id=False)

    elif args.operation.lower() == 'cottas2rdf':
        cottas_2_rdf(args.arg1, args.arg2)

    elif args.operation.lower() == 'search':
        print(search(args.arg1, args.arg2))

    elif args.operation.lower() == 'cat':
        cat(args.arg1, args.arg2, args.arg3)

    elif args.operation.lower() == 'diff':
        diff(args.arg1, args.arg2, args.arg3)

    elif args.operation.lower() == 'createid':
        create_id(args.arg1)

    elif args.operation.lower() == 'removeid':
        remove_id(args.arg1)

    elif args.operation.lower() == 'expand':
        create_id(args.arg1, expand=True)

    elif args.operation.lower() == 'shrink':
        remove_id(args.arg1, shrink=True)

    elif args.operation.lower() == 'verify':
        print(verify(args.arg1))

    elif args.operation.lower() == 'info':
        info_df = info(args.arg1)
        print(duckdb.query("SELECT * FROM info_df"))

    else:
        print('Invalid COTTAS option, arg1 must be `search`, `verify`, `info`, `cat`, `diff`, `cottas2rdf`, '
              '`rdf2cottas`, `rdf2cottasNoID`, `createID`, `removeID`, `expand` or `shrink`.')
