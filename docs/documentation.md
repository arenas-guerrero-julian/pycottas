# Documentation

## Installation

In the following we describe different ways in which you can install COTTAS.

### PyPi

**[PyPi](https://pypi.org/project/cottas/)** is the fastest way to install COTTAS.
```bash
pip install cottas
```

We recommend to use **[virtual environments](https://docs.python.org/3/library/venv.html#)** to install COTTAS.

### From Source

You can also grab the latest source code from the **[GitHub repository](https://github.com/arenas-guerrero-julian/cottas)**.
```bash
pip install git+https://github.com/arenas-guerrero-julian/cottas.git
```

## Usage

COTTAS can be executed from the command line or as a library. In the following it is described how to use COTTAS with both alternatives.

### Command Line

To execute COTTAS from the command line, it is necessary to call the `cottas` package, specifying the COTTAS operation to perform (rdf2cottas, search, cat, etc.), and providing a set of parameters.

#### rdf2cottas

Compress an [RDF-star](https://w3c.github.io/rdf-star/cg-spec/2021-12-17.html) file ([Turtle](https://www.w3.org/TR/turtle/), [N-Triples](https://www.w3.org/TR/n-triples/), [N-Quads](https://www.w3.org/TR/n-quads/), [RDF/XML](https://www.w3.org/TR/rdf-syntax-grammar/)) into a COTTAS file.
```bash
python3 -m cottas rdf2cottas file.ttl file.cottas
```

#### rdf2cottasNoID

Compress an [RDF-star](https://w3c.github.io/rdf-star/cg-spec/2021-12-17.html) file ([Turtle](https://www.w3.org/TR/turtle/), [N-Triples](https://www.w3.org/TR/n-triples/), [N-Quads](https://www.w3.org/TR/n-quads/), [RDF/XML](https://www.w3.org/TR/rdf-syntax-grammar/)) into a COTTAS file without **id** column. This achieves better compression ratio than creating the **id** column (with `rdf2cottas`), but it does not allow the evaluation of [triple patterns](https://w3c.github.io/rdf-star/cg-spec/2021-12-17.html#dfn-triple-star-pattern) with [quoted triples](https://w3c.github.io/rdf-star/cg-spec/2021-12-17.html#dfn-quoted).
```bash
python3 -m cottas rdf2cottasNoID file.ttl file.cottas
```

#### cottas2rdf

Uncompress a COTTAS file into an [RDF-star](https://w3c.github.io/rdf-star/cg-spec/2021-12-17.html) file ([N-Triples](https://www.w3.org/TR/n-triples/), [N-Quads](https://www.w3.org/TR/n-quads/)).
```bash
python3 -m cottas cottas2rdf file.cottas file.nt
```

#### search

Evaluate a [triple pattern](https://w3c.github.io/rdf-star/cg-spec/2021-12-17.html#dfn-triple-star-pattern) over a COTTAS file.
```bash
python3 -m cottas search file.cottas '<< ?employee <http://ex.com/jobTitle> ?job >> <http://ex.com/accordingTo> <http://ex.com/employee/22>'
```

#### cat

Merge two COTTAS files into a new COTTAS file.
```bash
python3 -m cottas cat input_file_1.cottas input_file_2.cottas output_file.cottas
```

#### diff

Substract a COTTAS file from another one into a new COTTAS file.
```bash
python3 -m cottas diff input_file_1.cottas input_file_2.cottas output_file.cottas
```

#### info

Retrieve basic information and statistics from a COTTAS file.
```bash
python3 -m cottas info file.cottas
```

#### verify

Check if a COTTAS file is correct.
```bash
python3 -m cottas verify file.cottas
```

#### createID

Add the **id** column to a COTTAS file. This increases the size of the COTTAS file, but it is necessary to evaluate [triple patterns](https://w3c.github.io/rdf-star/cg-spec/2021-12-17.html#dfn-triple-star-pattern) with [quoted triples](https://w3c.github.io/rdf-star/cg-spec/2021-12-17.html#dfn-quoted).
```bash
python3 -m cottas createID file.cottas
```

#### removeID

Remove the **id** column from a COTTAS file. This reduces the size of the COTTAS file, but the  evaluation of [triple patterns](https://w3c.github.io/rdf-star/cg-spec/2021-12-17.html#dfn-triple-star-pattern) with [quoted triples](https://w3c.github.io/rdf-star/cg-spec/2021-12-17.html#dfn-quoted) is not possible.
```bash
python3 -m cottas removeID file.cottas
```

### Library

Import COTTAS.
```python
import cottas
```

#### cottas.rdf_2_cottas

**`cottas.rdf_2_cottas(rdf_file, cottas_file, create_id=True, in_memory=True)`**

Compress an [RDF-star](https://w3c.github.io/rdf-star/cg-spec/2021-12-17.html) file ([Turtle](https://www.w3.org/TR/turtle/), [N-Triples](https://www.w3.org/TR/n-triples/), [N-Quads](https://www.w3.org/TR/n-quads/), [RDF/XML](https://www.w3.org/TR/rdf-syntax-grammar/)) into a COTTAS file.

* _**rdf_file**_: ([str](https://docs.python.org/3/library/stdtypes.html#str)) Path to the input [RDF-star](https://w3c.github.io/rdf-star/cg-spec/2021-12-17.html) file.
* _**cottas_file**_: ([str](https://docs.python.org/3/library/stdtypes.html#str)) Path to the output COTTAS file.
* _**create_id**_: ([bool](https://docs.python.org/3/library/stdtypes.html#bltin-boolean-values), default _True_) If _True_, the **id** column will be included in the COTTAS file. Creating the **id** column results in larger COTTAS files, but it enables the evaluation of [triple patterns](https://w3c.github.io/rdf-star/cg-spec/2021-12-17.html#dfn-triple-star-pattern) with [quoted triples](https://w3c.github.io/rdf-star/cg-spec/2021-12-17.html#dfn-quoted).
* _**in_memory**_: ([bool](https://docs.python.org/3/library/stdtypes.html#bltin-boolean-values), default _True_) If _True_, computations will be done in-memory, otherwise temporary files are created in the system (reducing memory consumption).

#### cottas.cottas_2_rdf

**`cottas.cottas_2_rdf(cottas_file, rdf_file, in_memory=True)`**

Uncompress a COTTAS file into an [RDF-star](https://w3c.github.io/rdf-star/cg-spec/2021-12-17.html) file ([N-Triples](https://www.w3.org/TR/n-triples/), [N-Quads](https://www.w3.org/TR/n-quads/)).

* _**cottas_file**_: ([str](https://docs.python.org/3/library/stdtypes.html#str)) Path to the input COTTAS file.
* _**rdf_file**_: ([str](https://docs.python.org/3/library/stdtypes.html#str)) Path to the output [RDF-star](https://w3c.github.io/rdf-star/cg-spec/2021-12-17.html) file.
* _**in_memory**_: ([bool](https://docs.python.org/3/library/stdtypes.html#bltin-boolean-values), default _True_) If _True_, computations will be done in-memory, otherwise temporary files are created in the system (reducing memory consumption).

#### cottas.search

**`cottas.search(cottas_file, triple_pattern)`**

Evaluate a [triple pattern](https://w3c.github.io/rdf-star/cg-spec/2021-12-17.html#dfn-triple-star-pattern) over a COTTAS file, returning a [DataFrame](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html).

* _**cottas_file**_: ([str](https://docs.python.org/3/library/stdtypes.html#str)) Path to the input COTTAS file.
* _**triple_pattern**_: ([str](https://docs.python.org/3/library/stdtypes.html#str)) [Triple pattern](https://w3c.github.io/rdf-star/cg-spec/2021-12-17.html#dfn-triple-star-pattern) to evaluate, e.g., '*<< ?employee \<http://ex.com/jobTitle> ?job >> \<http://ex.com/accordingTo> \<http://ex.com/employee/22>*'.

#### cottas.cat

**`cottas.cat(cottas_file_1, cottas_file_2, cottas_cat_file, in_memory=True)`**

Merge two COTTAS files into a new COTTAS file.

* _**cottas_file_1**_: ([str](https://docs.python.org/3/library/stdtypes.html#str)) Path to an input COTTAS file.
* _**cottas_file_2**_: ([str](https://docs.python.org/3/library/stdtypes.html#str)) Path to an input COTTAS file.
* _**cottas_cat_file**_: ([str](https://docs.python.org/3/library/stdtypes.html#str)) Path to the merged output COTTAS file.
* _**in_memory**_: ([bool](https://docs.python.org/3/library/stdtypes.html#bltin-boolean-values), default _True_) If _True_, computations will be done in-memory, otherwise temporary files are created in the system (reducing memory consumption).

#### cottas.diff

**`cottas.diff(cottas_file_1, cottas_file_2, cottas_diff_file, in_memory=True)`**

Substract a COTTAS file from another one into a new COTTAS file.

* _**cottas_file_1**_: ([str](https://docs.python.org/3/library/stdtypes.html#str)) Path to an input COTTAS file.
* _**cottas_file_2**_: ([str](https://docs.python.org/3/library/stdtypes.html#str)) Path to an input COTTAS file.
* _**cottas_diff_file**_: ([str](https://docs.python.org/3/library/stdtypes.html#str)) Path to the diff output COTTAS file.
* _**in_memory**_: ([bool](https://docs.python.org/3/library/stdtypes.html#bltin-boolean-values), default _True_) If _True_, computations will be done in-memory, otherwise temporary files are created in the system (reducing memory consumption).

#### cottas.info

**`cottas.info(cottas_file)`**

Retrieve basic information and statistics from a COTTAS file, returning an [RDF](https://www.w3.org/TR/rdf11-concepts/) [string](https://docs.python.org/3/library/stdtypes.html#str).

* _**cottas_file**_: ([str](https://docs.python.org/3/library/stdtypes.html#str)) Path to the input COTTAS file.

#### cottas.verify

**`cottas.verify(cottas_file)`**

Check if a COTTAS file is correct, returning a [boolean](https://docs.python.org/3/library/stdtypes.html#bltin-boolean-values).

* _**cottas_file**_: ([str](https://docs.python.org/3/library/stdtypes.html#str)) Path to the input COTTAS file.

#### cottas.create_id

**`cottas.create_id(cottas_file, in_memory=True)`**

Add the **id** column to a COTTAS file. This increases the size of the COTTAS file, but it is necessary to evaluate [triple patterns](https://w3c.github.io/rdf-star/cg-spec/2021-12-17.html#dfn-triple-star-pattern) with [quoted triples](https://w3c.github.io/rdf-star/cg-spec/2021-12-17.html#dfn-quoted).

* _**cottas_file**_: ([str](https://docs.python.org/3/library/stdtypes.html#str)) Path to the input/output COTTAS file.
* _**in_memory**_: ([bool](https://docs.python.org/3/library/stdtypes.html#bltin-boolean-values), default _True_) If _True_, computations will be done in-memory, otherwise temporary files are created in the system (reducing memory consumption).

#### cottas.remove_id

**`cottas.remove_id(cottas_file, in_memory=True)`**

Remove the **id** column from a COTTAS file. This reduces the size of the COTTAS file, but the  evaluation of [triple patterns](https://w3c.github.io/rdf-star/cg-spec/2021-12-17.html#dfn-triple-star-pattern) with [quoted triples](https://w3c.github.io/rdf-star/cg-spec/2021-12-17.html#dfn-quoted) is not possible.

* _**cottas_file**_: ([str](https://docs.python.org/3/library/stdtypes.html#str)) Path to the input/output COTTAS file.
* _**in_memory**_: ([bool](https://docs.python.org/3/library/stdtypes.html#bltin-boolean-values), default _True_) If _True_, computations will be done in-memory, otherwise temporary files are created in the system (reducing memory consumption).


![OEG](assets/logo-oeg.png){ width="150" align=left } ![UPM](assets/logo-upm.png){ width="161" align=right }
