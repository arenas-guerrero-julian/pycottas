# Documentation

## Installation

In the following we describe different ways in which you can install COTTA.

### PyPi

**[PyPi](https://pypi.org/project/cotta/)** is the fastest way to install COTTA.
```bash
pip install cotta
```

We recommend to use **[virtual environments](https://docs.python.org/3/library/venv.html#)** to install COTTA.

### From Source

You can also grab the latest source code from the **[GitHub repository](https://github.com/arenas-guerrero-julian/cotta)**.
```bash
pip install git+https://github.com/arenas-guerrero-julian/cotta.git
```

## Usage

### Command Line

#### rdf2cotta

Transform an [RDF-star](https://w3c.github.io/rdf-star/cg-spec/2021-12-17.html) file ([Turtle](https://www.w3.org/TR/turtle/), [N-Triples](https://www.w3.org/TR/n-triples/), [N-Quads](https://www.w3.org/TR/n-quads/), [RDF/XML](https://www.w3.org/TR/rdf-syntax-grammar/)) into a COTTA file.
```bash
python3 -m cotta rdf2cotta file.nt file.cotta
```

#### rdf2cottaNoID

Transform an [RDF-star](https://w3c.github.io/rdf-star/cg-spec/2021-12-17.html) file ([Turtle](https://www.w3.org/TR/turtle/), [N-Triples](https://www.w3.org/TR/n-triples/), [N-Quads](https://www.w3.org/TR/n-quads/), [RDF/XML](https://www.w3.org/TR/rdf-syntax-grammar/)) into a COTTA file without **id** column. This achieves better compression ratio than creating the **id** column (with `rdf2cotta`), but it does not allow the resolution of [triple patterns](https://w3c.github.io/rdf-star/cg-spec/2021-12-17.html#dfn-triple-star-pattern) with [quoted triples](https://w3c.github.io/rdf-star/cg-spec/2021-12-17.html#dfn-quoted).
```bash
python3 -m cotta rdf2cottaNoID file.nt file.cotta
```

#### cotta2rdf

Transform a COTTA file into an [RDF-star](https://w3c.github.io/rdf-star/cg-spec/2021-12-17.html) file ([N-Triples](https://www.w3.org/TR/n-triples/), [N-Quads](https://www.w3.org/TR/n-quads/)).
```bash
python3 -m cotta cotta2rdf file.cotta file.nt
```

#### search

Evaluate a [triple pattern](https://w3c.github.io/rdf-star/cg-spec/2021-12-17.html#dfn-triple-star-pattern) over a COTTA file:
```bash
python3 -m cotta search file.cotta '<< ?employee <http://ex.com/jobTitle> ?job >> <http://ex.com/accordingTo> <http://ex.com/employee/22>'
```

#### cat

Merge two COTTA files into a new COTTA file.
```bash
python3 -m cotta cat input_file_1.cotta input_file_2.cotta output_file.cotta
```

#### diff

Substract a COTTA file from another one into a new COTTA file.
```bash
python3 -m cotta diff input_file_1.cotta input_file_2.cotta output_file.cotta
```

#### info

Retrieve basic information and statistics from a COTTA file.
```bash
python3 -m cotta info file.cotta
```

#### verify

Check if a COTTA file is correct.
```bash
python3 -m cotta verify file.cotta
```

#### createID

Compute the **id** column of a COTTA file. This increases the size of the COTTA file, but it is necessary to evaluate [triple patterns](https://w3c.github.io/rdf-star/cg-spec/2021-12-17.html#dfn-triple-star-pattern) with [quoted triples](https://w3c.github.io/rdf-star/cg-spec/2021-12-17.html#dfn-quoted).
```bash
python3 -m cotta createID file.cotta
```

#### removeID

Remove the **id** column of a COTTA file. This reduces the size of the COTTA file, but the  evaluation of [triple patterns](https://w3c.github.io/rdf-star/cg-spec/2021-12-17.html#dfn-triple-star-pattern) with [quoted triples](https://w3c.github.io/rdf-star/cg-spec/2021-12-17.html#dfn-quoted) is not possible.
```bash
python3 -m cotta removeID file.cotta
```

### Library

Import COTTA:
```python
import cotta
```

#### rdf_2_cotta

**`rdf_2_cotta(rdf_file, cotta_file, create_id=True, in_memory=True)`**

#### cotta_2_rdf

**`cotta_2_rdf(cotta_file, rdf_file, in_memory=True)`**

#### search

**`search(cotta_file, triple_pattern)`**

#### cat

**`cat(cotta_file_1, cotta_file_2, cotta_cat_file, in_memory=True)`**

#### diff

**`diff(cotta_file_1, cotta_file_2, cotta_diff_file, in_memory=True)`**

#### info

**`info(cotta_file)`**

#### verify

**`verify(cotta_file)`**

#### create_id

**`create_id(cotta_file, in_memory=True)`**

#### remove_id

**`remove_id(cotta_file, in_memory=True)`**


![OEG](assets/logo-oeg.png){ width="150" align=left } ![UPM](assets/logo-upm.png){ width="161" align=right }
