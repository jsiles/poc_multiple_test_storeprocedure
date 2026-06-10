import json
import os
from datetime import datetime
import pandas as pd
from app.models import TestResult


def save_results(results: list[TestResult], results_dir: str, basename: str) -> tuple[str, str]:
    os.makedirs(results_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_path = os.path.join(results_dir, f"{basename}_{timestamp}.csv")
    json_path = os.path.join(results_dir, f"{basename}_{timestamp}.json")

    records = [result.__dict__ for result in results]

    df = pd.DataFrame(records)
    df.to_csv(csv_path, index=False)

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)

    return csv_path, json_path


def print_summary(results: list[TestResult]) -> None:
    total = len(results)
    passed = len([r for r in results if r.passed])
    failed = total - passed

    print("=" * 60)
    print("RESUMEN DE EJECUCIÓN")
    print("=" * 60)
    print(f"Total casos   : {total}")
    print(f"Exitosos      : {passed}")
    print(f"Fallidos      : {failed}")
    print("=" * 60)

    for result in results:
        status = "PASS" if result.passed else "FAIL"
        print(
            f"[{status}] id={result.id} name={result.name} "
            f"expected_status={result.expected_status} actual_status={result.actual_status}"
        )
        if result.error_message:
            print(f"       error={result.error_message}")