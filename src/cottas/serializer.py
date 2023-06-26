__author__ = "Julián Arenas-Guerrero"
__credits__ = ["Julián Arenas-Guerrero"]

__license__ = "Apache-2.0"
__maintainer__ = "Julián Arenas-Guerrero"
__email__ = "julian.arenas.guerrero@upm.es"


def serialize_cottas(graph, filepath, codec='ZSTD'):
    graph.triplestore.execute(f"COPY quads TO '{filepath}' (FORMAT 'PARQUET', CODEC '{codec}')")


def serialize_rdf(graph, filepath):
    f = open(filepath, 'w')

    duckdb_cursor = graph.triplestore.cursor()
    query = duckdb_cursor.execute("SELECT s, p, o, g FROM quads")

    cur_chunk_df = query.fetch_df_chunk()
    while len(cur_chunk_df):
        quads = cur_chunk_df.values.tolist()

        for quad in quads:
            # format quoted triples
            if ' <' in quad[0]:
                quad[0] = f'<< {quad[0]} >>'
            if ' <' in quad[2]:
                quad[2] = f'<< {quad[2]} >>'

            if quad[3]:
                # in case of named graph
                quad = f"{quad[0]} {quad[1]} {quad[2]} {quad[3]}"
            else:
                quad = f"{quad[0]} {quad[1]} {quad[2]}"

            f.write(f'{quad} .\n')

        cur_chunk_df = query.fetch_df_chunk()

    f.close()
