# Bulk Endpoint Test Runner

Proyecto Python para ejecutar pruebas masivas sobre un endpoint usando casos de prueba almacenados en una tabla de base de datos.

## Objetivo

Leer registros desde una tabla, transformar cada fila en una invocación a un endpoint, evaluar el resultado esperado y generar reportes consolidados.

## Requisitos

- Python 3.10+
- Acceso a la base de datos donde están los casos
- Endpoint disponible para prueba

## Instalación

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

En Windows:

```bash
.venv\Scripts\activate
pip install -r requirements.txt
```

## Configuración

Copiar el archivo de ejemplo:

```bash
cp .env.example .env
```

Configurar:

- `DB_CONNECTION_STRING`: cadena de conexión SQLAlchemy
- `TEST_CASES_QUERY`: query para leer los casos
- `ENDPOINT_URL`: endpoint a probar
- `HTTP_METHOD`: método HTTP
- `HTTP_TIMEOUT`: timeout en segundos
- `HTTP_HEADERS`: headers en formato JSON
- `RESULTS_DIR`: carpeta de salida
- `RESULTS_BASENAME`: nombre base de archivos de resultados

## Estructura esperada de la tabla

La consulta debe devolver al menos estas columnas:

- `id`
- `name`
- `payload`
- `expected_status`
- `expected_contains` (opcional)

Ejemplo:

```sql
SELECT
  id,
  name,
  payload,
  expected_status,
  expected_contains
FROM test_cases
```

## Ejemplo de tabla

```sql
CREATE TABLE test_cases (
  id INTEGER PRIMARY KEY,
  name VARCHAR(100),
  payload TEXT,
  expected_status INTEGER,
  expected_contains VARCHAR(255)
);
```

## Ejemplo de datos

```sql
INSERT INTO test_cases (id, name, payload, expected_status, expected_contains)
VALUES
(1, 'caso_ok', '{"document":"123","type":"A"}', 200, 'approved'),
(2, 'caso_error', '{"document":"999","type":"B"}', 400, 'invalid');
```

## Ejecución

```bash
python main.py
```

## Salida

El proceso genera:

- Resumen en consola
- Archivo CSV con el detalle de la ejecución
- Archivo JSON con el detalle de la ejecución

## Posibles mejoras

- Reintentos automáticos
- Ejecución concurrente
- Validaciones más complejas sobre JSON de respuesta
- Integración con pytest
- Métricas y dashboards