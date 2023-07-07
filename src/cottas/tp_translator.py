__author__ = "Julián Arenas-Guerrero"
__credits__ = ["Julián Arenas-Guerrero"]

__license__ = "Apache-2.0"
__maintainer__ = "Julián Arenas-Guerrero"
__email__ = "julian.arenas.guerrero@upm.es"


from random import randint


# dict mapping RDF-star term positions to attribute names
i_pos = {
    0: 's',
    1: 'p',
    2: 'o',
    3: 'g'
}


def _get_projected_vars(tp_str):
    """
    :param tp_str: a user-defined triple pattern
    :return: a list with the names of the variables in the triple pattern
    """

    # we split the string, so avoid cases where `<<` and `>>` are together with variables, e.g., <<?s ?p ?o>>
    projection_str = tp_str.replace("<<", ' ').replace(">>", ' ')
    # split and keep only substring starting by `?` (removing the starting `?`)
    projection_list = [sub_str[1:] for sub_str in projection_str.split() if sub_str.startswith('?')]

    return projection_list


def _construct_tp_tree(tp_str):
    """
    A SPARQL-star triple pattern resembles a binary tree structure (subject and object can be in turn other
    SPARQL-star triple pattern). This method evaluates a user-defined SPARQL-star triple pattern and constructs its
    tree structure. The tree is given by nested lists: (i) each triple pattern is a list [s, p, o], (ii) if the
    `s` or `o` are SPARQL-star triple patterns, they are given by a nested list.

    :param tp_str: a user-defined triple pattern
    :return: a list of the triple pattern representing its binary tree structure
    """
    # the general idea is to transform the user-defined triple pattern into a string representation that can be
    # evaluated by Python into nested lists

    # we split the string, so avoid cases where `<<` are together with the subject, e.g., <<?s ?p ?o>>
    tp_str = tp_str.replace('<<', '<< ')
    # same for the object, but it is necessary to reverse the string before replacement (then reverse it back)
    tp_str = tp_str[::-1].replace('>>', '>> ')[::-1]

    # enclose with quotes each substring, e.g., ?s: '?s', "24": '"24"', <<: '<<'
    tp_str = ' '.join("'{}'".format(sub_str) for sub_str in tp_str.split())

    # convert `<<`, `>>` to `[`, `]` so that SPARQL-star triple pattern are interpreted as lists
    tp_str = tp_str.replace("'<<' ", '[').replace(" '>>'", ']')
    # the separators in Python lists are not whitespaces but commas
    tp_str = tp_str.replace(' ', ',')
    # the root list of the SPARQL-star triple pattern
    tp_str = f"[{tp_str}]"

    # finally, evaluate the string representation to nested lists
    tp = eval(tp_str)

    return tp


def _construct_tp_star_query(tp, cottas_file, traversal_path=''):
    """

    :param tp: triple pattern
    :param cottas_file: path to a COTTAS file
    :param traversal_path: trace of the tree traversal path according to the recursive calls. The empty string
    represents the root of the tree. `sos` represents a traversal path of depth 3 given by recursive calls in the
    (i) subject, (ii) object, and (iii) subject positions.
    :return:
    """

    query = f"SELECT "

    # build projection iterating over all positions in the triple pattern
    for i in range(4):
        # skip named graph if not in the triple pattern
        if i < len(tp):
            # if the position is a variable, project it (removing the `?`)
            if type(tp[i]) is str and tp[i].startswith('?'):
                query += f"{i_pos[i]} AS {tp[i][1:]}, "
            # if the position is a triple pattern, project its hash for later joining
            elif type(tp[i]) is list:
                query += f"HASH({i_pos[i]}) AS {traversal_path}{i_pos[i]}, "

    # if there is recursion, we need to reference the id for joining in upper levels of the tree
    if traversal_path:
        query += f"id AS id{traversal_path}, "

    # remove final `, `
    query = query[:-2]
    query += f" FROM PARQUET_SCAN('{cottas_file}') WHERE "

    # build selection iterating over all positions in the triple pattern
    for i in range(4):
        # skip named graph if not in the triple pattern
        if i < len(tp):
            if type(tp[i]) is str and not tp[i].startswith('?'):
                query += f"{i_pos[i]}='{tp[i]}' AND "

    if not traversal_path:
        # is asserted must only be checked in the root triple pattern (where no recursion)
        query += 'ia=TRUE'

    # remove final `AND ` and `WHERE `
    if query.endswith('AND '):
        query = query[:-4]
    if query.endswith('WHERE '):
        query = query[:-6]

    # if triple patterns in the subject or object, build the corresponding queries and join them with main query
    for i in (0, 2):
        if type(tp[i]) is list:
            # recursive call to construct the query for the nested triple pattern
            # trace tree traversal path by appending position of the triple pattern to traversal_path
            star_query = _construct_tp_star_query(tp[i], cottas_file, f"{traversal_path}{i_pos[i]}")

            # join main and star queries
            v1, v2 = f"v{randint(0, 100000)}", f"v{randint(0, 100000)}"
            query = f"SELECT *\nFROM ( ( ( {star_query} ) AS {v1}\nINNER JOIN\n( {query} ) AS {v2} " \
                    f"ON {v1}.id{traversal_path}{i_pos[i]}={v2}.{traversal_path}{i_pos[i]} ) )"

    return query


def translate_triple_pattern(cottas_file, tp_str):
    """
    Given a COTTAS file and a user-defined triple pattern, translate the triple pattern to an SQL over COTTAS.

    :param cottas_file: path to a COTTAS file
    :param tp_str: a user-defined triple pattern
    :return: SQL query for the triple pattern
    """

    projection_list = _get_projected_vars(tp_str)
    tp = _construct_tp_tree(tp_str)

    tp_query = "SELECT "
    for var in projection_list:
        tp_query += f"IF (STARTS_WITH({var}, '<<'), ARRAY_SLICE({var}, 3, -2), {var}) AS {var}, "
    tp_query = f"{tp_query[:-2]}\nFROM ( {_construct_tp_star_query(tp, cottas_file)} )"

    print(tp_query)
    return tp_query
