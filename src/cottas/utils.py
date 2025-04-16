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

    properties_query = f"SELECT COUNT(DISTINCT p) AS properties FROM PARQUET_SCAN('{cottas_file}')"
    distinct_subjects_query = f"SELECT COUNT(DISTINCT s) AS distinct_subjects FROM PARQUET_SCAN('{cottas_file}')"
    distinct_objects_query = f"SELECT COUNT(DISTINCT o) AS distinct_objects FROM PARQUET_SCAN('{cottas_file}')"
    schema_query = f"DESCRIBE SELECT * FROM PARQUET_SCAN('{cottas_file}')"
    compression_query = f"SELECT compression FROM PARQUET_METADATA('{cottas_file}')"

    (mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat(cottas_file)
    cottas_issued = datetime.datetime.fromtimestamp(ctime).isoformat()

    info_list = (
        ('properties', duckdb.query(properties_query).df().iloc[0]['properties']),
        ('distinct_subjects', duckdb.query(distinct_subjects_query).df().iloc[0]['distinct_subjects']),
        ('distinct_objects', duckdb.query(distinct_objects_query).df().iloc[0]['distinct_objects']),
        ('issued', cottas_issued),
        ('size (MB)', os.path.getsize(cottas_file) / 10**6),
        ('compression', duckdb.query(compression_query).df().iloc[0]['compression']),
        ('schema', str(list(duckdb.query(schema_query).df()['column_name'])).replace("'", "")[1:-1]),
    )

    from pandas import DataFrame
    info_df = DataFrame(info_list, columns=['parameter', 'value'])

    return info_df
