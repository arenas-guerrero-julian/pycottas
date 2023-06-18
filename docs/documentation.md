# Documentation

## Installation

In the following we describe different ways in which you can install COTTA.

### PyPi

**[PyPi](https://pypi.org/project/cotta/)** is the fastest way to install COTTA:
```bash
pip install cotta
```

We recommend to use **[virtual environments](https://docs.python.org/3/library/venv.html#)** to install COTTA.

### From Source

You can also grab the latest source code from the **[GitHub repository](https://github.com/oeg-upm/cotta)**:
```bash
pip install git+https://github.com/oeg-upm/cotta.git
```

## Usage

### Command Line

#### rdf2cotta

Transform an RDF file ([Turtle](https://www.w3.org/TR/turtle/), [N-Triples](https://www.w3.org/TR/n-triples/), [N-Quads](https://www.w3.org/TR/n-quads/) and [RDF/XML](https://www.w3.org/TR/rdf-syntax-grammar/)) into a COTTA file:
```bash
python3 -m cotta rdf2cotta file.nt file.cotta
```

#### cotta2rdf

Transform a COTTA file into an RDF file ([N-Triples](https://www.w3.org/TR/n-triples/), [N-Quads](https://www.w3.org/TR/n-quads/)):
```bash
python3 -m cotta cotta2rdf file.cotta file.cotta
```

#### search

Resolve triple pattern in a COTTA file:
```bash
python3 -m cotta search file.cotta "? <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> ?"
```

#### cat

Merge two COTTA files:
```bash
python3 -m cotta cat input_graph_1.cotta input_graph_2.cotta output_file.cotta
```

#### diff

Substract a COTTA file from another one:
```bash
python3 -m cotta diff input_graph_1.cotta input_graph_2.cotta output_file.cotta
```

#### info

Retrieve basic information and statistics from a COTTA file:
```bash
python3 -m cotta info file.cotta
```

#### verify

Check if a COTTA file is correct:
```bash
python3 -m cotta verify file.cotta
```

### Library

Import COTTA:
```python
import cotta
```

#### rdf_2_cotta

**`rdf_2_cotta(rdf_file, cotta_file)`**

#### cotta_2_rdf

**`cotta_2_rdf(cotta_file, rdf_file)`**

#### search

**`search(cotta_file, triple_pattern, results_file=None)`**

#### cat

**`cat(cotta_file_1, cotta_file_2, cotta_cat_file)`**

#### diff

**`diff(cotta_file_1, cotta_file_2, cotta_diff_file)`**

#### info

**`info(cotta_file)`**

#### verify

**`verify(cotta_file)`**



![OEG](assets/logo-oeg.png){ width="150" align=left } ![UPM](assets/logo-upm.png){ width="161" align=right }
