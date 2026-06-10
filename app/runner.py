from app.config import load_settings
from app.db import load_test_cases
from app.evaluator import evaluate_response
from app.reporter import print_summary, save_results
from app.requester import execute_request


def run_bulk_tests() -> None:
    settings = load_settings()

    if not settings.endpoint_url:
        raise ValueError("ENDPOINT_URL no está configurado.")

    test_cases = load_test_cases(
        connection_string=settings.db_connection_string,
        query=settings.test_cases_query,
    )

    if not test_cases:
        print("No se encontraron casos de prueba.")
        return

    results = []

    for test_case in test_cases:
        try:
            response = execute_request(
                method=settings.http_method,
                url=settings.endpoint_url,
                payload=test_case.payload,
                headers=settings.http_headers,
                timeout=settings.http_timeout,
            )
            result = evaluate_response(test_case=test_case, response=response)
        except Exception as exc:
            result = evaluate_response(
                test_case=test_case,
                response=None,
                error_message=str(exc),
            )

        results.append(result)

    print_summary(results)
    csv_path, json_path = save_results(
        results=results,
        results_dir=settings.results_dir,
        basename=settings.results_basename,
    )

    print(f"Resultados CSV : {csv_path}")
    print(f"Resultados JSON: {json_path}")