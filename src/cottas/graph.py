__author__ = "Julián Arenas-Guerrero"
__credits__ = ["Julián Arenas-Guerrero"]

__license__ = "Apache-2.0"
__maintainer__ = "Julián Arenas-Guerrero"
__email__ = "julian.arenas.guerrero@upm.es"


import os
import duckdb
import pandas as pd

from random import randint

from .constants import DUCKDB_MEMORY
from .parser import parse_cottas, parse_rdf, parse_nquads
from .serializer import serialize_cottas, serialize_rdf


class Graph:

    def __init__(self, triplestore=DUCKDB_MEMORY):
        self.triplestore = duckdb.connect(database=triplestore)
        self.triplestore.execute(
            'CREATE TABLE quads ('
            's VARCHAR NOT NULL, p VARCHAR NOT NULL, o VARCHAR NOT NULL, g VARCHAR NOT NULL, id VARCHAR NOT NULL)')

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
        offset = max(0, offset)     # validate offset is non-negative
        return self.triplestore.execute(f'SELECT * FROM quads LIMIT {number_of_triples} OFFSET {offset}').fetch_df()

    def to_df(self):
        return self.triplestore.execute('SELECT * FROM quads').fetch_df()

    def to_arrow(self):
        return self.triplestore.execute('SELECT * FROM quads').fetch_arrow_table()

    def to_list(self):
        return self.to_df().values.tolist()

    def add(self, s, p, o, g='', preserve_duplicates=True):
        self.bulk_add([[s, p, o, g]], preserve_duplicates=preserve_duplicates)

    def bulk_add(self, quads, preserve_duplicates=True):
        quads_df = pd.DataFrame.from_records(quads, columns=['st', 'pt', 'ot', 'gt', 'idt'])

        temporal_table = f'temporal_quads_{randint(0, 1000000)}'
        self.triplestore.register(temporal_table, quads_df)
        if preserve_duplicates:
            self.triplestore.execute(f'INSERT INTO quads (SELECT * FROM {temporal_table})')
        else:
            self.triplestore.execute(f'INSERT INTO quads (SELECT DISTINCT * FROM {temporal_table} '
                                     f'EXCEPT SELECT * FROM quads)')
        self.triplestore.unregister(temporal_table)

    def remove(self, s, p, o, g=''):
        variable_dict = {'s': s, 'p': p, 'o': o, 'g': g}
        variable_dict = {k: v for k, v in variable_dict.items() if v is not None}

        if not len(variable_dict):
            self.triplestore.execute('DELETE FROM quads')
        else:
            delete_query = 'DELETE FROM quads WHERE '
            for k, v in variable_dict.items():
                delete_query += f"{k}='{v}' AND "
            delete_query = delete_query[:-5]    # remove final ` AND `

            self.triplestore.execute(delete_query)

    def bulk_remove(self, quads):
        quads_df = pd.DataFrame.from_records(quads, columns=['st', 'pt', 'ot', 'gt', 'idt'])
        quads_df = quads_df.drop_duplicates()

        temporal_table = f'temporal_quads_{randint(0, 1000000)}'
        self.triplestore.register(temporal_table, quads_df)
        self.triplestore.execute(f'DELETE FROM quads USING {temporal_table} WHERE '
                                 f'quads.s={temporal_table}.st AND quads.p={temporal_table}.pt AND '
                                 f'quads.o={temporal_table}.ot AND quads.g={temporal_table}.gt')
        self.triplestore.unregister(temporal_table)

    def parse(self, filepath, preserve_duplicates=True):
        file_extension = os.path.splitext(filepath)[1].lower()

        if file_extension == '.cottas' or file_extension == '.parquet' or file_extension == '.pq':
            self.triplestore = parse_cottas(self, filepath)
        elif file_extension == '.nq':   # lightrdf does not support N-Quads
            self.triplestore = parse_nquads(self, filepath, preserve_duplicates)
        else:
            self.triplestore = parse_rdf(self, filepath, preserve_duplicates)

    def serialize(self, filepath, codec='ZSTD', chunksize=250000):
        file_extension = os.path.splitext(filepath)[1].lower()

        if file_extension == '.cottas' or file_extension == '.parquet' or file_extension == '.pq':
            serialize_cottas(self, filepath, codec)
        elif file_extension == '.nt' or '.nq':
            serialize_rdf(self, filepath, chunksize)
        else:
            print('Invalid serialization file extension. Valid values: `.cottas`, `.parquet`, `.pq`, `.nt`, `.nq`.')

    def quads(self, s=None, p=None, o=None, g=None, only_triples=False, chunksize=250000):
        variable_dict = {'s': s, 'p': p, 'o': o, 'g': g}
        variable_dict = {k: v for k, v in variable_dict.items() if v is not None}

        select_query = 'SELECT * FROM quads'

        if len(variable_dict):
            select_query += ' WHERE '
            for k, v in variable_dict.items():
                select_query += f"{k}='{v}' AND "
            select_query = select_query[:-5]  # remove final ` AND `

        for i in range((len(self) // chunksize) + 1):
            chunk_select_query = f'{select_query} LIMIT {chunksize} OFFSET {i*chunksize}'
            quads = self.triplestore.execute(chunk_select_query).fetch_df().values.tolist()

            if only_triples:
                for quad in quads:
                    yield quad[0], quad[1], quad[2]
            else:
                for quad in quads:
                    yield quad[0], quad[1], quad[2], quad[3]

    def triples(self, s=None, p=None, o=None, g='', chunksize=250000):
        return self.quads(s, p, o, g, only_triples=True, chunksize=chunksize)
