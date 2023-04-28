__author__ = "Julián Arenas-Guerrero"
__credits__ = ["Julián Arenas-Guerrero"]

__license__ = "Apache-2.0"
__maintainer__ = "Julián Arenas-Guerrero"
__email__ = "julian.arenas.guerrero@upm.es"


import os
import duckdb
import pandas as pd

from random import randint

from .term import *
from .parser import parse_cotta, parse_rdf, parse_nquads
from .serializer import serialize_cotta, serialize_rdf


class Graph:

    # TODO: https://docs.python.org/3/reference/datamodel.html

    def __init__(self, triplestore=':memory:', read_only=False):
        self.triplestore = duckdb.connect(database=triplestore, read_only=read_only)
        self.triplestore.execute('CREATE TABLE quads (s VARCHAR NOT NULL, p VARCHAR NOT NULL, o VARCHAR NOT NULL, g VARCHAR NOT NULL)')

    def __str__(self):
        return repr(self)

    def __len__(self):
        return self.triplestore.execute('SELECT COUNT(*) FROM quads').fetchone()[0]

    def __contains__(self, quad):
        if len(quad) == 3:
            quad.append('')
        if len(quad) != 4:
            ValueError(f'`{quad}` is not a valid triple or quad. Only 3 or 4 RDF terms are valid.')

        # TODO: validate

        try:
            if self.triplestore.execute("SELECT * FROM quads WHERE s='?' AND p='?' AND o='?' AND g='?'", quad).fetchone():
                return True
        except Exception as e:
            # TODO: log error message, it could be because of adding a duplicate triple, violating CHECK constrainst, etc
            return False
        return False

    def __bool__(self):
        return bool(len(self))

    def __add__(self, other):
        graph = Graph()

        # it is faster to add the largest graph first
        larger_graph, smaller_graph = (self, other) if self > other else (other, self)

        records = larger_graph.to_list()
        graph.bulk_add(records, validate=False, preserve_duplicates=True)

        records = smaller_graph.to_list()
        graph.bulk_add(records, validate=False)

        return graph

    def __iadd__(self, other):
        return self + other

    def __sub__(self, other):
        graph = Graph()

        # it is faster to remove the triples in the smallest graph from the largest graph
        larger_graph, smaller_graph = (self, other) if self > other else (other, self)

        records = larger_graph.to_list()
        graph.bulk_add(records, validate=False, preserve_duplicates=True)

        records = smaller_graph.to_list()
        graph.bulk_remove(records)

        return graph

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
        # TODO: same triples? canonicalization?
        return isinstance(other, Graph) and (len(self) == len(other))

    def __ne__(self, other):
        # TODO: same triples? canonicalization?
        return isinstance(other, Graph) and (len(self) != len(other))

    def size(self):
        return len(self)

    def head(self, number_of_triples=10):
        return self.triplestore.execute(f'SELECT * FROM quads LIMIT {number_of_triples}').fetch_df()

    def tail(self, number_of_triples=10):
        offset = len(self) - number_of_triples
        offset = max(0, offset) # validate offset is non-negative
        return self.triplestore.execute(f'SELECT * FROM quads LIMIT {number_of_triples} OFFSET {offset}').fetch_df()

    def to_df(self):
        return self.triplestore.execute('SELECT * FROM quads').fetch_df()

    def to_arrow(self):
        return self.triplestore.execute('SELECT * FROM quads').fetch_arrow_table()

    def to_list(self):
        return self.to_df().values.tolist()

    def to_chunks(self, chunksize=250000):
        pass    # to_batches

    def add(self, s, p, o, g='', validate=False, preserve_duplicates=False):
        self.bulk_add([[s, p, o, g]], validate=validate, preserve_duplicates=preserve_duplicates)

    def bulk_add(self, quads, validate=False, preserve_duplicates=False):
        temp_columns = ['st', 'pt', 'ot', 'gt']

        quads_df = pd.DataFrame.from_records(quads, columns=temp_columns)

        quads_df['ot'] = quads_df['ot'].apply(remove_xsd_string)

        quads_df['ot'] = quads_df['ot'].apply(decode_escape_sequence)
        # TODO: unicode escaping?

        if validate:
            quads_df['st'].drop_duplicates().apply(validate_subject)
            quads_df['pt'].drop_duplicates().apply(validate_predicate)
            quads_df['ot'].apply(validate_object)
            quads_df['gt'].drop_duplicates().apply(validate_named_graph)

        temporal_table = f'temporal_quads_{randint(0, 10000000000)}'
        self.triplestore.register(temporal_table, quads_df)
        if preserve_duplicates:
            self.triplestore.execute(f'INSERT INTO quads (SELECT * FROM {temporal_table})')
        else:
            #self.triplestore.execute(f'INSERT INTO quads (SELECT DISTINCT * FROM {temporal_table} EXCEPT SELECT * FROM quads)')
            self.triplestore.execute(f'INSERT INTO quads (SELECT * FROM {temporal_table})')
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
        quads = [quad if len(quad) == 4 else quad + [''] for quad in quads]     # add default named graph for triples

        quads_df = pd.DataFrame.from_records(quads, columns=['st', 'pt', 'ot', 'gt'])
        quads_df = quads_df.drop_duplicates()

        temporal_table = f'temporal_quads_{randint(0, 10000000000)}'
        self.triplestore.register(temporal_table, quads_df)
        self.triplestore.execute(f'DELETE FROM quads USING {temporal_table} WHERE quads.s={temporal_table}.st AND quads.p={temporal_table}.pt AND quads.o={temporal_table}.ot AND quads.g={temporal_table}.gt')
        self.triplestore.unregister(temporal_table)

    def parse(self, filepath):
        file_extension = os.path.splitext(filepath)[1].lower()

        if file_extension == '.cotta' or file_extension == '.parquet':
            self.triplestore = parse_cotta(self, filepath)
        elif file_extension == '.nq':
            self.triplestore = parse_nquads(self, filepath)
        else:
            self.triplestore = parse_rdf(self, filepath)

    def serialize(self, filepath, codec='ZSTD', chunksize=250000):
        file_extension = os.path.splitext(filepath)[1].lower()

        if file_extension == '.cotta' or file_extension == '.parquet':
            serialize_cotta(self, filepath, codec)
        elif file_extension == '.nt' or '.nq':
            serialize_rdf(self, filepath, chunksize)
        else:
            print('Invalid serialization file extension. Valid values: `.cotta`, `.parquet`, `.nt`, `.nq`.')

    def sort(self, inplace=True):
        pass

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
            chunk_select_query = f'{select_query} LIMIT {chunksize} OFFSET {i*chunksize}'   # TODO: simplify with self.fetch_df_chunks?
            quads = self.triplestore.execute(chunk_select_query).fetch_df().values.tolist()

            if only_triples:
                for quad in quads:
                    yield quad[0], quad[1], quad[2]
            else:
                for quad in quads:
                    yield quad[0], quad[1], quad[2], quad[3]

    def triples(self, s=None, p=None, o=None, g='', chunksize=250000):
        return self.quads(s, p, o, g, only_triples=True, chunksize=chunksize)

    def subjects(self, p=None, o=None, g='', unique=False):
        variable_dict = {'p': p, 'o': o, 'g': g}

    def objects(self, subject=None, predicate=None, unique=False):
        pass
