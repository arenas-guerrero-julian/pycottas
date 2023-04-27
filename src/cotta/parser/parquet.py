__author__ = "Julián Arenas-Guerrero"
__credits__ = ["Julián Arenas-Guerrero"]

__license__ = "Apache-2.0"
__maintainer__ = "Julián Arenas-Guerrero"
__email__ = "julian.arenas.guerrero@upm.es"


from random import randint


def parse_parquet(graph, filepath, file_extension):
    temporal_table = f'temporal_quads_{randint(0, 10000000000)}'
    graph.triplestore.execute(f"CREATE TABLE {temporal_table} AS SELECT * FROM parquet_scan('{filepath}')")

    if len(graph.triplestore.execute(f"DESCRIBE {temporal_table}").fetchall()) == 3:
        # add empty named graphs column
        graph.triplestore.execute(f"ALTER TABLE {temporal_table} ADD COLUMN g TEXT DEFAULT ''")

    graph.triplestore.execute(f'INSERT INTO quads (SELECT * FROM {temporal_table} EXCEPT SELECT * FROM quads)')
    graph.triplestore.execute(f'DROP TABLE {temporal_table}')

    return graph.triplestore
