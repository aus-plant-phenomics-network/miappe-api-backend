from collections.abc import Sequence

from litestar import Controller, get

from src.services.sparql import QUERY_RESULT, SPARQLService


class SPARQLController(Controller):
    path: str = "/sparql"

    @get("/concept/uri")
    async def get_concept_by_uri(self, uri: str) -> QUERY_RESULT | None:
        service = SPARQLService()
        return service.get_concept_by_id(uri)

    @get("/concepts/{scheme: str}")
    async def get_all_concepts(
        self,
        scheme: str,
        limit: int | None = None,
        offset: int | None = None,
    ) -> Sequence[QUERY_RESULT]:
        service = SPARQLService()
        return service.get_leaf_concepts(
            scheme=scheme,
            limit=limit,
            offset=offset,
        )

    @get("/concept")
    async def get_concept_by_label(
        self,
        scheme: str,
        label: str,
        limit: int | None = None,
        offset: int | None = None,
    ) -> Sequence[QUERY_RESULT]:
        service = SPARQLService()
        return service.get_concept_by_pref_label(
            scheme=scheme,
            label=label,
            limit=limit,
            offset=offset,
        )
