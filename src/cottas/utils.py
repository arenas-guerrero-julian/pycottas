__author__ = "Julián Arenas-Guerrero"
__credits__ = ["Julián Arenas-Guerrero"]

__license__ = "Apache-2.0"
__maintainer__ = "Julián Arenas-Guerrero"
__email__ = "julian.arenas.guerrero@upm.es"


import duckdb

from os import path

from .constants import *
from .term import *


def get_file_extension(file_path):
    return path.splitext(file_path)[1].lower()


def is_id_computed(cottas_file):
    is_id_computed_query = f"SELECT id FROM READ_PARQUET('{cottas_file}') LIMIT 1"

    return duckdb.query(is_id_computed_query).df().iloc[0]['id'] == ''


def generate_cottas_info(cottas_file):
    import os
    import datetime

    triples_query = f"SELECT COUNT(*) AS triples FROM PARQUET_SCAN('{cottas_file}')"
    properties_query = f"SELECT COUNT(DISTINCT p) AS properties FROM PARQUET_SCAN('{cottas_file}')"
    distinct_subjects_query = f"SELECT COUNT(DISTINCT s) AS distinct_subjects FROM PARQUET_SCAN('{cottas_file}')"
    distinct_objects_query = f"SELECT COUNT(DISTINCT o) AS distinct_objects FROM PARQUET_SCAN('{cottas_file}')"
    schema_query = f"DESCRIBE SELECT * FROM READ_PARQUET('{cottas_file}');"
    compression_query = f"SELECT compression FROM PARQUET_METADATA('{cottas_file}')"

    cottas_path = f"file://{os.path.join(os.getcwd(), cottas_file)}"
    cottas_size = os.path.getsize(cottas_file)

    (mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat(cottas_file)
    cottas_issued = datetime.datetime.fromtimestamp(ctime).isoformat()

    triples = duckdb.query(triples_query).df().iloc[0]['triples']
    properties = duckdb.query(properties_query).df().iloc[0]['properties']
    distinct_subjects = duckdb.query(distinct_subjects_query).df().iloc[0]['distinct_subjects']
    distinct_objects = duckdb.query(distinct_objects_query).df().iloc[0]['distinct_objects']
    schema = str(list(duckdb.query(schema_query).df()['column_name'])).replace("'", "")[1:-1]
    compression = duckdb.query(compression_query).df().iloc[0]['compression']

    info = ''
    info += f"{iri(cottas_path)} {iri(RDF_TYPE)} {iri('http://purl.org/COTTAS/cottas#Dataset')} .\n"
    info += f"{iri(cottas_path)} {iri(RDF_TYPE)} {iri('http://rdfs.org/ns/void#Dataset')} .\n"
    info += f"{iri(cottas_path)} {iri('http://rdfs.org/ns/void#triples')} {literal(triples, datatype=XSD_INTEGER)} .\n"
    info += f"{iri(cottas_path)} {iri('http://rdfs.org/ns/void#properties')} " \
            f"{literal(properties, datatype=XSD_INTEGER)} .\n"
    info += f"{iri(cottas_path)} {iri('http://rdfs.org/ns/void#distinctSubjects')} " \
            f"{literal(distinct_subjects, datatype=XSD_INTEGER)} .\n"
    info += f"{iri(cottas_path)} {iri('http://rdfs.org/ns/void#distinctObjects')} " \
            f"{literal(distinct_objects, datatype=XSD_INTEGER)} .\n"

    info += f'{iri(cottas_path)} {iri("http://purl.org/COTTAS/cottas#publicationInformation")} ' \
            f'"_:publicationInformation" .\n'
    info += f'"_:publicationInformation" {iri("http://purl.org/dc/terms/issued")} ' \
            f'{literal(cottas_issued, datatype=XSD_DATETIME)} .\n'

    info += f'{iri(cottas_path)} {iri("http://purl.org/COTTAS/cottas#statisticalInformation")} "_:statistics" .\n'
    info += f'"_:statistics" {iri("http://purl.org/COTTAS/cottas#cottasSize")} ' \
            f'{literal(cottas_size, datatype=XSD_INTEGER)} .\n'

    info += f'{iri(cottas_path)} {iri("github.com/arenas-guerrero-julian/cottas#compression")} "{compression}" .\n'
    info += f'{iri(cottas_path)} {iri("github.com/arenas-guerrero-julian/cottas#schema")} "{schema}" .\n'

    info += f'{iri(cottas_path)} {iri("github.com/arenas-guerrero-julian/cottas#isIdComputed")} '
    if is_id_computed(cottas_file):
        info += f'"false"^^<http://www.w3.org/2001/XMLSchema#boolean> .\n'
    else:
        info += f'"true"^^<http://www.w3.org/2001/XMLSchema#boolean> .\n'

    return info
