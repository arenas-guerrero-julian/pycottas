__author__ = "Julián Arenas-Guerrero"
__credits__ = ["Julián Arenas-Guerrero"]

__license__ = "Apache-2.0"
__maintainer__ = "Julián Arenas-Guerrero"
__email__ = "julian.arenas.guerrero@upm.es"



def serialize_cotta(graph, filepath, codec='SNAPPY'):
    graph.triplestore.execute(f"COPY quads TO '{filepath}' (FORMAT 'PARQUET', CODEC '{codec}')")
    

def serialize_rdf(graph, filepath, chunksize=1000000):
    f = open(filepath, 'w')

    for i in range((len(graph) // chunksize) + 1):
        quads_df = graph.triplestore.execute(f'SELECT * FROM quads LIMIT {chunksize} OFFSET {i*chunksize}').fetch_df()

        quads = quads_df.values.tolist()
        for quad in quads:
            quad = f"{quad[0]} {quad[1]} {quad[2]}"
            if quad[3]:
                quad += f" {quad[3]}"

            f.write(f'{quad} .\n')

    f.close()
