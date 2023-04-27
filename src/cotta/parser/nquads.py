__author__ = "Julián Arenas-Guerrero"
__credits__ = ["Julián Arenas-Guerrero"]

__license__ = "Apache-2.0"
__maintainer__ = "Julián Arenas-Guerrero"
__email__ = "julian.arenas.guerrero@upm.es"


def _line_has_quad(line):
    line = line.strip()

    if line.startswith('#'):
        # it is a comment
        return False
    elif line == '':
        # empty
        return False
    return True


def _quad_from_line(line, file_extension):
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

    if file_extension == '.nt':
        quad.append(line)   # object
        quad.append('')     # quad
        return quad

    is_quad = False     # file_extension == '.nq' check if it is a triple or a quad
    if line.endswith('>'):
        if line.startswith('<') and ' ' in line:
            is_quad = True
        elif line.startswith('"') and not line.split('<')[-2].endswith('"^^'):
            is_quad = True
        elif line.startswith('_:'):
            is_quad = True

    if is_quad:
        splitted_line = line.split('<')
        quad.append('<'.join(splitted_line[:1]).strip())    # object
        quad.append(f'<{splitted_line[-1]}')                # quad
    else:
        quad.append(line)   # object
        quad.append('')     # quad

    return quad


def parse_nquads(graph, filepath, file_extension):
    file = open(filepath)

    while 1:
        lines = file.readlines(100000000)
        if not lines:
            break

        quads = [_quad_from_line(line, file_extension) for line in lines if _line_has_quad(line)]
        graph.bulk_add(quads)

    file.close()

    return graph.triplestore
