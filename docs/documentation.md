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

Compress an [RDF-star](https://w3c.github.io/rdf-star/cg-spec/2021-12-17.html) file ([Turtle](https://www.w3.org/TR/turtle/), [N-Triples](https://www.w3.org/TR/n-triples/), [N-Quads](https://www.w3.org/TR/n-quads/), [RDF/XML](https://www.w3.org/TR/rdf-syntax-grammar/)) into a COTTA file.
```bash
python3 -m cotta rdf2cotta file.nt file.cotta
```

#### rdf2cottaNoID

Compress an [RDF-star](https://w3c.github.io/rdf-star/cg-spec/2021-12-17.html) file ([Turtle](https://www.w3.org/TR/turtle/), [N-Triples](https://www.w3.org/TR/n-triples/), [N-Quads](https://www.w3.org/TR/n-quads/), [RDF/XML](https://www.w3.org/TR/rdf-syntax-grammar/)) into a COTTA file without **id** column. This achieves better compression ratio than creating the **id** column (with `rdf2cotta`), but it does not allow the evaluation of [triple patterns](https://w3c.github.io/rdf-star/cg-spec/2021-12-17.html#dfn-triple-star-pattern) with [quoted triples](https://w3c.github.io/rdf-star/cg-spec/2021-12-17.html#dfn-quoted).
```bash
python3 -m cotta rdf2cottaNoID file.nt file.cotta
```

#### cotta2rdf

Uncompress a COTTA file into an [RDF-star](https://w3c.github.io/rdf-star/cg-spec/2021-12-17.html) file ([N-Triples](https://www.w3.org/TR/n-triples/), [N-Quads](https://www.w3.org/TR/n-quads/)).
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

Add the **id** column to a COTTA file. This increases the size of the COTTA file, but it is necessary to evaluate [triple patterns](https://w3c.github.io/rdf-star/cg-spec/2021-12-17.html#dfn-triple-star-pattern) with [quoted triples](https://w3c.github.io/rdf-star/cg-spec/2021-12-17.html#dfn-quoted).
```bash
python3 -m cotta createID file.cotta
```

#### removeID

Remove the **id** column from a COTTA file. This reduces the size of the COTTA file, but the  evaluation of [triple patterns](https://w3c.github.io/rdf-star/cg-spec/2021-12-17.html#dfn-triple-star-pattern) with [quoted triples](https://w3c.github.io/rdf-star/cg-spec/2021-12-17.html#dfn-quoted) is not possible.
```bash
python3 -m cotta removeID file.cotta
```

### Library

Import COTTA:
```python
import cotta
```

#### cotta.rdf_2_cotta

**`cotta.rdf_2_cotta(rdf_file, cotta_file, create_id=True, in_memory=True)`**

Compress an [RDF-star](https://w3c.github.io/rdf-star/cg-spec/2021-12-17.html) file ([Turtle](https://www.w3.org/TR/turtle/), [N-Triples](https://www.w3.org/TR/n-triples/), [N-Quads](https://www.w3.org/TR/n-quads/), [RDF/XML](https://www.w3.org/TR/rdf-syntax-grammar/)) into a COTTA file.

* _**rdf_file**_: ([str](https://docs.python.org/3/library/stdtypes.html#str)) Path to the input [RDF-star](https://w3c.github.io/rdf-star/cg-spec/2021-12-17.html) file.
* _**cotta_file**_: ([str](https://docs.python.org/3/library/stdtypes.html#str)) Path to the output COTTA file.
* _**create_id**_: ([bool](https://docs.python.org/3/library/stdtypes.html#bltin-boolean-values), default _True_) If _True_, the **id** column will be included in the COTTA file. Creating the **id** column results in larger COTTA files, but it enables the evaluation of [triple patterns](https://w3c.github.io/rdf-star/cg-spec/2021-12-17.html#dfn-triple-star-pattern) with [quoted triples](https://w3c.github.io/rdf-star/cg-spec/2021-12-17.html#dfn-quoted).
* _**in_memory**_: ([bool](https://docs.python.org/3/library/stdtypes.html#bltin-boolean-values), default _True_) If _True_, computations will be done in-memory, otherwise temporary files are created in the system (reducing memory consumption).

#### cotta.cotta_2_rdf

**`cotta.cotta_2_rdf(cotta_file, rdf_file, in_memory=True)`**

Uncompress a COTTA file into an [RDF-star](https://w3c.github.io/rdf-star/cg-spec/2021-12-17.html) file ([N-Triples](https://www.w3.org/TR/n-triples/), [N-Quads](https://www.w3.org/TR/n-quads/)).

* _**cotta_file**_: ([str](https://docs.python.org/3/library/stdtypes.html#str)) Path to the input COTTA file.
* _**rdf_file**_: ([str](https://docs.python.org/3/library/stdtypes.html#str)) Path to the output [RDF-star](https://w3c.github.io/rdf-star/cg-spec/2021-12-17.html) file.
* _**in_memory**_: ([bool](https://docs.python.org/3/library/stdtypes.html#bltin-boolean-values), default _True_) If _True_, computations will be done in-memory, otherwise temporary files are created in the system (reducing memory consumption).

#### cotta.search

**`cotta.search(cotta_file, triple_pattern)`**

Evaluate a [triple pattern](https://w3c.github.io/rdf-star/cg-spec/2021-12-17.html#dfn-triple-star-pattern) over a COTTA file, returning a [DataFrame](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html).

* _**cotta_file**_: ([str](https://docs.python.org/3/library/stdtypes.html#str)) Path to the input COTTA file.
* _**triple_pattern**_: ([str](https://docs.python.org/3/library/stdtypes.html#str)) [Triple pattern](https://w3c.github.io/rdf-star/cg-spec/2021-12-17.html#dfn-triple-star-pattern) to evaluate.

#### cotta.cat

**`cotta.cat(cotta_file_1, cotta_file_2, cotta_cat_file, in_memory=True)`**

Merge two COTTA files into a new COTTA file.

* _**cotta_file_1**_: ([str](https://docs.python.org/3/library/stdtypes.html#str)) Path to an input COTTA file.
* _**cotta_file_2**_: ([str](https://docs.python.org/3/library/stdtypes.html#str)) Path to an input COTTA file.
* _**cotta_cat_file**_: ([str](https://docs.python.org/3/library/stdtypes.html#str)) Path to the output merged COTTA file.
* _**in_memory**_: ([bool](https://docs.python.org/3/library/stdtypes.html#bltin-boolean-values), default _True_) If _True_, computations will be done in-memory, otherwise temporary files are created in the system (reducing memory consumption).

#### cotta.diff

**`cotta.diff(cotta_file_1, cotta_file_2, cotta_diff_file, in_memory=True)`**

Substract a COTTA file from another one into a new COTTA file.

* _**cotta_file_1**_: ([str](https://docs.python.org/3/library/stdtypes.html#str)) Path to an input COTTA file.
* _**cotta_file_2**_: ([str](https://docs.python.org/3/library/stdtypes.html#str)) Path to an input COTTA file.
* _**cotta_diff_file**_: ([str](https://docs.python.org/3/library/stdtypes.html#str)) Path to the output diff COTTA file.
* _**in_memory**_: ([bool](https://docs.python.org/3/library/stdtypes.html#bltin-boolean-values), default _True_) If _True_, computations will be done in-memory, otherwise temporary files are created in the system (reducing memory consumption).

#### cotta.info

**`cotta.info(cotta_file)`**

Retrieve basic information and statistics from a COTTA file, returning an [RDF](https://www.w3.org/TR/rdf11-concepts/) [string](https://docs.python.org/3/library/stdtypes.html#str).

* _**cotta_file**_: ([str](https://docs.python.org/3/library/stdtypes.html#str)) Path to the input COTTA file.

#### cotta.verify

**`cotta.verify(cotta_file)`**

Check if a COTTA file is correct, returning a [boolean](https://docs.python.org/3/library/stdtypes.html#bltin-boolean-values).

* _**cotta_file**_: ([str](https://docs.python.org/3/library/stdtypes.html#str)) Path to the input COTTA file.

#### cotta.create_id

**`creatcotta._id(cotta_file, in_memory=True)`**

Add the **id** column to a COTTA file. This increases the size of the COTTA file, but it is necessary to evaluate [triple patterns](https://w3c.github.io/rdf-star/cg-spec/2021-12-17.html#dfn-triple-star-pattern) with [quoted triples](https://w3c.github.io/rdf-star/cg-spec/2021-12-17.html#dfn-quoted).

* _**cotta_file**_: ([str](https://docs.python.org/3/library/stdtypes.html#str)) Path to the input/output COTTA file.
* _**in_memory**_: ([bool](https://docs.python.org/3/library/stdtypes.html#bltin-boolean-values), default _True_) If _True_, computations will be done in-memory, otherwise temporary files are created in the system (reducing memory consumption).

#### cotta.remove_id

**`cotta.remove_id(cotta_file, in_memory=True)`**

Remove the **id** column from a COTTA file. This reduces the size of the COTTA file, but the  evaluation of [triple patterns](https://w3c.github.io/rdf-star/cg-spec/2021-12-17.html#dfn-triple-star-pattern) with [quoted triples](https://w3c.github.io/rdf-star/cg-spec/2021-12-17.html#dfn-quoted) is not possible.

* _**cotta_file**_: ([str](https://docs.python.org/3/library/stdtypes.html#str)) Path to the input/output COTTA file.
* _**in_memory**_: ([bool](https://docs.python.org/3/library/stdtypes.html#bltin-boolean-values), default _True_) If _True_, computations will be done in-memory, otherwise temporary files are created in the system (reducing memory consumption).


![OEG](assets/logo-oeg.png){ width="150" align=left } ![UPM](assets/logo-upm.png){ width="161" align=right }
