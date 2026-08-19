# Decisions
Decision guides for choosing between design alternatives. Derived from patterns validated across ≥3 projects.

---

## dataclass vs TypedDict vs Protocol vs BaseModel vs Struct

Choose `@dataclass(frozen=True, slots=True)` for internal fixed-shape value objects — immutable, memory-efficient, signals intent (19 projects use `__slots__`).

Choose `typing.Protocol` when describing capability — any class with the right methods satisfies, no inheritance needed (33 projects, the most common pattern in the DB).

Choose `pydantic.BaseModel` at external boundaries — validates at construction, collects all errors, serializes to/from JSON.

Choose `msgspec.Struct` when performance matters — types are schemas, compiled validators.

Choose `TypedDict` for typing dict payloads from external sources without converting — zero runtime cost.

Fitted/learned state uses `_` suffix (`self.coef_`) to separate from configuration (22 projects, scikit-learn contract).

---

## Protocol vs ABC

Default to `typing.Protocol` (33 occurrences, 15 projects). Structural subtyping — any class with the right methods satisfies, no inheritance needed.

Use `ABC` only when: you need `@abstractmethod` enforcement on subclasses, you provide shared implementation in the base, or you need `__subclasshook__` for custom isinstance checks.

`ABC` with `__subclasshook__` achieves structural typing but is a pre-Protocol workaround. New code should use `Protocol`.

---

## Eager vs lazy validation

**Eager** (fail-fast): raise on first error. Use for interactive input, CLI tools, or when early failure saves expensive downstream work.

**Lazy** (collect-all): aggregate all errors, raise once at the end. Default for batch processing — the cost of collecting errors is low, the value of seeing all failures is high.

Pydantic always collects (ValidationError aggregates). Pandera offers a `lazy` flag. dbt-core defaults to collect-all with fail-fast as opt-in.

A single `lazy` parameter switches mode. The decision is encapsulated in an ErrorHandler object, not scattered across validation code.

---

## Duplication vs abstraction for sync/async

**Duplicate** (httpx, celery, textual, tornado): maintain parallel sync/async classes. ~400 lines of near-duplicate code. Readable, debuggable, no coupling to async framework. Use when paths are simple enough to duplicate without errors.

**Bridge** (flask, anyio, starlette): detect function type at call site, wrap async with `async_to_sync`. No duplication, but overhead of `iscoroutinefunction()` check per call. Use when the pipeline is complex enough that duplication creates maintenance burden.

These are complementary strategies, not competing — httpx duplicates the Client class but bridges individual callbacks.

---

## Public API surface: `__all__` + lazy `__getattr__` vs direct re-export

Use `_internal/` or `_` prefix for private modules (26 projects). `__init__.py` uses `__all__` + lazy `__getattr__` for deferred module loading (pydantic pattern): `import pydantic` doesn't load all 40+ submodules; each symbol is loaded on first access.

Pre-instantiate the main object at module level (7 projects: loguru's `logger`, tornado's `IOLoop.current()`). The module IS the API — users import the object, not a class to instantiate.

---

## Plugin registration: hook spec/impl vs registry vs entry points

**Hook spec/impl** (pluggy, pytest, 12 projects): `@hookspec` defines contract, `@hookimpl` registers implementation. Decorators stamp attributes, don't wrap. Function remains directly callable.

**Registry dict** (5 projects): dict subclass with `__missing__` guard. Simple registration via `registry[name] = cls`. Good for type registries, format handlers.

**Signal/observer** (7 projects): weakref-based callback registry with per-callback exception isolation. Good for event-driven extension where plugins react, not implement contracts.

Use hook spec/impl when plugins provide interchangeable implementations. Use signals when plugins react to events. Use registry when mapping names to types/handlers.

---

## Error object design: structured data vs message strings

Collect errors as **structured data**, not messages (16 projects). Pydantic's `ValidationError.errors()` returns `[{loc, msg, type}]`. Pandera's `SchemaErrors` carries a DataFrame of failure cases.

Base exception carries domain context (request, response, config) and specialized subclasses inherit (16 projects). A `Result` object wraps call outcomes for error isolation — `get_result()` re-raises, `force_result()` suppresses (7 projects: pluggy, celery, pytest).

Errors as control flow (exit signals, warning degradation) are valid for non-error termination (5 projects: click's `ClickException`, hypothesis's warning-on-decorator-exception).

---

## Context propagation: ContextVar vs thread-local vs event-loop-scoped

**ContextVar + LocalProxy** (7 projects, flask, textual): async-safe, transparent proxy delegates attribute access. The modern default — works with asyncio, greenlets, concurrent requests.

**threading.local + Proxy** (celery): pre-ContextVar pattern, sync-only. Still valid for sync-only frameworks.

**RunVar** (anyio): per-event-loop, not per-task. For state shared across all tasks in the same loop (thread pools, caches). Uses WeakKeyDictionary keyed by event loop identity.

**Context manager as lifecycle boundary** (5 projects): `__enter__`/`__exit__` push/pop the context. Teardown always runs (try/finally). This is the pipeline boundary between transport and application.

---

## Pipeline stage boundaries: named steps vs processor chain vs IO manager

**Named step chain** (scikit-learn, 3 projects): `Pipeline([(name, step)])`. Steps addressable via `name__param`. Each step has uniform interface (fit/transform).

**Processor chain** (structlog, 5 projects): linear list of callables, each `(logger, method, event_dict) → event_dict`. Terminal processor breaks dict chain, returns str. Pure functions, composable, testable in isolation.

**IO manager** (dagster, 3 projects): two-method boundary — `load_input(context)` / `handle_output(context, obj)`. IO never touches compute function. Pure serialization boundary.

Use named steps when stages have heterogeneous interfaces. Use processor chain when stages share a uniform signature. Use IO manager when I/O must be separated from computation.

---

## Sentinel vs None vs default value

Use a **sentinel object** to distinguish "not provided" from `None` (15 projects). `None` is a valid value; the sentinel means "no value was given." Implemented as `object()`, `enum.auto()`, or a named class instance.

A **sentinel string** (6 projects, e.g. `'__no__default__'`) works but is fragile — string comparison, not identity. Use only for backwards compatibility.

Never use `val or 0` when 0 is a valid value. Use `val if val is not None else 0`. The sentinel pattern makes this unnecessary — check `if val is SENTINEL` instead.
