import dataclasses
from typing import Any

from hyperleda import common, config
from hyperleda.data import model


class HyperLedaDataClient:
    """
    Client for the HyperLeda data API, providing access to public query endpoints.
    """

    def __init__(self, endpoint: str = config.DEFAULT_ENDPOINT):
        self.endpoint = endpoint

    def _request(self, method: str, path: str, query: dict[str, Any] | None = None, stream: bool = False) -> Any:
        return common.request(method, f"{self.endpoint}{path}", query=query, stream=stream)

    def query_simple(self, req: model.QuerySimpleRequestSchema) -> model.QuerySimpleResponseSchema:
        """
        Query data about objects using simple parameters (AND logic).
        """
        response = self._request(
            "GET",
            "/api/v1/query/simple",
            query=dataclasses.asdict(req),
        )
        data = response.json()
        return model.QuerySimpleResponseSchema(**data["data"])

    def query(self, req: model.QueryRequestSchema) -> model.QueryResponseSchema:
        """
        Query data about objects using a query string (functions and operators).
        """
        response = self._request(
            "GET",
            "/api/v1/query",
            query=dataclasses.asdict(req),
        )
        data = response.json()
        return model.QueryResponseSchema(**data["data"])

    def query_fits(self, req: model.FITSRequestSchema) -> bytes:
        """
        Query data about objects and return as FITS file (binary).
        """
        response = self._request(
            "GET",
            "/api/v1/query/fits",
            query=dataclasses.asdict(req),
            stream=True,
        )
        return response.content
