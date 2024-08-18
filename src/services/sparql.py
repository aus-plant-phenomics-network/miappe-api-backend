from collections.abc import Mapping, Sequence
from typing import Any, Literal, cast

from SPARQLWrapper import JSON, SPARQLWrapper

URL = "https://demo.vocabs.ardc.edu.au/repository/api/sparql/appf_appf-test-project-2_appf-test-project-2-v0-1"

SKOS_CONCEPT_PROPERTY = Literal[
    "altLabel",
    "hiddenLabel",
    "definition",
    "notation",
    "example",
    "scopeNote",
    "broader",
    "narrower",
    "related",
    "exactMatch",
    "closeMatch",
    "broaderMatch",
    "relatedMatch",
]

ALL_PROPERTIES = [
    "altLabel",
    "hiddenLabel",
    "definition",
    "notation",
    "example",
    "scopeNote",
    "broader",
    "narrower",
    "related",
    "exactMatch",
    "closeMatch",
    "broaderMatch",
    "relatedMatch",
]

QUERY_RESULT = Mapping[SKOS_CONCEPT_PROPERTY, Any]

QUERY_LEAF = """
PREFIX dcterms:<http://purl.org/dc/terms/>
PREFIX skos:<http://www.w3.org/2004/02/skos/core#>

SELECT *

WHERE {{
    OPTIONAL{{?concept skos:narrower ?narrower}}
    FILTER(!BOUND(?narrower)) .
    ?concept skos:prefLabel ?prefLabel .
    ?concept skos:inScheme ?scheme .
    ?scheme dcterms:title ?schemeTitle .
    FILTER(REGEX(?schemeTitle, "Trait", "i" )) .
}}
"""


class QueryFactory:
    @staticmethod
    def concept_by_uri(uri: str) -> str:
        stmt = ""
        stmt += "PREFIX dcterms:<http://purl.org/dc/terms/>\n"
        stmt += "PREFIX skos:<http://www.w3.org/2004/02/skos/core#>\n\n"
        stmt += "SELECT * \n\n"
        stmt += "WHERE {{\n"
        for prop in ALL_PROPERTIES:
            stmt += f"    OPTIONAL{{?concept skos:{prop} ?{prop}}} .\n"
        stmt += "    ?concept skos:prefLabel ?prefLabel .\n"
        stmt += "    ?concept skos:inScheme ?scheme .\n"
        stmt += "    ?scheme dcterms:title ?schemeTitle .\n"
        stmt += f"    FILTER(?concept = <{uri}>) .\n"
        stmt += "}}\n\n"
        return stmt

    @staticmethod
    def all_leaf_concepts(scheme: str, limit: int | None = None, offset: int | None = None) -> str:
        return QueryFactory.leaf_concept(scheme=scheme, limit=limit, offset=offset)

    @staticmethod
    def leaf_concept(
        *properties: SKOS_CONCEPT_PROPERTY,
        scheme: str,
        pref_label: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> str:
        stmt = ""
        stmt += "PREFIX dcterms:<http://purl.org/dc/terms/>\n"
        stmt += "PREFIX skos:<http://www.w3.org/2004/02/skos/core#>\n\n"
        stmt += "SELECT * \n\n"
        stmt += "WHERE {{\n"
        for prop in properties:
            stmt += f"    OPTIONAL{{?concept skos:{prop} ?{prop}}} .\n"
        stmt += "    ?concept skos:prefLabel ?prefLabel .\n"
        if pref_label:
            stmt += f'    FILTER(REGEX(?prefLabel, "{pref_label}", "i" )) .\n'
        stmt += "    ?concept skos:inScheme ?scheme .\n"
        stmt += "    ?scheme dcterms:title ?schemeTitle .\n"
        stmt += f'    FILTER(REGEX(?schemeTitle, "{scheme}", "i" )) .\n'
        stmt += "}}\n\n"
        if limit:
            stmt += f"LIMIT {limit}\n\n"
        if offset:
            stmt += f"OFFSET {offset}\n\n"
        return stmt


class SPARQLService:
    def __init__(self, url: str = URL) -> None:
        self.url = url
        self._service = SPARQLWrapper(endpoint=url)
        self._service.setReturnFormat(JSON)
        self._last_stmt = ""

    @property
    def last_stmt(self) -> str:
        return self._last_stmt

    def _execute_query(self, query: str) -> Sequence[QUERY_RESULT]:
        self._service.setQuery(query)
        self._last_stmt = query
        try:
            ret = cast(dict[str, Any], self._service.queryAndConvert())
            rows = cast(list[dict[str, Any]], ret["results"]["bindings"])
            rows = [{key: value.get("value", None) for key, value in row.items()} for row in rows]
            return cast(Sequence[Mapping[SKOS_CONCEPT_PROPERTY, Any]], rows)

        except Exception as e:
            raise e

    def get_leaf_concepts(
        self, scheme: str, limit: int | None = None, offset: int | None = None
    ) -> Sequence[QUERY_RESULT]:
        stmt = QueryFactory.all_leaf_concepts(scheme=scheme, limit=limit, offset=offset)
        return self._execute_query(stmt)

    def get_concept_by_id(self, uri: str) -> QUERY_RESULT | None:
        stmt = QueryFactory.concept_by_uri(uri)
        result = self._execute_query(stmt)
        return result[0] if result else None

    def get_concept_by_pref_label(
        self,
        scheme: str,
        label: str,
        limit: int | None = None,
        offset: int | None = None,
    ) -> Sequence[QUERY_RESULT]:
        stmt = QueryFactory.leaf_concept(
            scheme=scheme,
            pref_label=label,
            limit=limit,
            offset=offset,
        )
        return self._execute_query(stmt)
