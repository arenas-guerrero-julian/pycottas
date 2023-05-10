# COTTA

**COTTA** is a toolkit for efficient **RDF** graph management. It is based on a triple table representation of RDF using the [Apache Parquet](https://parquet.apache.org/) file format. The toolkit provides an [HDT](https://www.rdfhdt.org/)-like interface.

## Tutorial :woman_teacher:

```
TODO: tutorial on google colab.
```

## Getting Started :rocket:

### Installation

**[PyPi](https://pypi.org/project/cotta/)** is the fastest way to install COTTA:
```bash
pip install cotta
```

We recommend to use **[virtual environments](https://docs.python.org/3/library/venv.html#)** to install COTTA.

### Command line

Transform an RDF file ([Turtle](https://www.w3.org/TR/turtle/), [N-Triples](https://www.w3.org/TR/n-triples/), [N-Quads](https://www.w3.org/TR/n-quads/) and [RDF/XML](https://www.w3.org/TR/rdf-syntax-grammar/)) into a COTTA file:
```bash
python3 -m cotta rdf2cotta graph.nt graph.cotta
```

Transform a COTTA file into an RDF file ([N-Triples](https://www.w3.org/TR/n-triples/), [N-Quads](https://www.w3.org/TR/n-quads/)):
```bash
python3 -m cotta cotta2rdf graph.cotta graph.cotta
```

Resolve triple pattern in a COTTA file:
```bash
python3 -m cotta cottaSearch graph.cotta "? <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> ?"
```

Merge two COTTA files:
```bash
python3 -m cotta cottaCat input_graph_1.cotta input_graph_2.cotta output_graph.cotta
```

Substract a COTTA file from another one:
```bash
python3 -m cotta cottaDiff input_graph_1.cotta input_graph_2.cotta output_graph.cotta
```

Check if a COTTA file is correct:
```bash
python3 -m cotta cottaVerify graph.cotta
```

Retrieve basic information and statistics from a COTTA file:
```bash
python3 -m cotta cottaInfo graph.cotta
```

### Library

## License :unlock:

COTTA is available under the **[Apache License 2.0](https://github.com/morph-kgc/morph-kgc/blob/main/LICENSE)**.

## Author & Contact :mailbox_with_mail:

- **[Julián Arenas-Guerrero](https://github.com/arenas-guerrero-julian/) - [julian.arenas.guerrero@upm.es](mailto:julian.arenas.guerrero@upm.es)**  
*[Ontology Engineering Group](https://oeg.fi.upm.es)*, *[Universidad Politécnica de Madrid](https://www.upm.es/internacional)*.