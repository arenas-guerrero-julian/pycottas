- Rename table `quads` to `STT`

# pycottas

[![License](https://img.shields.io/pypi/l/pycottas.svg)](https://github.com/arenas-guerrero-julian/cottas/blob/main/LICENSE)
[![Latest PyPI version](https://img.shields.io/pypi/v/cottas?style=flat)](https://pypi.python.org/pypi/cottas)
[![Python Version](https://img.shields.io/pypi/pyversions/cottas.svg)](https://pypi.python.org/pypi/cott)
[![PyPI status](https://img.shields.io:/pypi/status/cottas?)](https://pypi.python.org/pypi/cottas)
[![Documentation Status](https://readthedocs.org/projects/cottas/badge/?version=latest)](https://cottas.readthedocs.io/en/latest/?badge=latest)

**pycottas** is a toolkit for **[RDF-star](https://w3c.github.io/rdf-star/cg-spec/2021-12-17.html)** graph management in **compressed** space. It is based on a triple table representation of [RDF-star](https://w3c.github.io/rdf-star/cg-spec/2021-12-17.html) using the [Apache Parquet](https://parquet.apache.org/) file format. The toolkit provides an **[HDT](https://www.rdfhdt.org/)**-like interface.

## Documentation :bookmark_tabs:

**[Read the documentation](https://pycottas.readthedocs.io/en/latest/documentation/)**.

## Getting Started :rocket:

**[PyPi](https://pypi.org/project/pycottas/)** is the fastest way to install pycottas:
```bash
pip install pycottas
```

We recommend to use **[virtual environments](https://docs.python.org/3/library/venv.html#)** to install pycottas.

### Command line

Compress [RDF-star](https://w3c.github.io/rdf-star/cg-spec/2021-12-17.html):
```bash
python3 -m pycottas rdf2cottas file.ttl file.cottas
```

Evaluate a [triple pattern](https://w3c.github.io/rdf-star/cg-spec/2021-12-17.html#dfn-triple-star-pattern) over compressed [RDF-star](https://w3c.github.io/rdf-star/cg-spec/2021-12-17.html):
```bash
python3 -m pycottas search file.cottas '<< ?employee <http://ex.com/jobTitle> ?job >> <http://ex.com/accordingTo> <http://ex.com/employee/22>'
```

Uncompress [RDF-star](https://w3c.github.io/rdf-star/cg-spec/2021-12-17.html):
```bash
python3 -m pycottas cottas2rdf file.cottas file.nt
```

### Library

```python
import pycottas

# compress RDF-star
pycottas.rdf_2_cottas('file.ttl', 'file.cottas')

# evaluate triple pattern
tp_df = pycottas.search('file.cottas', '<< ?employee <http://ex.com/jobTitle> ?job >> <http://ex.com/accordingTo> <http://ex.com/employee/22>')

# uncompress RDF-star
pycottas.cottas_2_rdf('file.cottas', 'file.nt')

# merge two COTTAS files
pycottas.cat('input_file_1.cottas', 'input_file_2.cottas', 'output.cottas')
```

## License :unlock:

**pycottas** is available under the **[Apache License 2.0](https://github.com/cottas/cottas/blob/main/LICENSE)**.

## Author & Contact :mailbox_with_mail:

- **[Julián Arenas-Guerrero](https://github.com/arenas-guerrero-julian/) - [julian.arenas.guerrero@upm.es](mailto:julian.arenas.guerrero@upm.es)**

*[Universidad Politécnica de Madrid](https://www.upm.es/internacional)*.
