#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Proof of concept for RDFlib atop KùzuDB
"""

from icecream import ic
from rdflib.store import Store  # type: ignore
import rdflib  # type: ignore


rdflib.plugin.register(
    "ffurf",
    rdflib.store.Store,
    "graph",
    "PropertyGraph",
)


if __name__ == "__main__":
    graph = rdflib.Graph(
        store = "ffurf",
        identifier = "spatzle",
    )


    query = """
SELECT ?src ?dst
WHERE {
  ?src <http://purl.org/heals/food/hasIngredient> ?dst .
}"""

    res = graph.query(query)

    for row in res:
        ic(row)
