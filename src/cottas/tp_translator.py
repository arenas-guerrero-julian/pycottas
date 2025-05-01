__author__ = "Julián Arenas-Guerrero"
__credits__ = ["Julián Arenas-Guerrero"]

__license__ = "Apache-2.0"
__maintainer__ = "Julián Arenas-Guerrero"
__email__ = "julian.arenas.guerrero@upm.es"


from rdflib.util import from_n3


# dict mapping RDF term positions to attribute names
i_pos = {
    0: 's',
    1: 'p',
    2: 'o',
    3: 'g'
}


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
    Given a COTTAS file and a user-defined triple pattern, translate the triple pattern to an SQL query over COTTAS.

    :param cottas_file: path to a COTTAS file
    :param tp_str: a user-defined triple pattern
    :return: SQL query for the triple pattern
    """

    tp = _parse_tp(tp_str)

    tp_query = "SELECT "
    for i in range(len(tp)):
        if tp[i].startswith('?'):
            tp_query += f"{i_pos[i]} AS {tp[i][1:]}, "
    tp_query = f"{tp_query[:-2]}\nFROM PARQUET_SCAN('{cottas_file}') WHERE "

    # build selection iterating over all positions in the triple pattern
    for i in range(4):
        # skip named graph if not in the triple pattern
        if i < len(tp):
            if not tp[i].startswith('?'):
                # scape 'quotes'
                tp[i] = tp[i].replace("'", "''")
                tp_query += f"{i_pos[i]}='{tp[i]}' AND "

    # remove final `AND ` and `WHERE `
    if tp_query.endswith('AND '):
        tp_query = tp_query[:-4]
    if tp_query.endswith('WHERE '):
        tp_query = tp_query[:-6]

    return tp_query


def translate_triple_pattern_tuple(cottas_file, tp_tuple):
    """
    Given a COTTAS file and an RDFlib triple pattern tuple, translate the triple pattern to an SQL query over COTTAS.

    :param cottas_file: path to a COTTAS file
    :param tp_str: a user-defined triple pattern
    :return: SQL query for the triple pattern
    """

    tp_query = f"SELECT s, p, o FROM PARQUET_SCAN('{cottas_file}') WHERE "

    # build selection iterating over all positions in the triple pattern
    for i in range(4):
        # skip named graph if not in the triple pattern
        if i < len(tp_tuple):
            if not tp_tuple[i] is None:
                tp_query += f"{i_pos[i]}='{tp_tuple[i].n3()}' AND "

    # remove final `AND ` and `WHERE `
    if tp_query.endswith('AND '):
        tp_query = tp_query[:-4]
    if tp_query.endswith('WHERE '):
        tp_query = tp_query[:-6]

    return tp_query