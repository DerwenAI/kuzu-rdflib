# kuzu-rdflib

A proof-of-concept integration of KùzuDB and RDFlib.

The library module for this demo is in `graph.py` where an RDFlib
"Store" plugin has been adapted to manage its RDF triples within a
KùzuDB graph database.

For details about these libraries, see:

  - RDF support in KùzuDB <https://docs.kuzudb.com/rdf-graphs/>
  - RDFlib <https://rdflib.readthedocs.io/>
  - pySHACL <https://github.com/RDFLib/pySHACL>
  - SHACL <https://www.w3.org/TR/shacl/>


## Set up

```bash
git clone https://github.com/DerwenAI/kuzu-rdflib.git
cd kuzu-rdflib

# Use uv to create a virtual environment
uv venv
source .venv/bin/activate

uv pip install -U wheel setuptools
uv pip install -r requirements.txt
```

## Usage

First, initialize the example RDF data from the `uni.ttl` file:

```bash
python3 prep.py
```

Then run the `demo.py` script to perform an example SPARQL query
and SHACL validation:

```bash
python3 demo.py
```
