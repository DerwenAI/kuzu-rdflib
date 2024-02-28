# kuzu-rdflib

A proof-of-concept integration of KùzuDB and RDFlib.

The library module for this demo is in `graph.py` where an RDFlib
"Store" plugin has been adapted to manage its RDF triples within a
KùzuDB graph database.

For details about these libraries, see:

  - RDF support in KùzuDB <https://kuzudb.com/docusaurus/rdf-graphs/>
  - RDFlib <https://rdflib.readthedocs.io/>
  - pySHACL <https://github.com/RDFLib/pySHACL>
  - SHACL <https://www.w3.org/TR/shacl/>


## Set up

```bash
git clone https://github.com/DerwenAI/kuzu-rdflib.git
cd kuzu-rdflib

python3 -m venv venv
source venv/bin/activate

python3 -m pip install -U pip wheel setuptools
python3 -m pip install -r requirements.txt
```

## Usage

First, initialize the example RDF data from the `uni.ttl` file:

```bash
rm -rf db
python3 prep.py
```

Then run the `demo.py` script to perform an example SPARQL query
and SHACL validation:

```bash
python3 demo.py
```
