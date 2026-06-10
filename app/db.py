from sqlalchemy import create_engine, text
from app.models import TestCase


def load_test_cases(connection_string: str, query: str) -> list[TestCase]:
    engine = create_engine(connection_string)

    with engine.connect() as connection:
        result = connection.execute(text(query))
        rows = result.mappings().all()

    test_cases = []
    for row in rows:
        test_cases.append(
            TestCase(
                id=row.get("id"),
                name=row.get("name", f"case_{row.get('id')}"),
                payload=row.get("payload", "{}"),
                expected_status=int(row.get("expected_status", 200)),
                expected_contains=row.get("expected_contains"),
            )
        )

    return test_cases