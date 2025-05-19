# Documentation

## Installation

In the following we describe different ways in which you can install pycottas.

### PyPI

**[PyPI](https://pypi.org/project/pycottas/)** is the fastest way to install pycottas.
```bash
pip install pycottas
```

We recommend to use **[virtual environments](https://docs.python.org/3/library/venv.html#)** to install pycottas.

### From Source

You can also grab the latest source code from the **[GitHub repository](https://github.com/arenas-guerrero-julian/pycottas)**.
```bash
pip install git+https://github.com/arenas-guerrero-julian/pycottas.git
```

## Usage

pycottas can be executed from the command line or as a library. In the following it is described how to use pycottas with both alternatives.

### Library

#### rdf2cottas

#### cottas2rdf

#### search

#### cat

#### diff

#### info

#### verify

### RDFLib Store

#### COTTASStore

`{++pycottas.COTTASStore(path)++}`

`**Parameters:**`
* **path : str**
  
  Path to the COTTAS file.

### Command Line

To execute COTTAS from the command line, it is necessary to call the `pycottas` package, specifying the pycottas operation to perform (`rdf2cottas`, `search`, `cat`, etc.), and providing a set of parameters.

```bash
$ python3 -m pycottas -h

usage: pycottas {rdf2cottas,cottas2rdf,search,info,verify,cat,diff} ...

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
```

#### rdf2cottas

```bash
$ python3 -m pycottas rdf2cottas -h

usage: pycottas rdf2cottas -r RDF_FILE -c COTTAS_FILE [-i INDEX]

options:
  -r RDF_FILE, --rdf_file RDF_FILE
                        Path to RDF file
  -c COTTAS_FILE, --cottas_file COTTAS_FILE
                        Path to COTTAS file
  -i INDEX, --index INDEX
                        Zonemap index, e.g.: `SPO`, `PSO`, `GPOS`
```

#### cottas2rdf

```bash
$ python3 -m pycottas cottas2rdf -h

usage: pycottas cottas2rdf -c COTTAS_FILE -r RDF_FILE

options:
  -c COTTAS_FILE, --cottas_file COTTAS_FILE
                        Path to COTTAS file
  -r RDF_FILE, --rdf_file RDF_FILE
                        Path to RDF file (N-Triples)
```

#### search

```bash
$ python3 -m pycottas search -h

usage: pycottas search -c COTTAS_FILE -t TRIPLE_PATTERN [-r {table,tuples,to_csv}]

options:
  -c COTTAS_FILE, --cottas_file COTTAS_FILE
                        Path to COTTAS file
  -t TRIPLE_PATTERN, --triple_pattern TRIPLE_PATTERN
                        Triple pattern, e.g., `?s <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> ?o`
  -r {table,tuples,to_csv}, --result_option {table,tuples,to_csv}
                        What to do with the result set
```

#### info

```bash
$ python3 -m pycottas info -h

usage: pycottas info -c COTTAS_FILE

options:
  -c COTTAS_FILE, --cottas_file COTTAS_FILE
                        Path to COTTAS file
```

#### verify

```bash
$ python3 -m pycottas verify -h

usage: pycottas verify -c COTTAS_FILE

options:
  -c COTTAS_FILE, --cottas_file COTTAS_FILE
                        Path to COTTAS file
```

#### cat

```bash
$ python3 -m pycottas cat -h

usage: pycottas cat --input_cottas_files INPUT_COTTAS_FILES [INPUT_COTTAS_FILES ...] --output_cottas_file OUTPUT_COTTAS_FILE [-i INDEX] [-r REMOVE_INPUT_FILES]

options:
  --input_cottas_files INPUT_COTTAS_FILES [INPUT_COTTAS_FILES ...]
                        Path of the input COTTAS files
  --output_cottas_file OUTPUT_COTTAS_FILE
                        Path of the output COTTAS file
  -i INDEX, --index INDEX
                        Zonemap index, e.g.: `SPO`, `PSO`, `GPOS`
  -r REMOVE_INPUT_FILES, --remove_input_files REMOVE_INPUT_FILES
                        Whether to remove input COTTAS files after merging
```

#### diff

```bash
$ python3 -m pycottas diff -h

usage: pycottas diff -c COTTAS_FILE -s SUBTRACT_COTTAS_FILE -o OUTPUT_COTTAS_FILE [-i INDEX] [-r REMOVE_INPUT_FILES]

options:
  -c COTTAS_FILE, --cottas_file COTTAS_FILE
                        Path to the COTTAS file
  -s SUBTRACT_COTTAS_FILE, --subtract_cottas_file SUBTRACT_COTTAS_FILE
                        Path to the COTTAS file to subtract
  -o OUTPUT_COTTAS_FILE, --output_cottas_file OUTPUT_COTTAS_FILE
                        Path to the output COTTAS file
  -i INDEX, --index INDEX
                        Zonemap index, e.g.: `SPO`, `PSO`, `GPOS`
  -r REMOVE_INPUT_FILES, --remove_input_files REMOVE_INPUT_FILES
                        Whether to remove the input COTTAS files after merging
```

### Tricks


![OEG](assets/logo-oeg.png){ width="150" align=left } ![UPM](assets/logo-upm.png){ width="161" align=right }
