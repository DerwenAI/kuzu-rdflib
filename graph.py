#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
RDFlib `Store` plugin for adapting RDF/W3C functionality into KùzuDB
"""

import pathlib
import typing

from icecream import ic
import chocolate  # type: ignore
import kuzu

from rdflib.plugins.sparql.sparql import Query, Update
import rdflib  # type: ignore


QUERY_TRIPLES: str = """
MATCH (s)-[p:UniKG_rt|UniKG_lt]->(o)
RETURN s.iri, p.iri, o.iri, o.val
"""

QUERY_COUNT: str = """
MATCH (s)-[p:UniKG_rt]-(o)
RETURN count(*)
"""


######################################################################
## class definitions

class PropertyGraph (rdflib.store.Store):
    """
A subclass of `rdflib.store.Store` to use as a plugin, to integrate
the W3C stack in Python.
    """

    def __init__ (
        self,
        *,
        configuration: typing.Optional[ str ] = None,
        identifier: typing.Optional[ rdflib.term.Identifier ] = None,
        ) -> None:
        """
Instance constructor
        """
        super().__init__(configuration)

        self.identifier: rdflib.term.Identifier = identifier
        self.__namespace: typing.Dict[ str, rdflib.term.URIRef ] = {}
        self.__prefix: typing.Dict[ rdflib.term.URIRef, str ] = {}

        self.conn: typing.Optional[ kuzu.Connection ] = None


######################################################################
## rdflib.store.Store implementation

    @classmethod
    def get_graph (
        cls,
        graph: rdflib.Graph,
        ) -> "PropertyGraph":
        """
An accessor method to extract the PropertyGraph from an RDF graph,
which is a private member of the `rdflib.Graph` object.
        """
        return graph._Graph__store  # type: ignore # pylint: disable=W0212


    def open (
        self,
        configuration: str,
        create: bool = False,
        ) -> typing.Optional[ int ]:
        """
Opens the Store/connection specified by the configuration string.
        """
        self.conn = kuzu.Connection(kuzu.Database(configuration))

        return rdflib.store.VALID_STORE


    def add (  # type: ignore # pylint: disable=R0201,W0221
        self,
        triple: typing.Tuple,
        *,
        context: typing.Optional[ rdflib.graph._ContextType ] = None,  # pylint: disable=W0613
        quoted: bool = False,  # pylint: disable=W0613
        ) -> None:
        """
Adds the given statement to a specific context or to the model.

The quoted argument is interpreted by formula-aware stores to indicate
this statement is quoted/hypothetical.

It should be an error to not specify a context and have the quoted
argument be `True`.

It should also be an error for the quoted argument to be `True` when
the store is not formula-aware.
        """
        s, p, o = triple  # pylint: disable=W0612
        # DO SOMETHING?
        # We're ignoring this operation, for now


    def remove (  # type: ignore # pylint: disable=R0201,W0221
        self,
        triple_pattern: typing.Tuple,
        *,
        context: typing.Optional[ rdflib.graph._ContextType ] = None,  # pylint: disable=W0613
        ) -> None:
        """
Remove the set of triples matching the pattern from the store.
        """
        s, p, o = triple_pattern  # pylint: disable=W0612
        # DO SOMETHING?
        # We're ignoring this operation, for now


    def triples (  # type: ignore # pylint: disable=R0201,W0221
        self,
        triple_pattern: rdflib.graph._TriplePatternType,
        *,
        context: typing.Optional[ rdflib.graph._ContextType ] = None,  # pylint: disable=W0613
        debug: bool = None,
        ) -> typing.Iterator[
            typing.Tuple[
                rdflib.graph._TripleType,
                typing.Iterator[typing.Optional[ rdflib.graph._ContextType ]]
            ]
        ]:
        """
A generator over all the triples matching the pattern.

    triple_pattern:
Can include any objects for used for comparing against nodes in the store, for example, REGEXTerm, URIRef, Literal, BNode, Variable, Graph, QuotedGraph, Date? DateRange?

    context:
A conjunctive query can be indicated by either providing a value of None, or a specific context can be queries by passing a Graph instance (if store is context aware).  (currently IGNORED)
        """
        global QUERY_TRIPLES

        results: kuzu.query_result.QueryResult = self.conn.execute(QUERY_TRIPLES)

        if debug:
            ic(triple_pattern)

        while results.has_next():
            s_iri, p_iri, o_iri, o_val = results.get_next()

            if debug:
                ic(s_iri, p_iri, o_iri, o_val)

            if o_iri is not None:
                triple = ( rdflib.term.URIRef(s_iri), rdflib.term.URIRef(p_iri), rdflib.term.URIRef(o_iri), )
            else:
                triple = ( rdflib.term.URIRef(s_iri), rdflib.term.URIRef(p_iri), rdflib.term.Literal(o_val), )

            is_match: bool = True

            for i in range(3):
                if triple_pattern[i] is not None and triple_pattern[i] != triple[i]:
                    if debug:
                        print("fail", i, triple)
    
                    is_match = False
                    break

            if is_match:
                if debug:
                    print("  !!YIELD", triple)

                yield triple, self.__contexts()


    def __len__ (  # type: ignore # pylint: disable=W0221,W0222
        self,
        *,
        context: typing.Optional[ rdflib.graph._ContextType ] = None,  # pylint: disable=W0613
        ) -> int:
        """
Number of statements in the store. This should only account for
non-quoted (asserted) statements if the context is not specified,
otherwise it should return the number of statements in the formula or
context given.

    context:
a graph instance to query or None
        """
        global QUERY_COUNT

        results: kuzu.query_result.QueryResult = self.conn.execute(QUERY_COUNT)
        count: int = results.get_next()[0]

        return count


    def __contexts (  # pylint: disable=R0201
        self
        ) -> typing.Generator[ rdflib.graph._ContextType, None, None ]:
        """
A no-op, since contexts are not yet supported.
        """
        # best way to return an empty generator
        l: list = []
        return (c for c in l)


    def bind (
        self,
        prefix: str,
        namespace: rdflib.term.URIRef,
        *,
        override: bool = True,
        ) -> None:
        """
Should be identical to `Memory.bind`
        """
        self.__prefix[namespace] = prefix
        self.__namespace[prefix] = namespace


    def namespace (
        self,
        prefix: str,
        ) -> typing.Optional[ rdflib.term.URIRef ]:
        """
Should be identical to `Memory.namespace`
        """
        return self.__namespace.get(prefix, None)


    def prefix (
        self,
        namespace: rdflib.term.URIRef,
        ) -> typing.Optional[ str ]:
        """
Should be identical to `Memory.prefix`
        """
        return self.__prefix.get(namespace, None)


    def namespaces (
        self
        ) -> typing.Iterator[typing.Tuple[ str, rdflib.term.URIRef ]]:
        """
Should be identical to `Memory.namespaces`
        """
        for prefix, namespace in self.__namespace.items():
            yield prefix, namespace


    def query (  # pylint: disable=W0235
        self,
        query: typing.Union[ Query, str ],
        initNs: typing.Mapping[ str, typing.Any ],
        initBindings: typing.Mapping[ str, rdflib.term.Identifier ],
        queryGraph: typing.Any,
        **kwargs: typing.Any,
        ) -> rdflib.query.Result:
        """
queryGraph is None, a URIRef or '__UNION__'

If None the graph is specified in the query-string/object

If URIRef it specifies the graph to query,

If  '__UNION__' the union of all named graphs should be queried

This is used by ConjunctiveGraphs
Values other than None obviously only makes sense for context-aware stores.)
        """
        super().query(
            query,
            initNs,
            initBindings,
            queryGraph,
            **chocolate.filter_args(kwargs, super().query),
        )


    def update (  # pylint: disable=W0235
        self,
        update: typing.Union[ Update, str ],
        initNs: typing.Mapping[ str, typing.Any ],
        initBindings: typing.Mapping[ str, rdflib.term.Identifier ],
        queryGraph: typing.Any,
        **kwargs: typing.Any,
        ) -> None:
        """
queryGraph is None, a URIRef or '__UNION__'

If None the graph is specified in the query-string/object

If URIRef it specifies the graph to query,

If  '__UNION__' the union of all named graphs should be queried

This is used by ConjunctiveGraphs
Values other than None obviously only makes sense for context-aware stores.)
        """
        super().update(
            update,
            initNs,
            initBindings,
            queryGraph,
            **chocolate.filter_args(kwargs, super().update),
        )
