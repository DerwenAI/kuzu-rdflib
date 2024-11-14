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

python3 -m venv venv
source venv/bin/activate

python3 -m pip install -U pip wheel setuptools
python3 -m pip install -r requirements.txt
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

> [!NOTE]
> Why we need to pin the dependency for Kùzu specifically:
> - Starting from Kùzu v0.7.0, we will temporarily stop supporting RDFGraphs as the current implementation is not very scalable and maintainable. The Kùzu core team is thinking deeply about this, and we have plans to re-implement RDFGraphs in Kùzu as an extension so that we don't have a bloated binary for the database.
> - Users who want to experiment with pyshacl and rdflib using Kùzu can still do so using the pinned versions of packages specified in this repo.
>
> Please join the Kùzu [Discord](https://kuzudb.com/chat) if you want to discuss more on RDF graphs and Kùzu!
