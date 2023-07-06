__author__ = "Julián Arenas-Guerrero"
__credits__ = ["Julián Arenas-Guerrero"]

__license__ = "Apache-2.0"
__maintainer__ = "Julián Arenas-Guerrero"
__email__ = "julian.arenas.guerrero@upm.es"


import os
import duckdb
import io

import pandas as pd

from random import randint

from .constants import DUCKDB_MEMORY
from .parser import parse_cottas, parse_rdf, parse_rdf_fs
from .serializer import serialize_cottas, serialize_rdf


class Graph:

    def __init__(self, triplestore=DUCKDB_MEMORY, preserve_duplicates=True):
        self.preserve_duplicates = preserve_duplicates

        self.triplestore = duckdb.connect(database=triplestore)
        self.triplestore.execute(
            'CREATE TABLE quads (s VARCHAR NOT NULL, p VARCHAR NOT NULL, o VARCHAR NOT NULL, g VARCHAR NOT NULL, '
            'id VARCHAR NOT NULL, ia BOOLEAN NOT NULL)')

    def __str__(self):
        return repr(self)

    def __len__(self):
        return self.triplestore.execute('SELECT COUNT(*) FROM quads').fetchone()[0]

    def __contains__(self, quad):
        if len(quad) == 3:
            quad.append('')
        if len(quad) != 4:
            ValueError(f'`{quad}` is not a valid triple or quad. Only 3 or 4 RDF terms are valid.')

        try:
            if self.triplestore.execute("SELECT * FROM quads WHERE s='?' AND p='?' AND o='?' AND g='?'",
                                        quad).fetchone():
                return True
        except Exception as e:
            return False
        return False

    def __bool__(self):
        return bool(len(self))

    def __add__(self, other):
        self.bulk_add(other.to_list())

        return self

    def __iadd__(self, other):
        return self + other

    def __sub__(self, other):
        self.bulk_remove(other.to_list())

        return self

    def __isub__(self, other):
        return self - other

    def __lt__(self, other):
        return isinstance(other, Graph) and (len(self) < len(other))

    def __le__(self, other):
        return isinstance(other, Graph) and (len(self) <= len(other))

    def __gt__(self, other):
        return isinstance(other, Graph) and (len(self) > len(other))

    def __ge__(self, other):
        return isinstance(other, Graph) and (len(self) <= len(other))

    def __eq__(self, other):
        return isinstance(other, Graph) and (len(self) == len(other))

    def __ne__(self, other):
        return isinstance(other, Graph) and (len(self) != len(other))

    def size(self):
        return len(self)

    def head(self, number_of_triples=10):
        return self.triplestore.execute(f'SELECT * FROM quads LIMIT {number_of_triples}').fetch_df()

    def tail(self, number_of_triples=10):
        offset = len(self) - number_of_triples
        offset = max(0, offset)     # ensure offset is non-negative
        return self.triplestore.execute(f'SELECT * FROM quads LIMIT {number_of_triples} OFFSET {offset}').fetch_df()

    def to_df(self):
        return self.triplestore.execute('SELECT * FROM quads').fetch_df()

    def to_arrow(self):
        return self.triplestore.execute('SELECT * FROM quads').fetch_arrow_table()

    def to_list(self):
        return self.to_df().values.tolist()

    def bulk_add(self, quads):
        quads_df = pd.DataFrame.from_records(quads, columns=['st', 'pt', 'ot', 'gt', 'idt', 'iat'])

        temporal_table = f'temporal_quads_{randint(0, 1000000)}'
        self.triplestore.register(temporal_table, quads_df)

        self.triplestore.execute(f'INSERT INTO quads (SELECT * FROM {temporal_table})')

        self.triplestore.unregister(temporal_table)

    def bulk_remove(self, quads):
        quads_df = pd.DataFrame.from_records(quads, columns=['st', 'pt', 'ot', 'gt', 'idt', 'iat'])
        quads_df = quads_df.drop_duplicates()

        temporal_table = f'temporal_quads_{randint(0, 1000000)}'
        self.triplestore.register(temporal_table, quads_df)

        # this can also be done checking only (id, g) but it requires/assumes id to be precomputed
        self.triplestore.execute(f'DELETE FROM quads USING {temporal_table} WHERE '
                                 f'quads.s={temporal_table}.st AND quads.p={temporal_table}.pt AND '
                                 f'quads.o={temporal_table}.ot AND quads.g={temporal_table}.gt')

        self.triplestore.unregister(temporal_table)

    def parse(self, filepath):
        file_extension = os.path.splitext(filepath)[1].lower()

        if file_extension in ['.cottas', '.parquet', '.pq']:
            self.triplestore = parse_cottas(self, filepath)
        elif self.preserve_duplicates:
            self.triplestore = parse_rdf(self, filepath)
        else:
            # use the file system
            self.triplestore = parse_rdf_fs(self, filepath)

    def serialize(self, filepath, codec='ZSTD'):
        file_extension = os.path.splitext(filepath)[1].lower()

        if file_extension in ['.cottas', '.parquet', '.pq']:
            serialize_cottas(self, filepath, codec)
        elif file_extension in ['.nt', '.nq']:
            serialize_rdf(self, filepath)
        else:
            print('Invalid serialization file extension. Valid values: `.cottas`, `.parquet`, `.pq`, `.nt`, `.nq`.')

    def create_id(self):
        self.triplestore.execute(f"UPDATE quads SET id=CONCAT(s, ' ', p, ' ', o)")

    def remove_id(self):
        self.triplestore.execute(f"UPDATE quads SET id=NULL")

    def expand_quoted_triples(self):
        graph_num_triples = len(self)
        s_o = ['s', 'o']            # to alternate between subject and object positions
        i = 0                       # whether subject or object in s_o is being processed
        position_changed = False    # if True, expansion through previous position was unsuccessful

        while True:
            # LEFT JOIN between a quoted column (s, o) with id column
            # if id IS NULL then there is no id for that quoted triple, hence there is no record for the quoted triple
            expand_query = f"""
                SELECT DISTINCT {s_o[i]} FROM (
                    ( SELECT ARRAY_SLICE({s_o[i]}, 4, -3) AS {s_o[i]} FROM quads
                            WHERE STARTS_WITH({s_o[i]}, '<< ') ) AS v1
                    LEFT JOIN
                    ( SELECT id FROM quads ) as v2
                    ON v1.{s_o[i]}=v2.id
                ) WHERE id IS NULL
            """

            duckdb_cursor = self.triplestore.cursor()
            query = duckdb_cursor.execute(expand_query)

            # process query results in a streaming manner
            cur_chunk_df = query.fetch_df_chunk()
            while len(cur_chunk_df):
                # generate N-Triples string and load it to the graph
                quads_text = f"{'. '.join(list(cur_chunk_df[s_o[i]]))} ."
                self.triplestore = parse_rdf(self, io.BytesIO(quads_text.encode()), is_asserted=False,
                                             mime_type='application/n-triples')

                # process next chunk of the query result set
                cur_chunk_df = query.fetch_df_chunk()

            # if the graph is larger after expansion, expand it further
            if graph_num_triples < len(self):
                graph_num_triples = len(self)
                # reset position, the graph could be expanded through subject or object
                position_changed = False
            # expansion was not possible through the current position, try with the other position
            elif not position_changed:
                # mark that expansion through current position was unsuccessful
                position_changed = True
                # switch position in s_o
                i = (i+1) % 2
            # expanding the graph through subject and object was unsuccessful, it is not possible to expand further
            else:
                # terminate expansion
                break

    def shrink_quoted_triples(self):
        self.triplestore.execute(f"DELETE FROM quads WHERE ia=FALSE")
