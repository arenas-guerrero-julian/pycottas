__author__ = "Julián Arenas-Guerrero"
__credits__ = ["Julián Arenas-Guerrero"]

__license__ = "Apache-2.0"
__maintainer__ = "Julián Arenas-Guerrero"
__email__ = "julian.arenas.guerrero@upm.es"


import duckdb
import pyoxigraph
import os

from .constants import file_ext_2_mime_type
from .tp_translator import translate_triple_pattern
from .utils import generate_cottas_info, get_file_extension, is_valid_index, verify_cottas_file
from .cottas_store import COTTASStore
from .cottas_document import COTTASDocument


def rdf2cottas(rdf_file_path, cottas_file_path, index='spo'):
    if index and not is_valid_index(index):
        print(f"Index `{index}` is not valid.")
        return

    mime_type = file_ext_2_mime_type[get_file_extension(file_path=rdf_file_path)]
    quad_found = False

    create_query = """
                CREATE TABLE quads (s VARCHAR NOT NULL, p VARCHAR NOT NULL, o VARCHAR NOT NULL, g VARCHAR)
            """
    triplestore = duckdb.connect()
    triplestore.execute(create_query)

    quads = []
    i = 0
    for quad in pyoxigraph.parse(rdf_file_path, base_iri=None, mime_type=mime_type):
        quad = [str(term) for term in quad]

        if len(quad) == 3:
            # for empty quad
            quad.append(None)
        else:
            quad_found = True
        quads.append(quad)

        if i == 1000000:
            # bulk add quads
            insert_query = "SET preserve_insertion_order = false; INSERT INTO quads VALUES (?, ?, ?, ?)"
            triplestore.executemany(insert_query, quads)

            # reset quads
            quads = []
            i = 0
        else:
            i += 1

    # bulk add quads
    insert_query = "SET preserve_insertion_order = false; INSERT INTO quads VALUES (?, ?, ?, ?)"
    triplestore.executemany(insert_query, quads)

    # export the triple table
    if quad_found:
        export_query = f"COPY (SELECT DISTINCT s, p, o, g FROM quads"
    else:
        export_query = f"COPY (SELECT DISTINCT s, p, o FROM quads"
    if index:
        export_query += " ORDER BY "
        for p in index:
            export_query += f"{p}, "
        export_query = export_query[:-2]
    export_query += f") TO '{cottas_file_path}' (FORMAT PARQUET, COMPRESSION ZSTD, COMPRESSION_LEVEL 22, PARQUET_VERSION v2, KV_METADATA {{index: '{index.lower()}'}})"
    triplestore.execute(export_query)


def cottas2rdf(cottas_file_path, rdf_file_path):
    f = open(rdf_file_path, 'w')

    has_named_graph = 'g' in list(duckdb.query(f"SELECT name FROM PARQUET_SCHEMA('{cottas_file_path}')").df()['name'])
    cur = duckdb.execute(f"SELECT s, p, o{', g' if has_named_graph else ''} FROM PARQUET_SCAN('{cottas_file_path}')")
    cur_chunk_df = cur.fetch_df_chunk()
    while len(cur_chunk_df):
        quads = cur_chunk_df.values.tolist()
        for quad in quads:
            if has_named_graph:
                # in case of named graph
                quad = f"{quad[0]} {quad[1]} {quad[2]} {quad[3]}"
            else:
                quad = f"{quad[0]} {quad[1]} {quad[2]}"
            f.write(f'{quad} .\n')

        cur_chunk_df = cur.fetch_df_chunk()
    f.close()


def search(cottas_file_path, triple_pattern):
    return duckdb.query(translate_triple_pattern(f"{cottas_file_path}", triple_pattern))


def cat(cottas_file_paths, cottas_cat_file_path, index='spo', remove_input_files=False):
    if index and not is_valid_index(index):
        print(f"Index `{index}` is not valid.")
        return

    cat_query = f"COPY (SELECT DISTINCT s, p, o FROM PARQUET_SCAN({cottas_file_paths}, union_by_name = true)"
    if index:
        cat_query += " ORDER BY "
        for p in index:
            cat_query += f"{p}, "
        cat_query = cat_query[:-2]
    cat_query += f") TO '{cottas_cat_file_path}' (FORMAT PARQUET, COMPRESSION ZSTD, COMPRESSION_LEVEL 22, PARQUET_VERSION v2, KV_METADATA {{index: '{index.lower()}'}})"
    duckdb.execute(cat_query)

    if remove_input_files:
        for file in cottas_file_paths:
            os.remove(file)


def diff(cottas_file_1_path, cottas_file_2_path, cottas_diff_file_path, index='spo', remove_input_files=False):
    if index and not is_valid_index(index):
        print(f"Index `{index}` is not valid.")
        return

    diff_query = f"COPY (SELECT * FROM (SELECT DISTINCT * FROM PARQUET_SCAN('{cottas_file_1_path}') EXCEPT SELECT * FROM PARQUET_SCAN('{cottas_file_2_path}'))"
    if index:
        diff_query += " ORDER BY "
        for p in index:
            diff_query += f"{p}, "
        diff_query = diff_query[:-2]
    diff_query += f") TO '{cottas_diff_file_path}' (FORMAT PARQUET, COMPRESSION ZSTD, COMPRESSION_LEVEL 22, PARQUET_VERSION v2, KV_METADATA {{index: '{index.lower()}'}})"
    duckdb.execute(diff_query)

    if remove_input_files:
        os.remove(cottas_file_1_path)
        os.remove(cottas_file_2_path)


def info(cottas_file):
    return generate_cottas_info(cottas_file)


def verify(cottas_file):
    return verify_cottas_file(cottas_file)
