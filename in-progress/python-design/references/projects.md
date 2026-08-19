# Projects

Source maps for the 10 reference projects. Use to find specific implementations in the original codebase.

---

## pydantic (`~/third-party/pydantic`)

| File | Responsibility |
|------|---------------|
| `pydantic/__init__.py` | Public API surface, lazy `__getattr__`, `__all__` |
| `pydantic/main.py` | `BaseModel` — `__init__`, `model_dump`, `model_validate` |
| `pydantic/fields.py` | `Field` specifier, field metadata |
| `pydantic/_internal/_model_construction.py` | `ModelMetaclass` — schema building at class-definition time |
| `pydantic/_internal/_decorators.py` | Decorator metadata extraction (`@field_validator`, `@model_validator`) |
| `pydantic/_internal/_generate_schema.py` | Type → core schema mapping |
| `pydantic/_internal/_validators.py` | Validator assembly from schema |
| `pydantic/_internal/_serializers.py` | Serializer assembly from schema |
| `pydantic/_internal/_config.py` | `ConfigDict` processing |
| `pydantic/_internal/_mock_val_ser.py` | `MockValSer` — deferred schema construction |
| `pydantic/functional_validators.py` | `AfterValidator`, `BeforeValidator`, `WrapValidator`, `PlainValidator` (all `frozen=True, slots=True`) |
| `pydantic/annotated_handlers.py` | `Annotated` metadata → core schema handlers |
| `pydantic/type_adapter.py` | `TypeAdapter` — validate arbitrary types without a model |
| `pydantic/dataclasses.py` | Pydantic-backed dataclass support |

**Key patterns**: Metaclass-driven model construction, four validator modes, `ValidationError` error aggregation, `_internal/` convention, lazy `__getattr__` imports, `MockValSer` deferred build.

---

## httpx (`~/third-party/httpx`)

| File | Responsibility |
|------|---------------|
| `httpx/__init__.py` | Public API, `__all__`, convenience functions (`get`, `post`) |
| `httpx/_client.py` | `Client` and `AsyncClient` — parallel sync/async, `BaseClient` shared base |
| `httpx/_models.py` | `Request`, `Response`, `URL`, `Headers`, `Cookies` — immutable-ish models |
| `httpx/_transports/base.py` | `BaseTransport` / `AsyncBaseTransport` — Protocol interfaces |
| `httpx/_transports/mock.py` | `MockTransport` — testing adapter, inherits both sync+async |
| `httpx/_transports/wsgi.py` | `WSGITransport` — server-side testing |
| `httpx/_transports/asgi.py` | `ASGITransport` — server-side testing |
| `httpx/_config.py` | Client configuration, timeout, auth, proxies |

**Key patterns**: Sync/async duplication over abstraction, Protocol-based transport, `MockTransport` dual-interface, small interface + deep implementation, event hooks.

---

## rich (`~/third-party/rich`)

| File | Responsibility |
|------|---------------|
| `rich/console.py` | `Console` — rendering engine, `render()` protocol |
| `rich/segment.py` | `Segment` — universal rendering unit (text + style + control) |
| `rich/protocol.py` | `RichCast` protocol (`__rich__`) |
| `rich/abc.py` | `RichRenderable(ABC)` with `__subclasshook__` — structural typing |
| `rich/style.py` | `Style` — color, bold, italic, link composition |
| `rich/theme.py` | `Theme` — named style registry |
| `rich/table.py` | `Table` — composes `Column`, `Row`, any renderable |
| `rich/panel.py` | `Panel` — wraps any renderable with border |
| `rich/columns.py` | `Columns` — lays out renderables in columns |
| `rich/_loop.py` | `loop_first`, `loop_last` — iteration helpers (`_` prefix) |
| `rich/_pick.py` | `pick_bool` — first non-None selector (`_` prefix) |
| `rich/_stack.py` | `Stack(List[T])` — thin list wrapper (`_` prefix) |

**Key patterns**: Protocol-based design, Segment as universal unit, one element per module, `_` prefix for utilities, `__rich__` extension point.

---

## structlog (`~/third-party/structlog`)

| File | Responsibility |
|------|---------------|
| `structlog/_config.py` | `configure()` — processor chain assembly |
| `structlog/_base.py` | `BoundLoggerBase` — proxy to processor chain |
| `structlog/processors.py` | Built-in processors: `JSONRenderer`, `TimeStamper`, `add_log_level` |
| `structlog/contextvars.py` | `bind_contextvars` / `merge_contextvars` — context propagation |
| `structlog/stdlib.py` | `BoundLogger` wrapping stdlib `logging` |
| `structlog/_log_levels.py` | Level-based filtering as processor |

**Key patterns**: Processor chain `(logger, method, event_dict) → event_dict`, terminal processor as rendering boundary, `Protocol` over ABC, context via `contextvars`, immutable event dict contract.

---

## pluggy (`~/third-party/pluggy`)

| File | Responsibility |
|------|---------------|
| `pluggy/_hooks.py` | `HookspecMarker`, `HookimplMarker`, `HookCaller`, `HookImpl`, `HookSpec` |
| `pluggy/_manager.py` | `PluginManager` — registry, registration, `add_hookcall_monitoring` |
| `pluggy/_result.py` | `Result` — error isolation wrapper |
| `pluggy/_tracing.py` | Tracing via swappable `_inner_hookexec` |

**Key patterns**: Hook spec/impl separation, decorator as attribute stamp (no wrapping), `__slots__` everywhere, `@final` on building blocks, swappable execution strategy, `Result` for error isolation.

---

## msgspec (`~/third-party/msgspec`)

| File | Responsibility |
|------|---------------|
| `msgspec/__init__.py` | Public API — `Struct`, `Decoder`, `Encoder`, `decode`, `encode` |
| `msgspec/structs.py` | `Struct` base — `frozen`, `array_like`, `tag`, `gc` options |
| `msgspec/json.py` | Thin re-export from `_core` — JSON protocol |
| `msgspec/msgpack.py` | Thin re-export — MsgPack protocol |
| `msgspec/_core/exceptions.py` | `ValidationError`, `DecodeError` |
| `msgspec/_utils.py` | `get_class_annotations()` — type hint resolution with TypeVar support |
| `msgspec/_core/validators.py` | Compiled validators per type |

**Key patterns**: Types as schemas, `Struct` with slots/frozen, `Decoder[T]` as Generic, thin Python wrappers over C core, annotation-driven schema at definition time.

---

## dbt-core (`~/third-party/dbt-core`)

| File | Responsibility |
|------|---------------|
| `core/dbt/compilation.py` | Parse → compile → link, DAG construction |
| `core/dbt/graph.py` | Task graph, topological execution |
| `core/dbt/config.py` | Project + profile config loading |
| `core/dbt/context/providers.py` | Materialization context (table/view/incremental/ephemeral) |
| `core/dbt/adapters/base/` | Base adapter interface — `Relation`, `Column` types |
| `core/dbt/task/base.py` | `RunnableTask` — task interface |
| `core/dbt/exceptions.py` | Error hierarchy — `DbtRuntimeError`, `CompilationError` |

**Key patterns**: Config layering with per-field merge, materialization as strategy, adapter plugin pattern with Parse/Typed modes, error aggregation (collect-all default), fail-fast as opt-in.

---

## dagster (`~/third-party/dagster/python_modules/dagster/`)

| File | Responsibility |
|------|---------------|
| `src/dagster/_core/definitions/assets.py` | `@asset` decorator — asset declaration + dependency tracing |
| `src/dagster/_core/definitions/asset_dep.py` | Asset dependency resolution |
| `src/dagster/_core/definitions/op_definition.py` | `OpDefinition` — typed inputs/outputs (`In`, `Out`, `Nothing`) |
| `src/dagster/_core/definitions/graph_definition.py` | `@graph` — DAG composition, topological sort |
| `src/dagster/_core/definitions/resource_definition.py` | `ResourceDefinition` — resource injection via `required_resource_keys` |
| `src/dagster/_core/storage/io_manager.py` | `IOManager` — `load_input` / `handle_output` two-method boundary |

**Key patterns**: Software-defined assets with auto dependency inference, IO manager as serialization boundary, resource injection via string keys, graph composition with topological validation, Pydantic-based config schema.

---

## scikit-learn (`~/third-party/scikit-learn`)

| File | Responsibility |
|------|---------------|
| `sklearn/base.py` | `BaseEstimator` — `get_params`, `set_params`, `clone`. Mixins: `TransformerMixin`, `ClassifierMixin`, `RegressorMixin` |
| `sklearn/pipeline.py` | `Pipeline` — named step chain, `fit_transform` composition |
| `sklearn/utils/validation.py` | `check_X_y`, `check_array` — input validation |
| `sklearn/utils/_param_validation.py` | `@validate_params` decorator — parameter spec validation |
| `sklearn/metaestimators.py` | `_BaseComposition` — nested estimator management with `__` syntax |

**Key patterns**: `__init__` as parameter contract (signature introspection), `fit`/`transform`/`predict` protocol, `clone()` via `klass(**params)`, `_` suffix for fitted state, `@validate_params` decorator, nested `name__param` addressing.

---

## pandera (`~/third-party/pandera`)

| File | Responsibility |
|------|---------------|
| `pandera/schemas.py` | `DataFrameSchema` — schema definition, `validate()` with `lazy` flag |
| `pandera/columns.py` | `Column` — column-level schema |
| `pandera/checks.py` | `Check` — validation predicate abstraction, built-in checks |
| `pandera/errors.py` | `SchemaError`, `SchemaErrors` — structured failure data |
| `pandera/model.py` | `DataFrameModel` — class-based schema (Pydantic-like) |
| `pandera/model_components.py` | `Field`, `Config` — model components |
| `pandera/api/base/error_handler.py` | `ErrorHandler` — lazy/eager switch, error collection |

**Key patterns**: `lazy` flag for fail-fast vs collect-all, `ErrorHandler` encapsulating the decision, `SchemaErrors` with DataFrame of failures, `DataFrameModel` class-based schema with `Config` inner class, `Check` as composable predicate.
