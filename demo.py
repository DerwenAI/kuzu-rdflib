#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Proof of concept for RDFlib atop KùzuDB
"""

from icecream import ic
from rdflib.store import Store  # type: ignore
import rdflib  # type: ignore


rdflib.plugin.register(
    "kuzudb",
    rdflib.store.Store,
    "graph",
    "PropertyGraph",
)


if __name__ == "__main__":
    graph = rdflib.Graph(
        store = "kuzudb",
        identifier = "xyzzy",
    )


    query = """
SELECT ?src ?rel ?dst
WHERE {
  ?src ?rel ?dst .
}"""

    res = graph.query(query)

    for row in res:
        ic(row)
