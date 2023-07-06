__author__ = "Julián Arenas-Guerrero"
__credits__ = ["Julián Arenas-Guerrero"]

__license__ = "Apache-2.0"
__maintainer__ = "Julián Arenas-Guerrero"
__email__ = "julian.arenas.guerrero@upm.es"


from .graph import *
from .constants import DUCKDB_MEMORY
from .triple_pattern_translator import translate_triple_pattern
from .utils import generate_cottas_info


def _remove_cottas_temp_files(db_file):
    if db_file == DUCKDB_MEMORY:
        # in-memory, not needed to remove temp files
        return

    if os.path.isfile(db_file):
        os.remove(db_file)
    if os.path.isfile(f"{db_file}.wal"):
        os.remove(f"{db_file}.wal")


def rdf_2_cottas(rdf_file, cottas_file, create_id=True, expand=False, in_memory=True):
    db_file = DUCKDB_MEMORY if in_memory else '.cottas.db'

    _remove_cottas_temp_files(db_file)

    g = Graph(db_file)
    g.parse(rdf_file, preserve_duplicates=True)
    if not create_id and not expand:
        g.remove_id()
    if expand:
        g.expand_quoted_triples()
    g.serialize(cottas_file)

    _remove_cottas_temp_files(db_file)


def cottas_2_rdf(cottas_file, rdf_file, in_memory=True):
    db_file = DUCKDB_MEMORY if in_memory else '.cottas.db'

    _remove_cottas_temp_files(db_file)

    g = Graph(db_file)
    g.parse(cottas_file, preserve_duplicates=True)
    g.serialize(rdf_file)

    _remove_cottas_temp_files(db_file)


def remove_id(cottas_file, shrink=False, in_memory=True):
    db_file = DUCKDB_MEMORY if in_memory else '.cottas.db'

    _remove_cottas_temp_files(db_file)

    g = Graph(db_file)
    g.parse(cottas_file, preserve_duplicates=True)
    if shrink:
        g.shrink_quoted_triples()
    g.remove_id()
    g.serialize(cottas_file)

    _remove_cottas_temp_files(db_file)


def create_id(cottas_file, expand=False, in_memory=True):
    db_file = DUCKDB_MEMORY if in_memory else '.cottas.db'

    _remove_cottas_temp_files(db_file)

    g = Graph(db_file)
    g.parse(cottas_file, preserve_duplicates=True)
    g.create_id()
    if expand:
        g.expand_quoted_triples()
    g.serialize(cottas_file)

    _remove_cottas_temp_files(db_file)


def search(cottas_file, triple_pattern):
    return duckdb.query(translate_triple_pattern(f"{cottas_file}", triple_pattern)).df().to_string()


def cat(cottas_file_1, cottas_file_2, cottas_cat_file, in_memory=True):
    db_file_1, db_file_2 = (DUCKDB_MEMORY, DUCKDB_MEMORY) if in_memory else ('.cottas_1.db', '.cottas_2.db')

    _remove_cottas_temp_files(db_file_1)
    _remove_cottas_temp_files(db_file_2)

    g1 = Graph(db_file_1)
    g1.parse(cottas_file_1, preserve_duplicates=True)

    g2 = Graph(db_file_2)
    g2.parse(cottas_file_2, preserve_duplicates=True)

    g1 += g2
    g1.serialize(cottas_cat_file)

    _remove_cottas_temp_files(db_file_1)
    _remove_cottas_temp_files(db_file_2)


def diff(cottas_file_1, cottas_file_2, cottas_diff_file, in_memory=True):
    db_file_1, db_file_2 = (DUCKDB_MEMORY, DUCKDB_MEMORY) if in_memory else ('.cottas_1.db', '.cottas_2.db')

    _remove_cottas_temp_files(db_file_1)
    _remove_cottas_temp_files(db_file_2)

    g1 = Graph(db_file_1)
    g1.parse(cottas_file_1, preserve_duplicates=True)

    g2 = Graph(db_file_2)
    g2.parse(cottas_file_2, preserve_duplicates=True)

    g1 -= g2
    g1.serialize(cottas_diff_file)

    _remove_cottas_temp_files(db_file_1)
    _remove_cottas_temp_files(db_file_2)


def info(cottas_file):
    return generate_cottas_info(cottas_file)


def verify(cottas_file):
    verify_query = f"SELECT * FROM parquet_scan('{cottas_file}') LIMIT 0"
    cottas_df = duckdb.query(verify_query).df()

    cottas_columns = set(cottas_df.columns)

    for pos in ['s', 'p', 'o']:
        if pos not in cottas_columns:
            return False

    return cottas_columns <= {'s', 'p', 'o', 'g', 'id'}
