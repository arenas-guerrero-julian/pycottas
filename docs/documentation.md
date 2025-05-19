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

## API reference

### General Functions

#### rdf2cottas

`{++pycottas.rdf2cottas(rdf_file_path, cottas_file_path, index='spo')++}`

Compress an RDF file in plain text format to COTTAS. The compressed file is indexed for efficient querying.

**`Parameters:`**

* **rdf_file_path : *str***
  
    Path to the input RDF file. Supported formats:  N-Triples, N-Quads, Turtle, TriG, N3, and RDF/XML.

* **cottas_file_path : *str***
  
    Path to the compressed COTTAS file.

* **path : *{‘spo’, ‘sop’, ‘pso’, ‘pos’, ‘osp’, ‘ops’}, default ‘spo’***
  
    Computed index for the compressed file. For [RDF datasets](https://www.w3.org/TR/rdf11-concepts/#section-dataset) index permutations include **`g`**, e.g., `spog`.
  
#### cottas2rdf

`{++pycottas.cottas2rdf(cottas_file_path, rdf_file_path)++}`

Uncompress a COTTAS file to RDF in plain text format. The output RDF is generated in N-Triples format.

**`Parameters:`**

* **cottas_file_path : *str***
  
    Path to the input COTTAS file.

* **rdf_file_path : *str***
  
    Path to the output RDF file.

#### search

`{++pycottas.search(cottas_file_path, triple_pattern)++}`

Evaluates a triple pattern over a COTTAS file.

**`Parameters:`**

* **cottas_file_path : *str***
  
    Path to the COTTAS file.

* **triple_pattern : *str***
  
    Triple pattern.

#### cat

`{++pycottas.cat(cottas_file_paths, cottas_cat_file_path, index='spo', remove_input_files=False)++}`

Merge multiple COTTAS files into one.

**`Parameters:`**

* **cottas_file_paths : *str***
  
    Paths to the COTTAS files to merge.

* **cottas_cat_file_path : *str***
  
    Output COTTAS file.

#### diff

`{++pycottas.diff(cottas_file_1_path, cottas_file_2_path, cottas_diff_file_path, index='spo', remove_input_files=False)++}`

Substract a COTTAS file from another.

**`Parameters:`**

* **cottas_file_1_path : *str***
  
    Initial COTTAS file.

* **cottas_file_2_path : *str***
  
    COTTAS file to substract.

* **cottas_diff_file_path : *str***
  
    Resulting COTTAS file.

#### info

`{++pycottas.info(cottas_file_path)++}`

Gets the metadata of a COTTAS file.

**`Parameters:`**

* **cottas_file_path : *str***
  
    Path to the COTTAS file.

#### verify

`{++pycottas.verify(cottas_file_path)++}`

Checks whether a COTTAS file is valid.

**`Parameters:`**

* **cottas_file_path : *str***
  
    Path to the COTTAS file.

### COTTASDocument

`{++pycottas.COTTASStore(path)++}`

Class for evaluating [triple patterns](https://www.w3.org/TR/sparql11-query/#sparqlTriplePatterns) over COTTAS files. 

**`Parameters:`**

* **path : *str***
  
    Path to the COTTAS file.

``` py title="Example: Querying COTTAS files with triple patterns using COTTASDocument" hl_lines="4"
from pycottas import COTTASDocument
from rdflib import Graph, URIRef

store = COTTASDocument("my_file.cottas")

# the triple pattern can be a string or a tuple
res = cottas_doc.search('?s <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> ?o') # (1)

# limit and offset are optional
res = cottas_doc.search((None, URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#type'), None), limit=10, offset=20) # (2)

print(res)
```

1.  :small_red_triangle_down: Here the triple pattern is provided as a **string**.
2.  :small_red_triangle_down: Here the triple pattern is provided as **tuple of RDFLib terms** (`None` for variables).

### COTTASStore

`{++pycottas.COTTASStore(path)++}`

[RDFLib](https://github.com/RDFLib/rdflib) store backend to query COTTAS files with [SPARQL](https://www.w3.org/TR/sparql11-query/).

**`Parameters:`**

* **path : *str***
  
    Path to the COTTAS file.

``` py title="Example: Querying COTTAS files with SPARQL using COTTASStore" hl_lines="4"
from pycottas import COTTASStore
from rdflib import Graph

store = COTTASStore("my_file.cottas")

graph = Graph(store)

res = graph.query("""
  PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
  SELECT DISTINCT ?s ?o WHERE {
    ?s rdf:type ?o .
  } LIMIT 10""")

for row in res:
    print(row)
```

## Command Line

To execute COTTAS from the command line, it is necessary to call the `pycottas` package, specifying the pycottas operation to perform (`rdf2cottas`, `search`, `cat`, etc.), and providing a set of parameters.

``` hl_lines="1"
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

``` hl_lines="1"
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

``` hl_lines="1"
$ python3 -m pycottas cottas2rdf -h

usage: pycottas cottas2rdf -c COTTAS_FILE -r RDF_FILE

options:
  -c COTTAS_FILE, --cottas_file COTTAS_FILE
                        Path to COTTAS file
  -r RDF_FILE, --rdf_file RDF_FILE
                        Path to RDF file (N-Triples)
```

#### search

``` hl_lines="1"
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

``` hl_lines="1"
$ python3 -m pycottas info -h

usage: pycottas info -c COTTAS_FILE

options:
  -c COTTAS_FILE, --cottas_file COTTAS_FILE
                        Path to COTTAS file
```

#### verify

``` hl_lines="1"
$ python3 -m pycottas verify -h

usage: pycottas verify -c COTTAS_FILE

options:
  -c COTTAS_FILE, --cottas_file COTTAS_FILE
                        Path to COTTAS file
```

#### cat

``` hl_lines="1"
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

``` hl_lines="1"
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

## Tricks


![OEG](assets/logo-oeg.png){ width="150" align=left } ![UPM](assets/logo-upm.png){ width="161" align=right }
