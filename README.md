# pycottas

[![License](https://img.shields.io/pypi/l/pycottas.svg)](https://github.com/arenas-guerrero-julian/pycottas/blob/main/LICENSE)
[![Latest PyPI version](https://img.shields.io/pypi/v/cottas?style=flat)](https://pypi.python.org/pypi/pycottas)
[![Python Version](https://img.shields.io/pypi/pyversions/cottas.svg)](https://pypi.python.org/pypi/pycottas)
[![PyPI status](https://img.shields.io:/pypi/status/cottas?)](https://pypi.python.org/pypi/pycottas)
[![Documentation Status](https://readthedocs.org/projects/pycottas/badge/?version=latest)](https://pycottas.readthedocs.io)

**pycottas** is a library for working with **compressed** **[RDF](https://www.w3.org/TR/rdf11-concepts/)** files in the **COTTAS** format. COTTAS stores triples (or quads) in a triple table in the [Apache Parquet](https://parquet.apache.org/) format.

## Features :sparkles:

- **Compression** and **decompression** of RDF files.
- Querying COTTAS files with **triple patterns**.
- [RDFLib](https://github.com/RDFLib/rdflib) backend for querying COTTAS files with **[SPARQL](https://www.w3.org/TR/sparql11-query/)**.
- Supports named graphs (**quads**).
- Can be used as a **library** or via **command line**.

## Documentation :bookmark_tabs:

**[Read the documentation](https://pycottas.readthedocs.io)**.

## Getting Started :rocket:

**[PyPi](https://pypi.org/project/pycottas/)** is the fastest way to install pycottas:
```bash
pip install pycottas
```

We recommend to use **[virtual environments](https://docs.python.org/3/library/venv.html#)** to install pycottas.

```python

import pycottas
from rdflib import Graph, URIRef

pycottas.rdf2cottas('my_file.ttl', 'my_file.cottas', index='spo')
res = pycottas.search('my_file.cottas', '?s <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> ?o')
print(res)
pycottas.cottas2rdf('my_file.cottas', 'my_file.nt')

# COTTASDocument class for querying with triple patterns
cottas_doc = pycottas.COTTASDocument('my_file.cottas')
# the triple pattern can be a string or a tuple
res = cottas_doc.search('?s <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> ?o')
# limit and offset are optional
res = pycottas.search('a.cottas', (None, URIRef('http://www.w3.org/ns/r2rml#termType'), None))
res = cottas_doc.search((None, URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#type'), None), limit=10, offset=20)
print(res)

# COTTASStore class for querying with SPARQL
graph = Graph(store=pycottas.COTTASStore("my_file.cottas"))
res = graph.query("""
  PREFIX rdf: <http://xmlns.com/foaf/0.1/>
  SELECT DISTINCT ?s ?o WHERE {
    ?s rdf:type ?o .
  }""")
for row in res:
    print(row)
```

To execute via **command line** check the docs.

## License :unlock:

**pycottas** is available under the **[Apache License 2.0](https://github.com/arenas-guerrero-julian/pycottas/blob/main/LICENSE)**.

## Author & Contact :mailbox_with_mail:

- **[Julián Arenas-Guerrero](https://github.com/arenas-guerrero-julian/) - [julian.arenas.guerrero@upm.es](mailto:julian.arenas.guerrero@upm.es)**

*[Universidad Politécnica de Madrid](https://www.upm.es/internacional)*.
