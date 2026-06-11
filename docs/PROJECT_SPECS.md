# Especificacion del Proyecto: Bulk Endpoint Test Runner

## Estado Actual

- Repositorio: `jsiles/poc_multiple_test_storeprocedure`
- Rama base inspeccionada: `main`
- Pull requests abiertos: ninguno
- Issues abiertos: ninguno
- GitHub Actions: no hay ejecuciones registradas
- CI configurado: no detectado
- Tests automatizados: no detectados

Durante la inspeccion se encontro un bloqueo de runtime: `app/runner.py` importaba `app.config` y `app.requester`, pero esos modulos no existian en el repositorio. Se agregaron localmente ambos archivos:

- `app/config.py`: carga configuracion desde variables de entorno y `.env`
- `app/requester.py`: ejecuta requests HTTP usando el payload del caso de prueba

Validacion realizada:

- `python -m compileall app main.py`: exitoso usando el Python bundled de Codex
- Import completo de la aplicacion: bloqueado porque el entorno local no tiene instaladas las dependencias del proyecto, empezando por `python-dotenv`

## Objetivo

Construir una herramienta Python para ejecutar pruebas masivas contra un endpoint HTTP, usando casos de prueba almacenados en una base de datos, evaluando las respuestas obtenidas contra resultados esperados y generando reportes consolidados en CSV y JSON.

## Alcance Funcional

La aplicacion debe:

1. Cargar configuracion desde variables de entorno o archivo `.env`.
2. Conectarse a una base de datos compatible con SQLAlchemy.
3. Ejecutar una query configurable para obtener casos de prueba.
4. Convertir cada registro en un caso de prueba.
5. Enviar un request HTTP al endpoint configurado.
6. Evaluar el status HTTP recibido contra el status esperado.
7. Evaluar opcionalmente si el body de respuesta contiene un texto esperado.
8. Registrar errores de request o ejecucion por caso sin detener todo el lote.
9. Imprimir un resumen de ejecucion en consola.
10. Guardar el detalle de resultados en archivos CSV y JSON.

## Configuracion

Variables soportadas:

| Variable | Requerida | Default | Descripcion |
| --- | --- | --- | --- |
| `DB_CONNECTION_STRING` | Si | `sqlite:///test_cases.db` | Cadena de conexion SQLAlchemy |
| `TEST_CASES_QUERY` | Si | Query SELECT basica | Query para leer casos de prueba |
| `ENDPOINT_URL` | Si | vacio | URL del endpoint a probar |
| `HTTP_METHOD` | No | `POST` | Metodo HTTP usado para invocar el endpoint |
| `HTTP_TIMEOUT` | No | `30` | Timeout del request en segundos |
| `HTTP_HEADERS` | No | `{}` | Headers HTTP en formato JSON |
| `RESULTS_DIR` | No | `results` | Carpeta donde se guardan resultados |
| `RESULTS_BASENAME` | No | `bulk_test_results` | Prefijo base de archivos generados |

## Modelo de Datos de Entrada

La query configurada debe devolver al menos:

| Campo | Tipo esperado | Requerido | Descripcion |
| --- | --- | --- | --- |
| `id` | cualquiera | Si | Identificador del caso |
| `name` | string | No | Nombre descriptivo del caso |
| `payload` | string JSON | No | Body enviado al endpoint |
| `expected_status` | integer | No | Status HTTP esperado |
| `expected_contains` | string | No | Texto esperado dentro del body de respuesta |

Defaults aplicados por la aplicacion:

- `name`: `case_{id}`
- `payload`: `{}`
- `expected_status`: `200`
- `expected_contains`: `None`

## Flujo de Ejecucion

1. `main.py` llama `run_bulk_tests()`.
2. `run_bulk_tests()` carga settings desde `app.config`.
3. Valida que `ENDPOINT_URL` este configurado.
4. `app.db.load_test_cases()` obtiene registros desde la base de datos.
5. Para cada caso:
   - `app.requester.execute_request()` ejecuta el request HTTP.
   - `app.evaluator.evaluate_response()` compara resultado real contra esperado.
   - Si ocurre una excepcion, se genera un resultado fallido con `error_message`.
6. `app.reporter.print_summary()` imprime resumen.
7. `app.reporter.save_results()` escribe CSV y JSON con timestamp.

## Criterios de Evaluacion

Un caso pasa cuando:

- `actual_status == expected_status`
- y, si `expected_contains` fue informado, el texto aparece dentro de `response.text`

Un caso falla cuando:

- El status recibido no coincide.
- El texto esperado no aparece en la respuesta.
- Ocurre un error al construir o ejecutar el request.

## Salidas

La aplicacion genera:

- Resumen de consola:
  - total de casos
  - exitosos
  - fallidos
  - detalle por caso
- Archivo CSV:
  - `RESULTS_DIR/RESULTS_BASENAME_YYYYMMDD_HHMMSS.csv`
- Archivo JSON:
  - `RESULTS_DIR/RESULTS_BASENAME_YYYYMMDD_HHMMSS.json`

Campos esperados por resultado:

- `id`
- `name`
- `passed`
- `expected_status`
- `actual_status`
- `expected_contains`
- `response_contains_match`
- `request_payload`
- `response_body`
- `error_message`

## Requisitos No Funcionales

- Python 3.10+
- Dependencias declaradas en `requirements.txt`
- Compatible con bases soportadas por SQLAlchemy
- El proceso debe continuar aunque un caso falle
- Los errores por caso deben quedar reportados
- Los reportes deben ser reproducibles y auditablemente fechados

## Riesgos y Gaps Actuales

- No hay tests automatizados.
- No hay workflow de CI.
- No existe validacion avanzada del JSON de entrada.
- `payload` debe ser JSON valido; si no lo es, el caso fallara por excepcion.
- `HTTP_HEADERS` debe ser un objeto JSON valido.
- No hay soporte nativo para auth dinamica, retries, concurrencia o metricas.
- No hay fixture de base de datos de ejemplo para ejecutar una prueba end-to-end local.

## Criterios de Aceptacion Sugeridos

1. Con un `.env` valido y una tabla con casos, `python main.py` debe ejecutar todos los casos.
2. Si el endpoint responde con el status esperado, el caso debe pasar.
3. Si `expected_contains` esta configurado, el caso solo debe pasar si el body contiene ese texto.
4. Si un request falla, el proceso debe continuar con el siguiente caso.
5. Al terminar, deben generarse archivos CSV y JSON.
6. El resumen de consola debe coincidir con los resultados guardados.

## Proximos Pasos Recomendados

1. Instalar dependencias y ejecutar una prueba local con SQLite.
2. Agregar tests unitarios para `config`, `requester`, `evaluator` y `db`.
3. Agregar un workflow de GitHub Actions para correr lint/test.
4. Agregar un script o fixture para crear `test_cases.db` de ejemplo.
5. Considerar validaciones JSON mas expresivas para comparar respuestas estructuradas.
