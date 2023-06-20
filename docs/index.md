# COTTAS

**COTTAS** is a toolkit for **[RDF-star](https://w3c.github.io/rdf-star/cg-spec/2021-12-17.html)** graph management in **compressed** space. It is based on a triple table representation of [RDF-star](https://w3c.github.io/rdf-star/cg-spec/2021-12-17.html) using the [Apache Parquet](https://parquet.apache.org/) file format with [ZSTD](https://en.wikipedia.org/wiki/Zstd). The toolkit is built on top of [DuckDB](https://duckdb.org/) and provides an **[HDT](https://www.rdfhdt.org/)**-like interface.

## Features

- Compress/uncompress [RDF-star](https://w3c.github.io/rdf-star/cg-spec/2021-12-17.html).
- Evaluate [triple patterns](https://w3c.github.io/rdf-star/cg-spec/2021-12-17.html#dfn-triple-star-pattern) over [RDF-star](https://w3c.github.io/rdf-star/cg-spec/2021-12-17.html) in compressed space.
- Merge compressed files.
- Executes via **command line** or as a **library**.
- Runs on **Linux**, **Windows** and **macOS** systems.

## COTTAS Files

COTTAS is based on COlumnar Triple TAble storage with the [Apache Parquet](https://parquet.apache.org/) file format. A COTTAS file consists on a table with **s**, **p**, **o**, **g** columns representing triples (and [named graphs](https://www.w3.org/TR/rdf11-concepts/#dfn-named-graph)). In addition, an optional **id** column is necessary when evaluating [triple patterns](https://w3c.github.io/rdf-star/cg-spec/2021-12-17.html#dfn-triple-star-pattern) over [RDF-star](https://w3c.github.io/rdf-star/cg-spec/2021-12-17.html).

- The **s**, **p**, **o**, **g** are filled with the [RDF-star terms](https://w3c.github.io/rdf-star/cg-spec/2021-12-17.html#dfn-rdf-star-terms) of the triples.
- When a triple belongs to the [default graph](https://www.w3.org/TR/rdf11-concepts/#dfn-default-graph), **g** is the empty string. If all the triples in the [dataset](https://w3c.github.io/rdf-star/cg-spec/2021-12-17.html#dfn-dataset) belong to the [default graph](https://www.w3.org/TR/rdf11-concepts/#dfn-default-graph), **g** can be omitted.
- The **id** column consists on the concatenation of the former columns. The **id** column is only necessary if evaluating [triple patterns](https://w3c.github.io/rdf-star/cg-spec/2021-12-17.html#dfn-triple-star-pattern) over [datasets](https://w3c.github.io/rdf-star/cg-spec/2021-12-17.html#dfn-dataset) with [quoted triples](https://w3c.github.io/rdf-star/cg-spec/2021-12-17.html#dfn-quoted).

## Licenses

**COTTAS** is available under the **[Apache License 2.0](https://github.com/morph-kgc/morph-kgc/blob/main/LICENSE)**.

The **documentation** is licensed under **[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)**.

## Author

- **[Julián Arenas-Guerrero](https://github.com/arenas-guerrero-julian/) - [julian.arenas.guerrero@upm.es](mailto:julian.arenas.guerrero@upm.es)**  
*[Ontology Engineering Group](https://oeg.fi.upm.es)*, *[Universidad Politécnica de Madrid](https://www.upm.es/internacional)*.


![OEG](assets/logo-oeg.png){ width="150" align=left } ![UPM](assets/logo-upm.png){ width="161" align=right }
