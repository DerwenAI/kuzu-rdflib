#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Demo to load and query RDF triples in KùzuDB.
"""

import pathlib
import shutil

from icecream import ic
import kuzu


if __name__ == "__main__":
    DB_DIR: str = "db"
    db_path: pathlib.Path = pathlib.Path(DB_DIR)

    # remove pre-existing data from prior runs
    if db_path.exists() and db_path.is_dir():
        shutil.rmtree(db_path)

    # populate the RDF tables
    db = kuzu.Database(DB_DIR)
    conn = kuzu.Connection(db)

    conn.execute("CREATE RDFGraph UniKG")
    conn.execute("COPY UniKG FROM 'uni.ttl'")

    # run a query
    query: str = """
    MATCH (s)-[p:UniKG_rt]-(o) RETURN s.iri, p.iri, o.iri
    """

    results = conn.execute(query)

    while results.has_next():
        s, p, o = results.get_next()
        ic(s, p, o)
