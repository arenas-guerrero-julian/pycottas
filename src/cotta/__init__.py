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


def rdf_2_cotta(rdf_file, cotta_file, in_memory=True):
    if in_memory:
        g = Graph()
        g.parse(rdf_file, preserve_duplicates=False)
        g.serialize(cotta_file)
    else:
        rmtree('.cotta_temp', ignore_errors=True)
        mkdir('.cotta_temp')

        g = Graph('.cotta_temp/cotta.duckdb')
        g.parse(rdf_file, preserve_duplicates=True)
        g.serialize(cotta_file)

        rmtree('.cotta_temp', ignore_errors=True)


def cotta_2_rdf(cotta_file, rdf_file, in_memory=True):
    if in_memory:
        g = Graph()
        g.parse(cotta_file, preserve_duplicates=False)
        g.serialize(rdf_file)
    else:
        rmtree('.cotta_temp', ignore_errors=True)
        mkdir('.cotta_temp')

        g = Graph('.cotta_temp/cotta.duckdb')
        g.parse(cotta_file, preserve_duplicates=True)
        g.serialize(rdf_file)

        rmtree('.cotta_temp', ignore_errors=True)


def cotta_remove_id(cotta_file, in_memory=True):
    if in_memory:
        g = Graph()
        g.parse(cotta_file, preserve_duplicates=False)
        g.triplestore.execute("UPDATE quads SET id=''")
        g.serialize(cotta_file)
    else:
        rmtree('.cotta_temp', ignore_errors=True)
        mkdir('.cotta_temp')

        g = Graph('.cotta_temp/cotta.duckdb')
        g.parse(cotta_file, preserve_duplicates=True)
        g.serialize(cotta_file)

        rmtree('.cotta_temp', ignore_errors=True)


def cotta_search(cotta_file, triple_pattern, results_file=None):
    results_df = duckdb.query(translate_triple_pattern(f"{cotta_file}", triple_pattern)).df()

    if results_file:
        results_df.to_csv(results_file, index=False, sep='\t')
    else:
        return results_df


def cotta_cat(cotta_file_1, cotta_file_2, cotta_cat_file, in_memory=True):
    if in_memory:
        g1 = Graph()
        g1.parse(cotta_file_1, preserve_duplicates=False)

        g2 = Graph()
        g2.parse(cotta_file_2, preserve_duplicates=False)

        g1 += g2
        g1.serialize(cotta_cat_file)
    else:
        rmtree('.cotta_temp', ignore_errors=True)
        mkdir('.cotta_temp')

        g1 = Graph('.cotta_temp/cotta_1.duckdb')
        g1.parse(cotta_file_1, preserve_duplicates=True)

        g2 = Graph('.cotta_temp/cotta_2.duckdb')
        g2.parse(cotta_file_2, preserve_duplicates=True)

        g1 += g2
        g1.serialize(cotta_cat_file)

        rmtree('.cotta_temp', ignore_errors=True)


def cotta_diff(cotta_file_1, cotta_file_2, cotta_diff_file, in_memory=True):
    if in_memory:
        g1 = Graph()
        g1.parse(cotta_file_1, preserve_duplicates=False)

        g2 = Graph()
        g2.parse(cotta_file_2, preserve_duplicates=False)

        g1 -= g2
        g1.serialize(cotta_diff_file)
    else:
        rmtree('.cotta_temp', ignore_errors=True)
        mkdir('.cotta_temp')

        g1 = Graph('.cotta_temp/cotta_1.duckdb')
        g1.parse(cotta_file_1, preserve_duplicates=True)

        g2 = Graph('.cotta_temp/cotta_2.duckdb')
        g2.parse(cotta_file_2, preserve_duplicates=True)

        g1 -= g2
        g1.serialize(cotta_diff_file)

        rmtree('.cotta_temp', ignore_errors=True)


def cotta_info(cotta_file):
    return generate_cotta_info(cotta_file)


def cotta_verify(cotta_file):
    verify_query = f"SELECT * FROM parquet_scan('{cotta_file}') LIMIT 0"
    cotta_df = duckdb.query(verify_query).df()

    cotta_columns = [c.lower() for c in cotta_df.columns]

    if 's' not in cotta_columns or 'p' not in cotta_columns or 'o' not in cotta_columns:
        return False

    return set(cotta_columns) <= {'s', 'p', 'o', 'g', 'id'}
