import json
from typing import Any

import requests


def _load_payload(payload: str) -> Any:
    if not payload:
        return {}

    return json.loads(payload)


def execute_request(
    method: str,
    url: str,
    payload: str,
    headers: dict[str, str],
    timeout: float,
) -> requests.Response:
    return requests.request(
        method=method.upper(),
        url=url,
        json=_load_payload(payload),
        headers=headers,
        timeout=timeout,
    )
