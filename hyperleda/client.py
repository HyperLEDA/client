import dataclasses
from typing import Any

import pandas
import requests

from hyperleda import config, error, model


class HyperLedaClient:
    """
    This is client for HyperLeda service. It allows one to query different types of data from the database
    and, if authentication information is present, add new data.
    """

    def __init__(self, endpoint: str = config.DEFAULT_ENDPOINT, token: str | None = None) -> None:
        self.endpoint = endpoint
        self.token = token

    def _set_auth(self, headers: dict[str, str]) -> dict[str, str]:
        if self.token is not None:
            headers["Authorization"] = f"Bearer {self.token}"

        return headers

    def _post(self, path: str, request: Any) -> dict[str, Any]:
        headers = {}
        if path.startswith("/api/v1/admin"):
            headers = self._set_auth(headers)

        response = requests.post(f"{self.endpoint}{path}", json=dataclasses.asdict(request), headers=headers)

        if not response.ok:
            raise error.APIError.from_dict(response.json())

        return response.json()

    def _get(self, path: str, query: dict[str, str]) -> dict[str, Any]:
        headers = {}
        if path.startswith("/api/v1/admin"):
            headers = self._set_auth(headers)

        response = requests.get(f"{self.endpoint}{path}", params=query, headers=headers)

        if not response.ok:
            raise error.APIError.from_dict(response.json())

        return response.json()

    def create_internal_source(self, title: str, authors: list[str], year: int) -> str:
        """
        Creates new source entry in the database for internal communication and unpublished articles.
        Responds with internally generated code for the source which can be used as bibcode in other methods.
        """
        data = self._post(
            "/api/v1/admin/source",
            model.CreateSourceRequestSchema(title=title, authors=authors, year=year),
        )

        return model.CreateSourceResponseSchema(**data["data"]).code

    def create_table(self, table_description: model.CreateTableRequestSchema) -> int:
        """
        Create new table with raw data from the source.
        """
        data = self._post(
            "/api/v1/admin/table",
            table_description,
        )

        return model.CreateTableResponseSchema(**data["data"]).id

    def add_data(self, table_id: int, data: pandas.DataFrame) -> None:
        """
        Add new data to the table created in `create_table` method.
        """
        _ = self._post(
            "/api/v1/admin/table/data",
            model.AddDataRequestSchema(table_id, data.to_dict("records")),
        )
