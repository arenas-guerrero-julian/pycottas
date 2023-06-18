# COTTA

[![License](https://img.shields.io/pypi/l/cotta.svg)](https://github.com/arenas-guerrero-julian/cotta/blob/main/LICENSE)
[![Latest PyPI version](https://img.shields.io/pypi/v/cotta?style=flat)](https://pypi.python.org/pypi/cotta)
[![Python Version](https://img.shields.io/pypi/pyversions/cotta.svg)](https://pypi.python.org/pypi/cott)
[![PyPI status](https://img.shields.io:/pypi/status/cotta?)](https://pypi.python.org/pypi/cotta)
[![Documentation Status](https://readthedocs.org/projects/cotta/badge/?version=latest)](https://cotta.readthedocs.io/en/latest/?badge=latest)

**COTTA** is a toolkit for **[RDF-star](https://w3c.github.io/rdf-star/cg-spec/2021-12-17.html)** graph management in **compressed** space. It is based on a triple table representation of [RDF-star](https://w3c.github.io/rdf-star/cg-spec/2021-12-17.html) using the [Apache Parquet](https://parquet.apache.org/) file format. The toolkit provides an **[HDT](https://www.rdfhdt.org/)**-like interface.

## Documentation :bookmark_tabs:

**[Read the documentation](https://cotta.readthedocs.io/en/latest/documentation/)**.

## Getting Started :rocket:

**[PyPi](https://pypi.org/project/cotta/)** is the fastest way to install COTTA:
```bash
pip install cotta
```

We recommend to use **[virtual environments](https://docs.python.org/3/library/venv.html#)** to install COTTA.

### Command line

Compress [RDF-star](https://w3c.github.io/rdf-star/cg-spec/2021-12-17.html):
```bash
python3 -m cotta rdf2cotta file.ttl file.cotta
```

Evaluate a triple pattern over compressed [RDF-star](https://w3c.github.io/rdf-star/cg-spec/2021-12-17.html):
```bash
python3 -m cotta search '<< ?employee <http://ex.com/jobTitle> ?job >> <http://ex.com/accordingTo> <http://ex.com/employee/22>'
```

Uncompress [RDF-star](https://w3c.github.io/rdf-star/cg-spec/2021-12-17.html):
```bash
python3 -m cotta cotta2rdf file.cotta file.nt
```

### Library

```python
import cotta

# compress RDF-star
cotta.rdf_2_cotta('file.ttl', 'file.cotta')

# evaluate triple pattern
tp_df = cotta.search('file.cotta', '<< ?employee <http://ex.com/jobTitle> ?job >> <http://ex.com/accordingTo> <http://ex.com/employee/22>')

# uncompress RDF-star
cotta.rdf_2_cotta('file.cotta', 'file.nt')

# merge two COTTA files
cotta.cat('input_file_1.cotta', 'input_file_2.cotta', 'output.cotta')
```


## License :unlock:

COTTA is available under the **[Apache License 2.0](https://github.com/cotta/cotta/blob/main/LICENSE)**.

## Author & Contact :mailbox_with_mail:

- **[Julián Arenas-Guerrero](https://github.com/arenas-guerrero-julian/) - [julian.arenas.guerrero@upm.es](mailto:julian.arenas.guerrero@upm.es)**  
*[Ontology Engineering Group](https://oeg.fi.upm.es)*, *[Universidad Politécnica de Madrid](https://www.upm.es/internacional)*.