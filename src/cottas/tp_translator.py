# dict mapping RDF term positions to attribute names
i_pos = {
    0: 's',
    1: 'p',
    2: 'o',
    3: 'g'
}


def _get_projected_vars(tp):
    """
    :param tp: a triple pattern
    :return: a list with the names of the variables in the triple pattern
    """

    projected_vars = []

    for i in range(len(tp)):
        if tp[i].startswith('?'):
            projected_vars.append(tp[i][1:])

    return list(set(projected_vars))


def _parse_tp(tp_str):
    # enclose with quotes each substring, e.g., ?s: '?s', "24": '"24"'
    tp_str = ' '.join("'{}'".format(sub_str) for sub_str in tp_str.split())

    # the separators in Python lists are not whitespaces but commas
    tp_str = tp_str.replace(' ', ',')
    tp_str = f"[{tp_str}]"

    # evaluate the string representation to nested lists
    tp = eval(tp_str)
    return tp


def translate_triple_pattern(cottas_file, tp_str):
    """
    Given a COTTAS file and a user-defined triple pattern, translate the triple pattern to an SQL over COTTAS.

    :param cottas_file: path to a COTTAS file
    :param tp_str: a user-defined triple pattern
    :return: SQL query for the triple pattern
    """

    tp = _parse_tp(tp_str)
    projected_vars = _get_projected_vars(tp)

    tp_query = "SELECT "
    for var in projected_vars:
        tp_query += f"{var}, "
    tp_query = f"{tp_query[:-2]}\nFROM PARQUET_SCAN('{cottas_file}') WHERE "

    # build selection iterating over all positions in the triple pattern
    for i in range(4):
        # skip named graph if not in the triple pattern
        if i < len(tp):
            if not tp[i].startswith('?'):
                tp_query += f"{i_pos[i]}='{tp[i]}' AND "

    # remove final `AND ` and `WHERE `
    if tp_query.endswith('AND '):
        tp_query = tp_query[:-4]
    if tp_query.endswith('WHERE '):
        tp_query = tp_query[:-6]

    return tp_query