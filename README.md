# pycottas

[![License](https://img.shields.io/pypi/l/pycottas)](https://github.com/arenas-guerrero-julian/pycottas/blob/main/LICENSE)
[![DOI](https://zenodo.org/badge/633315029.svg)](https://doi.org/10.5281/zenodo.15350990)
[![Latest PyPI version](https://img.shields.io/pypi/v/pycottas?style=flat)](https://pypi.python.org/pypi/pycottas)
[![Python Version](https://img.shields.io/pypi/pyversions/pycottas.svg)](https://pypi.python.org/pypi/pycottas)
[![PyPI status](https://img.shields.io:/pypi/status/pycottas?)](https://pypi.python.org/pypi/pycottas)
[![Documentation Status](https://readthedocs.org/projects/pycottas/badge/?version=latest)](https://pycottas.readthedocs.io)

**pycottas** is a library for working with **compressed** **[RDF](https://www.w3.org/TR/rdf11-concepts/)** files in the **COTTAS** format. COTTAS stores triples as a triple table in [Apache Parquet](https://parquet.apache.org/). It is built on top of [DuckDB](https://duckdb.org/) and provides an [HDT](https://www.rdfhdt.org/)-like interface.

## Features :sparkles:

- **Compression** and **decompression** of RDF files.
- Querying COTTAS files with **[triple patterns](https://www.w3.org/TR/sparql11-query/#sparqlTriplePatterns)**.
- [RDFLib](https://github.com/RDFLib/rdflib) store backend for querying COTTAS files with **[SPARQL](https://www.w3.org/TR/sparql11-query/)**.
- Supports [RDF datasets](https://www.w3.org/TR/rdf11-concepts/#section-dataset) (**quads**).
- Can be used as a **library** or via **command line**.

## Documentation :bookmark_tabs:

**[Read the documentation](https://pycottas.readthedocs.io/en/latest/documentation/)**.

## Getting Started :rocket:

**[PyPI](https://pypi.org/project/pycottas/)** is the fastest way to install pycottas:
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
# the triple pattern can be a string (below) or a tuple of RDFLib terms
res = cottas_doc.search('?s <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> ?o')

# COTTASStore class for querying with SPARQL
graph = Graph(store=pycottas.COTTASStore('my_file.cottas'))
res = graph.query('''
  PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
  SELECT DISTINCT ?s ?o WHERE {
    ?s rdf:type ?o .
  } LIMIT 10''')
for row in res:
    print(row)
```

To execute via **command line** check the [docs](https://pycottas.readthedocs.io/en/latest/documentation/#command-line).

## License :unlock:

**pycottas** is available under the **[Apache License 2.0](https://github.com/arenas-guerrero-julian/pycottas/blob/main/LICENSE)**.

## Author & Contact :mailbox_with_mail:

- **[Julián Arenas-Guerrero](https://github.com/arenas-guerrero-julian/) - [julian.arenas.guerrero@upm.es](mailto:julian.arenas.guerrero@upm.es)**

*[Universidad Politécnica de Madrid](https://www.upm.es/internacional)*.

## Citing :speech_balloon:

If you used pycottas in your work, please cite the **[ISWC paper](https://www.researchgate.net/profile/Julian_Arenas-Guerrero/publication/394146089_COTTAS_Columnar_Triple_Table_Storage_for_Efficient_and_Compressed_RDF_Management/links/688b7410d26c2f6f56d71667/COTTAS-Columnar-Triple-Table-Storage-for-Efficient-and-Compressed-RDF-Management.pdf?origin=publicationDetail&_sg%5B0%5D=cbHy3nejio22UaFokTJTKnURSf5wYV0crJtQ8pAryjeNpj-8odPjns2zrN9pPWjjy9Vz2strK3xAZhg12XLLfw.m5GZ8H8xuq-3T22No3-8MbsxN4DaXbYC9XBJtmb2YqA-gs_XzYOrosFMPAQomVsNyMa5HGM3P9DfqaiZtWI44A&_sg%5B1%5D=aAhtCdTPSEItp6DG1HaxClJn3ijFnR3dC0B1b6NRSbft_B-M_LUeKQjdZBdyB5wjQrVwkn7dNhEN3QHxfJa64wheKE8lZMkD0etQBnXIViua.m5GZ8H8xuq-3T22No3-8MbsxN4DaXbYC9XBJtmb2YqA-gs_XzYOrosFMPAQomVsNyMa5HGM3P9DfqaiZtWI44A&_iepl=&_rtd=eyJjb250ZW50SW50ZW50IjoibWFpbkl0ZW0ifQ%3D%3D&_tp=eyJjb250ZXh0Ijp7ImZpcnN0UGFnZSI6InB1YmxpY2F0aW9uIiwicGFnZSI6InB1YmxpY2F0aW9uIiwicG9zaXRpb24iOiJwYWdlSGVhZGVyIn19)**:

```bib
@inproceedings{arenas2025cottas,
  title     = {{COTTAS: Columnar Triple Table Storage for Efficient and Compressed RDF Management}},
  author    = {Arenas-Guerrero, Julián and Ferrada, Sebastián},
  booktitle = {Proceedings of the 24th International Semantic Web Conference, ISWC},
  year      = {2025},
}
```
