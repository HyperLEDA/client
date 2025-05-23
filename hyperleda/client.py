import dataclasses
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
        Responds with internally generated code for the source which can be used as bibcode in other methods.
        """
        data = self._request(
            "POST",
            "/admin/api/v1/source",
            dataclasses.asdict(model.CreateSourceRequestSchema(title=title, authors=authors, year=year)),
        )

        return model.CreateSourceResponseSchema(**data["data"]).code

    def create_table(self, table_description: model.CreateTableRequestSchema) -> int:
        """
        Create new table with raw data from the source.
        """
        data = self._request(
            "POST",
            "/admin/api/v1/table",
            dataclasses.asdict(table_description),
        )

        return model.CreateTableResponseSchema(**data["data"]).id

    def add_data(self, table_id: int, data: pandas.DataFrame) -> None:
        """
        Add new data to the table created in `create_table` method.
        """
        _ = self._request(
            "POST",
            "/admin/api/v1/table/data",
            dataclasses.asdict(model.AddDataRequestSchema(table_id, data.to_dict("records"))),
        )

    def start_processing(self, table_id: int) -> None:
        """
        Start processing the table data. Processing includes cross-identification of objects.
        """
        _ = self._request(
            "POST",
            "/admin/api/v1/table/process",
            dataclasses.asdict(model.TableProcessRequestSchema(table_id)),
        )

    def get_table_status_stats(self, table_id: int) -> model.TableStatusStatsResponseSchema:
        """
        Get statistics of cross identification of the table. Shows the total number of objects
        in each status.
        """
        data = self._request(
            "GET",
            "/admin/api/v1/table/status/stats",
            query={"table_id": str(table_id)},
        )
        return model.TableStatusStatsResponseSchema(**data["data"])

    def set_table_status(self, table_id: int, overrides: list[model.Overrides] | None = None) -> None:
        """
        Moves objects that were cross identified successfully to the homogenous part of the
        database. If `overrides` is provided, will manually set status the provided object.
        """
        _ = self._request(
            "POST",
            "/admin/api/v1/table/status",
            dataclasses.asdict(model.SetTableStatusRequestSchema(table_id, overrides)),
        )

    def validate_table(self, table_name: str) -> model.GetTableValidationResponseSchema:
        """
        Validate the table data. Checks if all objects were cross-identified and if there are
        any duplicates.
        """
        data = self._request(
            "GET",
            "/admin/api/v1/table/validation",
            query={"table_name": str(table_name)},
        )
        return model.GetTableValidationResponseSchema(**data["data"])

    def patch_table_schema(self, table_name: str, actions: list) -> None:
        """
        Patch table schema with provided actions. For example, change UCD or unit of the column.
        """
        _ = self._request(
            "PATCH",
            "/admin/api/v1/table",
            dataclasses.asdict(model.PatchTableRequestSchema(table_name, actions)),
        )

    def create_marking(self, table_name: str, rules: list[model.Catalog]) -> None:
        _ = self._request(
            "POST",
            "/admin/api/v1/marking",
            dataclasses.asdict(model.CreateMarkingRequestSchema(table_name, rules)),
        )
