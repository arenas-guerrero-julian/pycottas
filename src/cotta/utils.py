__author__ = "Julián Arenas-Guerrero"
__credits__ = ["Julián Arenas-Guerrero"]

__license__ = "Apache-2.0"
__maintainer__ = "Julián Arenas-Guerrero"
__email__ = "julian.arenas.guerrero@upm.es"


import duckdb

from .constants import *
from .term import *


def translate_triple_pattern(table_name, triple_pattern):
    triple_pattern = triple_pattern.split()

    if len(triple_pattern) != 3 and len(triple_pattern) != 4:
        print('The provided triple pattern is not correct.')
        return None

    s = triple_pattern[0]
    p = triple_pattern[1]
    o = triple_pattern[2]

    if len(triple_pattern) == 4:
        g = triple_pattern[3]
    else:
        g = None

    triple_pattern_query = 'SELECT '
    if s == '?':
        triple_pattern_query += 's, '
    if p == '?':
        triple_pattern_query += 'p, '
    if o == '?':
        triple_pattern_query += 'o, '
    if g == '?':
        triple_pattern_query += 'g, '

    triple_pattern_query = f"{triple_pattern_query[:-2]} FROM parquet_scan('{table_name}')"

    if s != '?' or p != '?' or o != '?' or (g and g != '?'):
        triple_pattern_query += " WHERE"
        if s != '?':
            triple_pattern_query = f"{triple_pattern_query} AND s='{s}' "
        if p != '?':
            triple_pattern_query = f"{triple_pattern_query} AND p='{p}' "
        if o != '?':
            triple_pattern_query = f"{triple_pattern_query} AND o='{o}' "
        if g and g != '?':
            triple_pattern_query = f"{triple_pattern_query} AND g='{g}' "

    triple_pattern_query = triple_pattern_query.replace('WHERE AND', 'WHERE')

    return triple_pattern_query


def cotta_info(cotta_file):
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
    info += f"{iri(cotta_path)} {iri('http://rdfs.org/ns/void#properties')} {literal(properties, datatype=XSD_INTEGER)} .\n"
    info += f"{iri(cotta_path)} {iri('http://rdfs.org/ns/void#distinctSubjects')} {literal(distinct_subjects, datatype=XSD_INTEGER)} .\n"
    info += f"{iri(cotta_path)} {iri('http://rdfs.org/ns/void#distinctObjects')} {literal(distinct_objects, datatype=XSD_INTEGER)} .\n"

    info += f'{iri(cotta_path)} {iri("http://purl.org/COTTA/cotta#publicationInformation")} "_:publicationInformation" .\n'
    info += f'"_:publicationInformation" {iri("http://purl.org/dc/terms/issued")} {literal(cotta_issued, datatype=XSD_DATETIME)} .\n'

    info += f'{iri(cotta_path)} {iri("http://purl.org/COTTA/cotta#statisticalInformation")} "_:statistics" .\n'
    info += f'"_:statistics" {iri("http://purl.org/COTTA/cotta#cottaSize")} {literal(cotta_size, datatype=XSD_INTEGER)} .'

    return info
