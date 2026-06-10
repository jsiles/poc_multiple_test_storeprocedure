from app.models import TestCase, TestResult


def evaluate_response(test_case: TestCase, response=None, error_message: str = "") -> TestResult:
    actual_status = None
    response_body = ""
    response_contains_match = False
    passed = False

    if response is not None:
        actual_status = response.status_code
        response_body = response.text or ""

        status_ok = actual_status == test_case.expected_status

        if test_case.expected_contains:
            response_contains_match = test_case.expected_contains in response_body
        else:
            response_contains_match = True

        passed = status_ok and response_contains_match

    return TestResult(
        id=test_case.id,
        name=test_case.name,
        passed=passed,
        expected_status=test_case.expected_status,
        actual_status=actual_status,
        expected_contains=test_case.expected_contains,
        response_contains_match=response_contains_match,
        request_payload=test_case.payload,
        response_body=response_body,
        error_message=error_message,
    )