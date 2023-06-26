__author__ = "Julián Arenas-Guerrero"
__credits__ = ["Julián Arenas-Guerrero"]

__license__ = "Apache-2.0"
__maintainer__ = "Julián Arenas-Guerrero"
__email__ = "julian.arenas.guerrero@upm.es"


import lightrdf

from random import randint


def parse_cottas(graph, filepath):
    temporal_table = f'temporal_quads_{randint(0, 10000000000)}'
    graph.triplestore.execute(f"CREATE TABLE {temporal_table} AS SELECT * FROM parquet_scan('{filepath}')")

    if len(graph.triplestore.execute(f"DESCRIBE {temporal_table}").fetchall()) == 3:
        # add empty named graphs column
        graph.triplestore.execute(f"ALTER TABLE {temporal_table} ADD COLUMN g TEXT DEFAULT ''")

    graph.triplestore.execute(f'INSERT INTO quads (SELECT * FROM {temporal_table})')
    graph.triplestore.execute(f'DROP TABLE {temporal_table}')

    return graph.triplestore


def parse_rdf(graph, filepath, preserve_duplicates):
    parser = lightrdf.Parser()

    triples = []
    i = 0
    for triple in parser.parse(filepath, base_iri=None):
        triple = list(triple)

        triple.append('')   # for empty quad
        triple.append(f'{triple[0]} {triple[1]} {triple[2]}')
        triples.append(triple)

        if i == 100000000:
            graph.bulk_add(triples, preserve_duplicates)
            triples = []
            i = 0
        else:
            i += 1
    graph.bulk_add(triples, preserve_duplicates)

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
        quad.append('<'.join(splitted_line[:-1]).strip())    # object
        quad.append(f'<{splitted_line[-1]}')                # quad
    else:
        quad.append(line)   # object
        quad.append('')     # quad

    quad.append('')

    return quad


def parse_nquads(graph, filepath, preserve_duplicates):
    file = open(filepath)

    while 1:
        lines = file.readlines(100000000)
        if not lines:
            break

        quads = [_quad_from_line(line) for line in lines if _line_has_quad(line)]
        graph.bulk_add(quads, preserve_duplicates)

    file.close()

    return graph.triplestore
