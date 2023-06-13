__author__ = "Julián Arenas-Guerrero"
__credits__ = ["Julián Arenas-Guerrero"]

__license__ = "Apache-2.0"
__maintainer__ = "Julián Arenas-Guerrero"
__email__ = "julian.arenas.guerrero@upm.es"


import duckdb

from random import randint

from .constants import *
from .term import *


def _build_star_query(triple_pattern, query, cotta_file):
    s_query, o_query = '', ''

    if type(triple_pattern[0]) is list:
        s_query = _build_star_query(triple_pattern[0], query, cotta_file)
    if type(triple_pattern[2]) is list:
        o_query = _build_star_query(triple_pattern[2], query, cotta_file)

    query = f"SELECT "
    if type(triple_pattern[0]) is str and triple_pattern[0].startswith('?'):
        query += f"s AS {triple_pattern[0][1:]}, "
    elif type(triple_pattern[0]) is list:
        query += "s, "
    if type(triple_pattern[1]) is str and triple_pattern[1].startswith('?'):
        query += f"p AS {triple_pattern[1][1:]}, "
    elif type(triple_pattern[1]) is list:
        query += "p, "
    if type(triple_pattern[2]) is str and triple_pattern[2].startswith('?'):
        query += f"o AS {triple_pattern[2][1:]}, "
    elif type(triple_pattern[2]) is list:
        query += "o, "
    if type(triple_pattern[0]) is list or type(triple_pattern[1]) is list or type(triple_pattern[2]) is list:
        query = query[:-2]
    else:
        query += 'id'
    query += f" FROM read_parquet('{cotta_file}') WHERE "

    if type(triple_pattern[0]) is str and not triple_pattern[0].startswith('?'):
        query += f"s='{triple_pattern[0]}' AND "
    if type(triple_pattern[1]) is str and not triple_pattern[1].startswith('?'):
        query += f"p='{triple_pattern[1]}' AND "
    if type(triple_pattern[2]) is str and not triple_pattern[2].startswith('?'):
        query += f"o='{triple_pattern[2]}' AND "

    # remove last "AND "
    if query.endswith(' AND '):
        query = query[:-5]

    if s_query:
        v1, v2 = f"v{randint(0, 100000)}", f"v{randint(0, 100000)}"
        query = f"SELECT *\nFROM ( ( ( {s_query} ) AS {v1}\nINNER JOIN\n( {query} ) AS {v2} ON {v1}.id={v2}.s ) )"
    if o_query:
        v1, v2 = f"v{randint(0, 100000)}", f"v{randint(0, 100000)}"
        query = f"SELECT *\nFROM ( ( ( {o_query} ) AS {v1}\nINNER JOIN\n( {query} ) AS {v2} ON {v1}.id={v2}.o ) )"

    return query


def translate_triple_pattern(cotta_file, triple_pattern_str):
    projection_str = triple_pattern_str
    projection_str = projection_str.replace("<<", '').replace(">>", '')
    projection_list = [term[1:] for term in projection_str.split() if term.startswith('?')]

    triple_pattern_str = ' '.join("'{}'".format(word) for word in triple_pattern_str.split())

    triple_pattern_str = triple_pattern_str.replace("'<<' ", '[').replace(" '>>'", ']')
    triple_pattern_str = triple_pattern_str.replace(' ', ',')
    triple_pattern_str = '[' + triple_pattern_str + ']'

    triple_pattern = eval(triple_pattern_str)

    if type(triple_pattern[0]) is list or type(triple_pattern[2]) is list:
        triple_pattern_query = "SELECT "
        for var in projection_list:
            triple_pattern_query += f"{var}, "
        triple_pattern_query = f"{triple_pattern_query[:-2]}\nFROM ( {_build_star_query(triple_pattern, '', cotta_file)} )"
    else:
        triple_pattern_query = f"SELECT "
        if triple_pattern[0].startswith('?'):
            triple_pattern_query += f"s AS {triple_pattern[0][1:]}, "
        if triple_pattern[1].startswith('?'):
            triple_pattern_query += f"p AS {triple_pattern[1][1:]}, "
        if triple_pattern[2].startswith('?'):
            triple_pattern_query += f"o AS {triple_pattern[2][1:]}, "

        triple_pattern_query = f"{triple_pattern_query[:-2]}\nFROM read_parquet('{cotta_file}')\nWHERE "

        if not triple_pattern[0].startswith('?'):
            triple_pattern_query += f"s='{triple_pattern[0]}' AND "
        if not triple_pattern[1].startswith('?'):
            triple_pattern_query += f"p='{triple_pattern[1]}' AND "
        if not triple_pattern[2].startswith('?'):
            triple_pattern_query += f"o='{triple_pattern[2]}' AND "
        triple_pattern_query = triple_pattern_query[:-5]
        print(triple_pattern_query)

    return triple_pattern_query


def generate_cotta_info(cotta_file):
    import os
    import datetime

    triples_query = f"SELECT COUNT(*) AS triples FROM parquet_scan('{cotta_file}')"
    properties_query = f"SELECT COUNT(DISTINCT p) AS properties FROM parquet_scan('{cotta_file}')"
    distinct_subjects_query = f"SELECT COUNT(DISTINCT s) AS distinct_subjects FROM parquet_scan('{cotta_file}')"
    distinct_objects_query = f"SELECT COUNT(DISTINCT o) AS distinct_objects FROM parquet_scan('{cotta_file}')"

    cotta_path = f"file://{os.path.join(os.getcwd(), cotta_file)}"
    cotta_size = os.path.getsize(cotta_file)

    (mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat(cotta_file)
    cotta_issued = datetime.datetime.fromtimestamp(ctime).isoformat()

    triples = duckdb.query(triples_query).df().iloc[0]['triples']
    properties = duckdb.query(properties_query).df().iloc[0]['properties']
    distinct_subjects = duckdb.query(distinct_subjects_query).df().iloc[0]['distinct_subjects']
    distinct_objects = duckdb.query(distinct_objects_query).df().iloc[0]['distinct_objects']

    info = ''
    info += f"{iri(cotta_path)} {iri(RDF_TYPE)} {iri('http://purl.org/COTTA/cotta#Dataset')} .\n"
    info += f"{iri(cotta_path)} {iri(RDF_TYPE)} {iri('http://rdfs.org/ns/void#Dataset')} .\n"
    info += f"{iri(cotta_path)} {iri('http://rdfs.org/ns/void#triples')} {literal(triples, datatype=XSD_INTEGER)} .\n"
    info += f"{iri(cotta_path)} {iri('http://rdfs.org/ns/void#properties')} " \
            f"{literal(properties, datatype=XSD_INTEGER)} .\n"
    info += f"{iri(cotta_path)} {iri('http://rdfs.org/ns/void#distinctSubjects')} " \
            f"{literal(distinct_subjects, datatype=XSD_INTEGER)} .\n"
    info += f"{iri(cotta_path)} {iri('http://rdfs.org/ns/void#distinctObjects')} " \
            f"{literal(distinct_objects, datatype=XSD_INTEGER)} .\n"

    info += f'{iri(cotta_path)} {iri("http://purl.org/COTTA/cotta#publicationInformation")} ' \
            f'"_:publicationInformation" .\n'
    info += f'"_:publicationInformation" {iri("http://purl.org/dc/terms/issued")} ' \
            f'{literal(cotta_issued, datatype=XSD_DATETIME)} .\n'

    info += f'{iri(cotta_path)} {iri("http://purl.org/COTTA/cotta#statisticalInformation")} "_:statistics" .\n'
    info += f'"_:statistics" {iri("http://purl.org/COTTA/cotta#cottaSize")} ' \
            f'{literal(cotta_size, datatype=XSD_INTEGER)} .'

    return info
