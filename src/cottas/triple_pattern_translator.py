__author__ = "Julián Arenas-Guerrero"
__credits__ = ["Julián Arenas-Guerrero"]

__license__ = "Apache-2.0"
__maintainer__ = "Julián Arenas-Guerrero"
__email__ = "julian.arenas.guerrero@upm.es"


from random import randint


def _build_star_query(triple_pattern, query, cottas_file, recursion_track=''):
    s_query, o_query = '', ''

    if type(triple_pattern[0]) is list:
        s_query = _build_star_query(triple_pattern[0], query, cottas_file, f"{recursion_track}s")
    if type(triple_pattern[2]) is list:
        o_query = _build_star_query(triple_pattern[2], query, cottas_file, f"{recursion_track}o")

    query = f"SELECT "
    if type(triple_pattern[0]) is str and triple_pattern[0].startswith('?'):
        query += f"s AS {triple_pattern[0][1:]}, "
    elif type(triple_pattern[0]) is list:
        query += f"s AS s{recursion_track}, "

    if type(triple_pattern[1]) is str and triple_pattern[1].startswith('?'):
        query += f"p AS {triple_pattern[1][1:]}, "

    if type(triple_pattern[2]) is str and triple_pattern[2].startswith('?'):
        query += f"o AS {triple_pattern[2][1:]}, "
    elif type(triple_pattern[2]) is list:
        query += f"o AS o{recursion_track}, "

    # if named graph
    if len(triple_pattern) == 4 and type(triple_pattern[3]) is str and triple_pattern[3].startswith('?'):
        query += f"g AS {triple_pattern[3][1:]}, "

    if recursion_track:
        query += f"CONCAT('<< ', id, ' >>') AS id{recursion_track}, "
    query = f"{query[:-2]} FROM READ_PARQUET('{cottas_file}') WHERE "

    if type(triple_pattern[0]) is str and not triple_pattern[0].startswith('?'):
        query += f"s='{triple_pattern[0]}' AND "
    if not triple_pattern[1].startswith('?'):
        query += f"p='{triple_pattern[1]}' AND "
    if type(triple_pattern[2]) is str and not triple_pattern[2].startswith('?'):
        query += f"o='{triple_pattern[2]}' AND "
    if len(triple_pattern) == 4 and not triple_pattern[3].startswith('?'):
        query += f"g='{triple_pattern[3]}' AND "

    # if recursion level is 0, i.e., recursion_track is ''
    if not recursion_track:
        # checking is asserted is only needed in the root triple pattern
        query += 'ia=TRUE'
    # remove last "AND "
    if query.endswith(' AND '):
        query = query[:-5]
    # remove las "WHERE "
    if query.endswith(' WHERE '):
        query = query[:-6]

    if s_query:
        v1, v2 = f"v{randint(0, 100000)}", f"v{randint(0, 100000)}"
        query = f"SELECT *\nFROM ( ( ( {s_query} ) AS {v1}\nINNER JOIN\n( {query} ) AS {v2} " \
                f"ON {v1}.id{recursion_track}s={v2}.s{recursion_track} ) )"
    if o_query:
        v1, v2 = f"v{randint(0, 100000)}", f"v{randint(0, 100000)}"
        query = f"SELECT *\nFROM ( ( ( {o_query} ) AS {v1}\nINNER JOIN\n( {query} ) AS {v2} " \
                f"ON {v1}.id{recursion_track}o={v2}.o{recursion_track} ) )"

    return query


def translate_triple_pattern(cottas_file, triple_pattern_str):
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
            triple_pattern_query += f"IF(STARTS_WITH({var}, '<< '), ARRAY_SLICE({var}, 4, -3), {var}) AS {var}, "
        triple_pattern_query = f"{triple_pattern_query[:-2]}\n" \
                               f"FROM ( {_build_star_query(triple_pattern, '', cottas_file)} )"
    else:
        triple_pattern_query = f"SELECT "
        if triple_pattern[0].startswith('?'):
            triple_pattern_query += f"s AS {triple_pattern[0][1:]}, "
        if triple_pattern[1].startswith('?'):
            triple_pattern_query += f"p AS {triple_pattern[1][1:]}, "
        if triple_pattern[2].startswith('?'):
            triple_pattern_query += f"o AS {triple_pattern[2][1:]}, "
        if len(triple_pattern) == 4 and triple_pattern[3].startswith('?'):
            triple_pattern_query += f"g AS {triple_pattern[3][1:]}, "

        triple_pattern_query = f"{triple_pattern_query[:-2]}\nFROM READ_PARQUET('{cottas_file}')\nWHERE "

        if not triple_pattern[0].startswith('?'):
            triple_pattern_query += f"s='{triple_pattern[0]}' AND "
        if not triple_pattern[1].startswith('?'):
            triple_pattern_query += f"p='{triple_pattern[1]}' AND "
        if not triple_pattern[2].startswith('?'):
            triple_pattern_query += f"o='{triple_pattern[2]}' AND "
        if len(triple_pattern) == 4 and not triple_pattern[3].startswith('?'):
            triple_pattern_query += f"g='{triple_pattern[3]}' AND "
        triple_pattern_query += "ia=TRUE"

    print(triple_pattern_query)
    return triple_pattern_query
