__author__ = "Julián Arenas-Guerrero"
__credits__ = ["Julián Arenas-Guerrero"]

__license__ = "Apache-2.0"
__maintainer__ = "Julián Arenas-Guerrero"
__email__ = "julian.arenas.guerrero@upm.es"


import duckdb

from os import path


def get_file_extension(file_path):
    return path.splitext(file_path)[1].lower()


def generate_cottas_info(cottas_file):
    import os
    import datetime

    kv_query = f"SELECT * FROM PARQUET_KV_METADATA('{cottas_file}') WHERE key='index'"
    row_query = f"SELECT num_rows AS triples, num_row_groups AS triples_groups FROM PARQUET_FILE_METADATA('{cottas_file}')"
    properties_query = f"SELECT COUNT(DISTINCT p) AS properties FROM PARQUET_SCAN('{cottas_file}')"
    distinct_subjects_query = f"SELECT COUNT(DISTINCT s) AS distinct_subjects FROM PARQUET_SCAN('{cottas_file}')"
    distinct_objects_query = f"SELECT COUNT(DISTINCT o) AS distinct_objects FROM PARQUET_SCAN('{cottas_file}')"
    schema_query = f"DESCRIBE SELECT * FROM PARQUET_SCAN('{cottas_file}')"
    compression_query = f"SELECT compression FROM PARQUET_METADATA('{cottas_file}')"

    (mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat(cottas_file)
    cottas_issued = datetime.datetime.fromtimestamp(ctime).isoformat()

    info_list = (
        ('index', duckdb.query(kv_query).fetchone()[2].decode()),
        ('triples', duckdb.query(row_query).fetchone()[0]),
        ('triples_groups', duckdb.query(row_query).fetchone()[1]),
        ('properties', duckdb.query(properties_query).df().iloc[0]['properties']),
        ('distinct_subjects', duckdb.query(distinct_subjects_query).df().iloc[0]['distinct_subjects']),
        ('distinct_objects', duckdb.query(distinct_objects_query).df().iloc[0]['distinct_objects']),
        ('issued', cottas_issued),
        ('size (MB)', os.path.getsize(cottas_file) / 10**6),
        ('compression', duckdb.query(compression_query).df().iloc[0]['compression']),
        ('quads', 'g' in list(duckdb.query(schema_query).df()['column_name'])),
    )

    from pandas import DataFrame
    info_df = DataFrame(info_list, columns=['parameter', 'value'])

    return info_df

def is_valid_index(index):
    index = index.lower()
    if len(index) == 3:
        if set(index) != {'s', 'p', 'o'}:
            return False
    elif len(index) == 4:
        if set(index) != {'s', 'p', 'o', 'g'}:
            return False
    else:
        return False
    return True