# pycottas

[![License](https://img.shields.io/pypi/l/pycottas.svg)](https://github.com/arenas-guerrero-julian/pycottas/blob/main/LICENSE)
[![Latest PyPI version](https://img.shields.io/pypi/v/cottas?style=flat)](https://pypi.python.org/pypi/pycottas)
[![Python Version](https://img.shields.io/pypi/pyversions/cottas.svg)](https://pypi.python.org/pypi/pycottas)
[![PyPI status](https://img.shields.io:/pypi/status/cottas?)](https://pypi.python.org/pypi/pycottas)
[![Documentation Status](https://readthedocs.org/projects/pycottas/badge/?version=latest)](https://pycottas.readthedocs.io)

**pycottas** is a library for working with **compressed** **[RDF](https://www.w3.org/TR/rdf11-concepts/)** files in the **COTTAS** format. COTTAS stores triples (or quads) in a triple table in the [Apache Parquet](https://parquet.apache.org/) format.

## Features :sparkles:

- Compression and decompression of RDF files.
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
pycottas.rdf2cottas('my_file.ttl', 'my_file.cottas', index='spo')

pycottas.search('my_file.cottas', '?s <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> ?o')


```

Execute pycottas in the command line with:
```
python3 -m pycottas ...
```

Complete the command with one of the following operations ([check the docs]() for more details):

```
usage: pycottas [-h] {rdf2cottas,cottas2rdf,search,info,verify,cat,diff} ...

positional arguments:
  {rdf2cottas,cottas2rdf,search,info,verify,cat,diff}
                        subcommand help
    rdf2cottas          Compress an RDF file into COTTAS format
    cottas2rdf          Decompress a COTTAS file to RDF (N-Triples)
    search              Evaluate a triple pattern
    info                Get the metadata of a COTTAS file
    verify              Check whether a file is a valid COTTAS file
    cat                 Merge multiple COTTAS files
    diff                Subtract the triples in a COTTAS files from another

options:
  -h, --help            show this help message and exit
```


## License :unlock:

**pycottas** is available under the **[Apache License 2.0](https://github.com/arenas-guerrero-julian/pycottas/blob/main/LICENSE)**.

## Author & Contact :mailbox_with_mail:

- **[Julián Arenas-Guerrero](https://github.com/arenas-guerrero-julian/) - [julian.arenas.guerrero@upm.es](mailto:julian.arenas.guerrero@upm.es)**

*[Universidad Politécnica de Madrid](https://www.upm.es/internacional)*.
