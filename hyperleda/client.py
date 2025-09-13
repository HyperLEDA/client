import enum
import json
from typing import Any

import pandas
import requests

from hyperleda import config, error, model, utils


def _marshaller(obj):
    if isinstance(obj, enum.Enum):
        return obj.value
    return str(obj)


class HyperLedaClient:
    """
    This is client for HyperLeda service. It allows one to query different types of data from the database
    and, if authentication information is present, add new data.
    """

    def __init__(self, endpoint: str = config.DEFAULT_ENDPOINT, token: str | None = None) -> None:
        self.endpoint = endpoint
        self.token = token

    def _request(
        self, method: str, path: str, body: dict[str, Any] | None = None, query: dict[str, str] | None = None
    ) -> dict[str, Any]:
        headers = {}
        if path.startswith("/admin/api/v1/admin"):
            if self.token is not None:
                headers["Authorization"] = f"Bearer {self.token}"

        kwargs = {}

        if body is not None:
            body = utils.clean_dict(body) if body is not None else None
            data = json.dumps(body, default=_marshaller)
            kwargs["data"] = data

        if query is not None:
            kwargs["params"] = query

        if len(headers) != 0:
            kwargs["headers"] = headers

        response = requests.request(method, f"{self.endpoint}{path}", **kwargs)
        if not response.ok:
            try:
                msg = error.APIError.from_dict(response.json())
            except Exception:
                msg = error.APIError(response.status_code, response.text)
            raise msg

        return response.json()

    def create_internal_source(self, title: str, authors: list[str], year: int) -> str:
        """
        Creates new source entry in the database for internal communication and unpublished articles.
        Responds with an internally generated code for the source which can be used as bibcode in other methods.
        """
        request_data = model.CreateSourceRequest(title=title, authors=authors, year=year)
        data = self._request(
            "POST",
            "/admin/api/v1/source",
            request_data.model_dump(),
        )

        return model.CreateSourceResponse(**data["data"]).code

    def create_table(self, table_description: model.CreateTableRequest) -> int:
        """
        Create new table with raw data from the source.
        """
        data = self._request(
            "POST",
            "/admin/api/v1/table",
            table_description.model_dump(),
        )

        return model.CreateTableResponse(**data["data"]).id

    def add_data(self, table_id: int, data: pandas.DataFrame) -> None:
        """
        Add new data to the table created in `create_table` method.
        """
        request_data = model.AddDataRequest(table_id=table_id, data=data.to_dict("records"))
        _ = self._request(
            "POST",
            "/admin/api/v1/table/data",
            request_data.model_dump(),
        )

    def start_processing(self, table_id: int) -> None:
        """
        Start processing the table data. Processing includes cross-identification of objects.
        """
        _ = self._request(
            "POST",
            "/admin/api/v1/table/process",
            {"table_id": table_id},
        )

    def patch_table_schema(self, table_name: str, actions: list) -> None:
        """
        Patch table schema with provided actions. For example, change UCD or unit of the column.
        """
        request_data = model.PatchTableRequest(table_name=table_name, actions=actions)
        _ = self._request(
            "PATCH",
            "/admin/api/v1/table",
            request_data.model_dump(),
        )

    def create_marking(self, table_name: str, rules: list[model.CatalogToMark]) -> None:
        request_data = model.CreateMarkingRequest(table_name=table_name, catalogs=rules)
        _ = self._request(
            "POST",
            "/admin/api/v1/marking",
            request_data.model_dump(),
        )
