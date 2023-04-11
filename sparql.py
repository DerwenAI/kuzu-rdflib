#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pathlib

from icecream import ic
import kuzu


DB_DIR: str = "db"

# check if tables are populated already
db_exists: bool = pathlib.Path(DB_DIR).is_dir()
db = kuzu.Database(DB_DIR)
conn = kuzu.Connection(db)

# populate tables if not
if not db_exists:
    conn.execute("CREATE NODE TABLE subobj(iri STRING, PRIMARY KEY (iri))")
    conn.execute("CREATE REL TABLE triple(FROM subobj TO subobj, pred STRING)")

    conn.execute('COPY subobj FROM "nodes.csv"')
    conn.execute('COPY triple FROM "edges.csv"')

# run a query
query: str = """
MATCH (src:subobj)-[r:triple]->(dst:subobj) RETURN src.iri, r.pred, dst.iri;
"""
results = conn.execute(query)

while results.has_next():
    print(results.get_next())
