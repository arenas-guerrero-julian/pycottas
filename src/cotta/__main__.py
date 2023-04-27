__author__ = "Julián Arenas-Guerrero"
__credits__ = ["Julián Arenas-Guerrero"]

__license__ = "Apache-2.0"
__maintainer__ = "Julián Arenas-Guerrero"
__email__ = "julian.arenas.guerrero@upm.es"


import argparse

from .graph import *
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

    if args.operation == 'cottaSearch':
        result_df = duckdb.query(translate_triple_pattern(f"{args.arg1}", args.arg2)).df()
        if args.arg3 is None:
            print(result_df)
        else:
            result_df.to_csv(args.arg3, index=False, sep='\t')

    elif args.operation == 'cottaVerify':
        verify_query = f"SELECT * FROM parquet_scan('{args.arg1}') LIMIT 0"
        cotta_df = duckdb.query(verify_query).df()

        cotta_columns = [c.lower() for c in cotta_df.columns]
        print(set(cotta_columns) <= {'s', 'p', 'o', 'g'})

    elif args.operation == 'cottaInfo':
        print(cotta_info(args.arg1))

    elif args.operation == 'cottaCat':
        g1 = Graph()
        g1.parse(args.arg1)

        g2 = Graph()
        g2.parse(args.arg1)

        g1 += g2
        g1.serialize(args.arg3)

    elif args.operation == 'cotta2rdf' or args.operation == 'rdf2cotta':
        g = Graph()
        g.parse(args.arg1)
        g.serialize(args.arg2)

    else:
        print('Invalid COTTA option, arg1 must be `cottaSearch`, `cottaVerify`, `cottaInfo`, `cottaCat`, `cotta2rdf` or `rdf2cotta`.')
