__author__ = "Julián Arenas-Guerrero"
__credits__ = ["Julián Arenas-Guerrero"]

__license__ = "Apache-2.0"
__maintainer__ = "Julián Arenas-Guerrero"
__email__ = "julian.arenas.guerrero@upm.es"


import duckdb

from typing import Iterable
from rdflib.store import Store
from rdflib.util import from_n3
from cottas.types import Triple
from cottas.tp_translator import translate_triple_pattern_tuple


class COTTASStore(Store):
    """An implementation of a Store over a COTTAS document.

    It is heavily inspired by the work from @FlorianLudwig (https://github.com/RDFLib/rdflib/issues/894) and rdflib-hdt (https://github.com/RDFLib/rdflib-hdt).
l
    Args:
      - path: Absolute path to the COTTAS file to load.
    """
    def __init__(self, path: str, configuration=None, identifier=None):
        super(COTTASStore, self).__init__(configuration=configuration, identifier=identifier)
        # TODO: verify
        self._cottas_path = path
        duckdb.query(f"SET parquet_metadata_cache=true; SET enable_progress_bar=false; SELECT * FROM PARQUET_SCAN('{path}')")
        #self._nb_subjects = list(duckdb.query("SELECT COUNT(DISTINCT s) AS s_count FROM PARQUET_SCAN('{path}')").df()['s_count'])[0]
        #self._nb_predicates =
        #self._nb_objects =

    @property
    def cottas_file(self) -> str:
        """The COTTAS file path."""
        return self._cottas_path

    def __len__(self, context) -> int:
        """The number of RDF triples in the COTTAS store."""
        return False

    @property
    def nb_subjects(self) -> int:
        """The number of subjects in the COTTAS store."""
        return False

    @property
    def nb_predicates(self) -> int:
        """The number of predicates in the COTTAS store."""
        return False

    @property
    def nb_objects(self) -> int:
        """The number of objects in the COTTAS store."""
        return False

    @property
    def nb_shared(self) -> int:
        """The number of shared subject-object in the COTTAS store."""
        # TODO: remove?
        return False

    def triples(self, pattern, context) -> Iterable[Triple]:
        """Search for a triple pattern in a COTTAS store.

        Args:
          - pattern: The triple pattern (s, p, o) to search.
          - context: The query execution context.

        Returns: An iterator that produces RDF triples matching the input triple pattern.
        """
        for triple in duckdb.execute(translate_triple_pattern_tuple(self._cottas_path, pattern)).fetchall():
            triple = from_n3(triple[0]), from_n3(triple[1]), from_n3(triple[2])
            yield triple, None
        return

    def create(self, configuration):
        raise TypeError('The COTTAS store is read only!')

    def destroy(self, configuration):
        raise TypeError('The COTTAS store is read only!')

    def commit(self):
        raise TypeError('The COTTAS store is read only!')

    def rollback(self):
        raise TypeError('The COTTAS store is read only!')

    def add(self, _, context=None, quoted=False):
        raise TypeError('The COTTAS store is read only!')

    def addN(self, quads):
        raise TypeError('The COTTAS store is read only!')

    def remove(self, _, context):
        raise TypeError('The COTTAS store is read only!')