#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Proof-of-concept for RDFlib atop KùzuDB
"""

import json
import typing

from icecream import ic  # pylint: disable=E0401
import pandas as pd  # pylint: disable=E0401
import pyshacl  # type: ignore  # pylint: disable=E0401
import rdflib  # type: ignore  # pylint: disable=E0401


rdflib.plugin.register(
    "kuzudb",
    rdflib.store.Store,
    "graph",
    "PropertyGraph",
)


if __name__ == "__main__":
    ## load and configure the `RDFlib` integration
    graph: rdflib.Graph = rdflib.Graph(
        store = "kuzudb",
        identifier = "kuzudb",
    )

    graph.open(
        configuration = json.dumps({
            "db_path": "db",
            "db_rt": "UniKG_rt",
            "db_lt": "UniKG_lt",
        }),
        create = True,
    )


    ## confirm the number of RDF triples, which should be `16`
    ic(len(graph))


    ## run a SPARQL query
    QUERY: str = """
SELECT ?src ?rel ?dst
WHERE {
  ?src ?rel ?dst .
}"""

    df: pd.DataFrame = pd.DataFrame([
        r.asdict() for r in graph.query(QUERY)
    ])

    print(QUERY.strip())
    ic(df)


    ## run a SHACL report on the RDF data
    SHAPES_GRAPH: str = """
@prefix sh:   <http://www.w3.org/ns/shacl#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix kz: <http://kuzu.io/rdf-ex#> .

kz:PersonShape
    a sh:NodeShape ;
    sh:targetClass kz:student ;
    sh:property [
        sh:path kz:age ;
        sh:datatype xsd:integer
    ] .
"""

    results: typing.Tuple = pyshacl.validate(
        graph,
        shacl_graph = SHAPES_GRAPH,
        data_graph_format = "json-ld",
        shacl_graph_format = "ttl",
        #inference = "rdfs",
        inplace = False,
        serialize_report_graph = "ttl",
        debug = False,
    )

    conforms, report_graph, report_text = results
    print(report_text)


    ## run a more constrained SPARQL query
    QUERY = """
PREFIX kz: <http://kuzu.io/rdf-ex#>
SELECT DISTINCT ?src ?name
WHERE {
  ?src a kz:faculty .
  ?src kz:name ?name .
}"""

    df = pd.DataFrame([
        r.asdict() for r in graph.query(QUERY)
    ])

    print(QUERY.strip())
    ic(df)
