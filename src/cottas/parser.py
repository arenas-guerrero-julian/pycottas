__author__ = "Julián Arenas-Guerrero"
__credits__ = ["Julián Arenas-Guerrero"]

__license__ = "Apache-2.0"
__maintainer__ = "Julián Arenas-Guerrero"
__email__ = "julian.arenas.guerrero@upm.es"


import pyoxigraph

from .utils import get_file_extension
from .constants import file_ext_2_mime_type


def parse_cottas(graph, filepath):
    if graph.preserve_duplicates:
        graph.triplestore.execute(f"INSERT INTO quads (SELECT * FROM PARQUET_SCAN('{filepath}'))")
    else:
        graph.triplestore.execute(f"INSERT OR IGNORE INTO quads (SELECT DISTINCT * FROM PARQUET_SCAN('{filepath}'))")

    return graph.triplestore


def parse_rdf(graph, file_path, is_asserted=True, mime_type=None):
    if not mime_type:
        mime_type = file_ext_2_mime_type[get_file_extension(file_path=file_path)]

    quads = []
    i = 0
    for quad in pyoxigraph.parse(file_path, base_iri=None, mime_type=mime_type):
        quad = [str(term) for term in quad]

        if len(quad) == 3:
            # for empty quad
            quad.append('')

        if ' <' in quad[0]:
            quad[0] = f'<<{quad[0]}>>'
        if not quad[2].startswith('"') and ' <' in quad[2]:
            quad[2] = f'<<{quad[2]}>>'
        quad.append(f'<<{quad[0]} {quad[1]} {quad[2]}>>')
        quad.append(is_asserted)

        quads.append(quad)

        if i == 1000000:
            graph.bulk_add(quads, hash_id=True)
            quads = []
            i = 0
        else:
            i += 1

    graph.bulk_add(quads, hash_id=True)

    return graph.triplestore
