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
    DB_PATH: str = "db"
    DB_NAME: str = "UniKG"
    db_path: pathlib.Path = pathlib.Path(DB_PATH)

    # remove pre-existing data from prior runs
    if db_path.exists() and db_path.is_dir():
        shutil.rmtree(db_path)

    # populate the RDF tables
    db = kuzu.Database(DB_PATH)
    conn = kuzu.Connection(db)

    conn.execute(f"CREATE RDFGraph {DB_NAME}")
    conn.execute(f"COPY {DB_NAME} FROM 'uni.ttl'")

    # run a query
    query: str = f"""
    MATCH (s)-[p:{DB_NAME}_rt]-(o) RETURN s.iri, p.iri, o.iri
    """

    results = conn.execute(query)

    while results.has_next():
        s, p, o = results.get_next()
        ic(s, p, o)
