# kuzu-rdflib

An integration of KùzuDB and RDFlib.

The library module for this demo is in `graph.py` where an RDFlib
"Store" plugin has been adapted to manage its RDF triples within a
KùzuDB graph database.


## Set up

```bash
git clone https://github.com/DerwenAI/kuzu-rdflib.git
cd kuzu-rdflib
python3 -m venv venv
source venv/bin/activate

python3 -m pip install -U pip
python3 -m pip install -r requirements.txt
```

## Usage

First, clear the existing database directory and run `sparql.py` to
reinitialize the data:

```bash
rm -rf db
python3 sparql.py
```

Then run the demo script to query for the ingredients of spätzle:

```bash
python3 demo.py
```


