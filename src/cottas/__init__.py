__author__ = "Julián Arenas-Guerrero"
__credits__ = ["Julián Arenas-Guerrero"]

__license__ = "Apache-2.0"
__maintainer__ = "Julián Arenas-Guerrero"
__email__ = "julian.arenas.guerrero@upm.es"


from os import mkdir

from shutil import rmtree


from .graph import *
from .term import *
from .constants import *
from .utils import *


def rdf_2_cottas(rdf_file, cottas_file, create_id=True, in_memory=True):
    if in_memory:
        g = Graph()
        g.parse(rdf_file, preserve_duplicates=True)
        if not create_id:
            g.triplestore.execute("UPDATE quads SET id=''")
        g.serialize(cottas_file)
    else:
        rmtree('.cottas_tmp', ignore_errors=True)
        mkdir('.cottas_tmp')

        g = Graph('.cottas_tmp/cottas.duckdb')
        g.parse(rdf_file, preserve_duplicates=True)
        if not create_id:
            g.triplestore.execute("UPDATE quads SET id=''")
        g.serialize(cottas_file)

        rmtree('.cottas_tmp', ignore_errors=True)


def cottas_2_rdf(cottas_file, rdf_file, in_memory=True):
    if in_memory:
        g = Graph()
        g.parse(cottas_file, preserve_duplicates=True)
        g.serialize(rdf_file)
    else:
        rmtree('.cottas_tmp', ignore_errors=True)
        mkdir('.cottas_tmp')

        g = Graph('.cottas_tmp/cottas.duckdb')
        g.parse(cottas_file, preserve_duplicates=True)
        g.serialize(rdf_file)

        rmtree('.cottas_tmp', ignore_errors=True)


def remove_id(cottas_file, in_memory=True):
    if in_memory:
        g = Graph()
        g.parse(cottas_file, preserve_duplicates=True)
        g.triplestore.execute("UPDATE quads SET id=''")
        g.serialize(cottas_file)
    else:
        rmtree('.cottas_tmp', ignore_errors=True)
        mkdir('.cottas_tmp')

        g = Graph('.cottas_tmp/cottas.duckdb')
        g.parse(cottas_file, preserve_duplicates=True)
        g.triplestore.execute("UPDATE quads SET id=''")
        g.serialize(cottas_file)

        rmtree('.cottas_tmp', ignore_errors=True)


def create_id(cottas_file, in_memory=True):
    if in_memory:
        g = Graph()
        g.parse(cottas_file, preserve_duplicates=True)
        g.triplestore.execute("UPDATE quads SET id=CONCAT(s, ' ', p, ' ', o)")
        g.serialize(cottas_file)
    else:
        rmtree('.cottas_tmp', ignore_errors=True)
        mkdir('.cottas_tmp')

        g = Graph('.cottas_tmp/cottas.duckdb')
        g.parse(cottas_file, preserve_duplicates=True)
        g.serialize(cottas_file)

        rmtree('.cottas_tmp', ignore_errors=True)


def search(cottas_file, triple_pattern):
    return duckdb.query(translate_triple_pattern(f"{cottas_file}", triple_pattern)).df()


def cat(cottas_file_1, cottas_file_2, cottas_cat_file, in_memory=True):
    if in_memory:
        g1 = Graph()
        g1.parse(cottas_file_1, preserve_duplicates=True)

        g2 = Graph()
        g2.parse(cottas_file_2, preserve_duplicates=True)

        g1 += g2
        g1.serialize(cottas_cat_file)
    else:
        rmtree('.cottas_tmp', ignore_errors=True)
        mkdir('.cottas_tmp')

        g1 = Graph('.cottas_tmp/cottas_1.duckdb')
        g1.parse(cottas_file_1, preserve_duplicates=True)

        g2 = Graph('.cottas_tmp/cottas_2.duckdb')
        g2.parse(cottas_file_2, preserve_duplicates=True)

        g1 += g2
        g1.serialize(cottas_cat_file)

        rmtree('.cottas_tmp', ignore_errors=True)


def diff(cottas_file_1, cottas_file_2, cottas_diff_file, in_memory=True):
    if in_memory:
        g1 = Graph()
        g1.parse(cottas_file_1, preserve_duplicates=True)

        g2 = Graph()
        g2.parse(cottas_file_2, preserve_duplicates=True)

        g1 -= g2
        g1.serialize(cottas_diff_file)
    else:
        rmtree('.cottas_tmp', ignore_errors=True)
        mkdir('.cottas_tmp')

        g1 = Graph('.cottas_tmp/cottas_1.duckdb')
        g1.parse(cottas_file_1, preserve_duplicates=True)

        g2 = Graph('.cottas_tmp/cottas_2.duckdb')
        g2.parse(cottas_file_2, preserve_duplicates=True)

        g1 -= g2
        g1.serialize(cottas_diff_file)

        rmtree('.cottas_tmp', ignore_errors=True)


def info(cottas_file):
    return generate_cottas_info(cottas_file)


def verify(cottas_file):
    verify_query = f"SELECT * FROM parquet_scan('{cottas_file}') LIMIT 0"
    cottas_df = duckdb.query(verify_query).df()

    cottas_columns = list(cottas_df.columns)

    if 's' not in cottas_columns or 'p' not in cottas_columns or 'o' not in cottas_columns:
        return False

    return set(cottas_columns) <= {'s', 'p', 'o', 'g', 'id'}
