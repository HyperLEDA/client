from typing import Any

import requests

from hyperleda import error, utils


def request(method: str, url: str, query: dict[str, Any] | None = None, stream: bool = False) -> requests.Response:
    kwargs = {}
    if query is not None:
        kwargs["params"] = utils.clean_dict(query)
    if stream:
        kwargs["stream"] = True
    response = requests.request(method, url, **kwargs)
    if not response.ok:
        try:
            msg = error.APIError.from_dict(response.json())
        except Exception:
            msg = error.APIError(response.status_code, response.text)
        raise msg
    return response
