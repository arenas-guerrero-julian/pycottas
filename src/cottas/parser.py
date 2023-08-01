__author__ = "Julián Arenas-Guerrero"
__credits__ = ["Julián Arenas-Guerrero"]

__license__ = "Apache-2.0"
__maintainer__ = "Julián Arenas-Guerrero"
__email__ = "julian.arenas.guerrero@upm.es"


import pyoxigraph

from os import path

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


##############################################################################
#############################   FROM HERE IT IS DEPRECATED   #################
##############################################################################


def parse_rdf_fs(graph, file_path, is_asserted=True):
    # remove temporary dir if existing beforehand
    from shutil import rmtree
    if path.isdir('.cottas.oxi'):
        rmtree('.cottas.oxi', ignore_errors=True)

    mime_type = file_ext_2_mime_type[get_file_extension(file_path=file_path)]

    oxi_store = pyoxigraph.Store('.cottas.oxi')
    oxi_store.bulk_load(file_path, mime_type=mime_type)

    quads = []
    i = 0
    for quad in oxi_store.quads_for_pattern(None, None, None, graph_name=None):
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

    # remove temporary dir
    del oxi_store
    if path.isdir('.cottas.oxi'):
        rmtree('.cottas.oxi', ignore_errors=True)

    return graph.triplestore


def _line_has_quad(line):
    line = line.strip()

    if line.startswith('#'):
        # it is a comment
        return False
    elif line == '':
        # empty
        return False
    return True


def _quad_from_line(line):
    quad = []

    line = line.strip()
    line = line[:-1]  # remove final dot

    # SUBJECT
    if line.startswith('<'):
        r = line.split('>', 1)
        quad.append(f'{r[0]}>')
        line = r[1]
    elif line.startswith('_:'):
        r = line.split(' ', 1)
        quad.append(r[0])
        line = r[1]

    # PREDICATE
    line = line.strip()
    r = line.split('>', 1)
    quad.append(f'{r[0]}>')
    line = r[1]

    # OBJECT and NAMED GRAPH
    line = line.strip()

    is_quad = False     # check if it is a triple or a quad
    if line.endswith('>'):
        if line.startswith('<') and ' ' in line:
            is_quad = True
        elif line.startswith('"') and not line.split('<')[-2].endswith('"^^'):
            is_quad = True
        elif line.startswith('_:'):
            is_quad = True

    if is_quad:
        splitted_line = line.split('<')
        quad.append('<'.join(splitted_line[:-1]).strip())   # object
        quad.append(f'<{splitted_line[-1]}')                # quad
    else:
        quad.append(line)   # object
        quad.append('')     # quad

    quad.append(f'{quad[0]} {quad[1]} {quad[2]}')   # id
    quad.append(True)                               # is_asserted

    return quad


def parse_nquads(graph, filepath):
    file = open(filepath)

    while 1:
        lines = file.readlines(100000)
        if not lines:
            break

        quads = [_quad_from_line(line) for line in lines if _line_has_quad(line)]
        graph.bulk_add(quads, hash_id=True)

    file.close()

    return graph.triplestore
