import json
import os
from dataclasses import dataclass
from typing import Any

from dotenv import load_dotenv


@dataclass
class Settings:
    db_connection_string: str
    test_cases_query: str
    endpoint_url: str
    http_method: str
    http_timeout: float
    http_headers: dict[str, str]
    results_dir: str
    results_basename: str


def _load_headers(raw_headers: str) -> dict[str, str]:
    if not raw_headers:
        return {}

    headers: Any = json.loads(raw_headers)
    if not isinstance(headers, dict):
        raise ValueError("HTTP_HEADERS debe ser un objeto JSON.")

    return {str(key): str(value) for key, value in headers.items()}


def load_settings() -> Settings:
    load_dotenv()

    return Settings(
        db_connection_string=os.getenv("DB_CONNECTION_STRING", "sqlite:///test_cases.db"),
        test_cases_query=os.getenv(
            "TEST_CASES_QUERY",
            "SELECT id, name, payload, expected_status, expected_contains FROM test_cases",
        ),
        endpoint_url=os.getenv("ENDPOINT_URL", ""),
        http_method=os.getenv("HTTP_METHOD", "POST").upper(),
        http_timeout=float(os.getenv("HTTP_TIMEOUT", "30")),
        http_headers=_load_headers(os.getenv("HTTP_HEADERS", "{}")),
        results_dir=os.getenv("RESULTS_DIR", "results"),
        results_basename=os.getenv("RESULTS_BASENAME", "bulk_test_results"),
    )
