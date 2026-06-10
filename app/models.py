from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class TestCase:
    id: Any
    name: str
    payload: str
    expected_status: int
    expected_contains: Optional[str] = None


@dataclass
class TestResult:
    id: Any
    name: str
    passed: bool
    expected_status: int
    actual_status: Optional[int]
    expected_contains: Optional[str]
    response_contains_match: bool
    request_payload: str
    response_body: str
    error_message: str