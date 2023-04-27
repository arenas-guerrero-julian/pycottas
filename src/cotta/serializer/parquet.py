__author__ = "Julián Arenas-Guerrero"
__credits__ = ["Julián Arenas-Guerrero"]

__license__ = "Apache-2.0"
__maintainer__ = "Julián Arenas-Guerrero"
__email__ = "julian.arenas.guerrero@upm.es"


def serialize_parquet(graph, filepath, file_extension, codec='SNAPPY'):
    graph.triplestore.execute(f"COPY quads TO '{filepath}' (FORMAT 'PARQUET', CODEC '{codec}')")
