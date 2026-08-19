# Python Design — Pattern Glossary

Authoritative definitions for design pattern terms used in `patterns-db.json`. When patterns are merged, the shared concept is recorded here as the canonical term. Subagents consult this glossary to decide whether a "new" pattern is actually an instance of an existing concept.

## How to use

- **Matching**: before reporting `is_new: true`, check if the pattern is an instance of a concept defined here. If it is, match the corresponding pattern ID instead.
- **Merging**: when two patterns are merged, the survivor's concept is updated here; the merged-away pattern's name is recorded as a synonym.
- **Cross-cutting concerns**: see the section below — some concepts appear across multiple dimensions but are not dimensions themselves.

## Concepts

### Sentinel

A dedicated object distinguishing "not provided" from `None`. `None` is a valid value; the sentinel means "no value was given." Implemented as `object()`, `enum.auto()`, or a named class instance. Variations (string sentinel, enum sentinel) are implementation details, not separate patterns.

- Canonical pattern: **P042**
- Merged: P131 (Sentinel enum), P197 (Sentinel string), P267 (Sentinel object)

### Metaclass-driven model construction

Intercepting class creation via metaclass `__new__` to build infrastructure (validators, serializers, field metadata) at definition time. `__init__` becomes a thin delegate. The compiled metadata (e.g. `__attrs_attrs__`, `__pydantic_validator__`) is a class-level singleton, not per-instance.

- Canonical pattern: **P001**
- Merged: P048 (Compiled field metadata as `__attrs_attrs__`)

### Frozen + slots value object

Combining `frozen=True` (immutability) + `slots=True` (no `__dict__`, fixed shape) for value objects. Signals "this is a fixed-shape data object." The `object.__setattr__` bypass for custom `__init__` is a workaround technique, not a separate pattern.

- Canonical pattern: **P003** (also covers P002 msgspec.Struct)
- Merged: P090 (frozen dataclass with `__setattr__` bypass)

### Lazy validation toggle

A single `lazy` parameter or flag switches between fail-fast (raise on first error) and collect-all (aggregate all errors, raise once). The ErrorHandler object that encapsulates this decision is an implementation mechanism, not a separate design decision.

- Canonical pattern: **P007**
- Merged: P008 (ErrorHandler as lazy/eager switch)

### Protocol over ABC

Using `typing.Protocol` for structural subtyping — any class with the right methods satisfies the interface, no inheritance needed. `@runtime_checkable` is a specific capability of this approach, not a separate pattern. Protocol for external interop interfaces (`__array_interface__`, `__arrow_c_array__`) is a specific application.

- Canonical pattern: **P021**
- Merged: P105 (runtime_checkable Protocol), P364 (Protocol for external interop)

### Exception hierarchy with context-carrying base

A base exception class that carries domain context (request, response, config) and a hierarchy of specialized subclasses that inherit and extend that context. PEP-numbered leaf exceptions are a variation in naming, not a separate pattern.

- Canonical pattern: **P096**
- Merged: P134 (Error hierarchy with context-carrying exceptions)

### Error handler lookup by MRO + scope cascade

Error handler registry that walks the MRO of the raised exception type and cascades through scopes (blueprint → app). Dual registries (status code + exception type) and MRO-only walks are subsets of this pattern.

- Canonical pattern: **P071**
- Merged: P380 (MRO walk only), P381 (dual handler registry)

### `__init__` as the parameter contract

The constructor signature IS the parameter schema, discovered via `inspect.signature()`. No `*args`/`**kwargs`. Fitted/learned state uses `_` suffix. Factory functions (e.g. `Image.open`, `Image.new`) are alternative construction paths that still store params via `__init__`.

- Canonical pattern: **P004**

### Thin Python wrappers over compiled core

Python modules are thin re-export layers over a compiled core (C extension or Rust bindings), providing the import surface and `__all__` while all logic lives in the compiled layer. C and Rust bindings are the same pattern.

- Canonical pattern: **P028**
- Merged: P292 (Rust bindings re-export)

### Signal: observer pattern with weak references

A callback registry using weak references to prevent memory leaks, with per-callback exception isolation so one broken handler doesn't crash the dispatch chain. Weakref-based registries and robust dispatch signal systems are the same pattern.

- Canonical pattern: **P058**
- Merged: P307 (Weakref-based callback registry)

### Code generation pipeline

Generate Python source code as strings → `compile()` → `exec()` into a namespace. Used by attrs (method generation), beartype (type-checking wrappers). PEP-dispatched routing and string template constants are internal mechanisms of this pipeline, not separate patterns.

- Canonical pattern: **P040** (original), superseded by **P204** (richer description)
- Merged: P207 (PEP-dispatched code generation), P214 (string template constants)

### `__getstate__`/`__setstate__` for pickleable objects

Making objects with non-pickleable fields survive pickling via `__getstate__`/`__setstate__` or `__reduce__`. Field whitelists and namedtuple `__reduce__` are implementation variations.

- Canonical pattern: **P103**
- Merged: P169 (Picklable namedtuple with `__reduce__`)

### BlockingPortal — sync-to-async bridge

Running an event loop in a separate thread and bridging sync→async via Future-based result transport. TestClient is a specific application of this pattern.

- Canonical pattern: **P117**
- Merged: P378 (TestClient as sync HTTP client bridged to async)

### Convention-based handler dispatch via `__init_subclass__`

Using `__init_subclass__` to auto-register handlers at class definition time, either by naming convention (get/post → HTTP methods) or by scanning for decorated methods. Metaclass-collected handlers are a more explicit mechanism of the same concept.

- Canonical pattern: **P076** (HTTP method dispatch), **P251** (general convention)
- Merged: P262 (metaclass-collected decorated handlers)

### Iterator-first design

Everything returns generators/iterators, materialized on demand. Lazy file loading (`_open` + `load` separation) and deferred execution with optimization flags (LazyFrame) are specific applications.

- Canonical pattern: **P188**
- Merged: P349 (lazy file access), P243 (deferred execution with optimization)

### Backend capability flags

Class-level boolean attributes declaring backend capabilities. Decorators that set `cls._capability = True` are a specific mechanism for the same pattern.

- Canonical pattern: **P060**
- Merged: P273 (stream_request_body decorator as capability flag)

### Virtual base class with `__new__` dispatch

`__new__` dispatches to a backend factory to return a concrete implementation. The fallback case (no event loop → return adapter) is a specific branch of the same dispatch logic.

- Canonical pattern: **P108**
- Merged: P109 (adapter fallback for no-event-loop)

### RcParams as validated config dict

Config as `MutableMapping` + `dict` subclass with write-time validation. Per-key validator function registries are the implementation mechanism, not a separate pattern.

- Canonical pattern: **P304**
- Merged: P305 (per-key validator function registry)

### Optional dependency handling

Gracefully handling optional dependencies. `suppress(ImportError)` for simple cases, lazy proxy modules for sophisticated deferred loading. Both are the same concept at different complexity levels — keep both as variations.

- Canonical pattern: **P235** (sophisticated), **P233** (simple) — kept as variations

## Cross-cutting concerns

Concepts that appear across multiple dimensions but are **not dimensions themselves**. They are implementation techniques or perspectives that every dimension may use. When a pattern's core design decision is one of these, classify by the dimension the decision serves, not by the technique.

### Decorator as implementation technique

Decorators are Python's syntactic tool for many design decisions — registration, validation, interface transformation, lazy wrapping, parameter accumulation. The decorator is usually the **vehicle**, not the **decision**. Classify by what the decorator achieves:

- `@hookimpl` achieves plugin registration → `plugin-architecture`
- `@given` achieves pipeline stage declaration → `pipeline-composition`
- `@deprecated` achieves interface transformation → `interface-design`
- `@setupmethod` achieves lifecycle ordering guard → `error-strategy`

True "decorator-as-design-decision" patterns (where the design decision IS the decorator's API shape — e.g. dual-mode decorator `@deco` vs `@deco(args)`) belong to `interface-design`.

### Lifecycle as a perspective

Every dimension has lifecycle aspects — when to register, when to validate, when to initialize, when to tear down. "Lifecycle" describes **when** things happen, but the design decision is about **what** is being managed. Classify by what is being managed:

- Plugin registration timing → `plugin-architecture`
- Validation execution order → `validation`
- Resource setup/teardown → `pipeline-composition` or `state-context`
- Class-definition-time computation → `data-modeling`

"Lifecycle management" is not a separate dimension because pulling it out would scatter each system's lifecycle across two places — the system's dimension and the lifecycle dimension.

### Dimensions overview

The 11 dimensions of the patterns database:

| Dimension | Core question |
|-----------|--------------|
| `data-modeling` | How to represent domain data with types? |
| `validation` | How to validate inputs and collect errors? |
| `error-strategy` | Fail-fast vs collect-all? Error object design? |
| `pipeline-composition` | How to chain stages with type boundaries? |
| `interface-design` | Protocol vs ABC? Surface size? Adapter patterns? |
| `module-organization` | Public vs internal? File granularity? Import discipline? |
| `plugin-architecture` | How to allow extension without modification? |
| `config-management` | How to layer and validate configuration? |
| `serialization` | How to convert between objects and bytes/JSON? |
| `sync-async` | How to offer dual interfaces? Async semantics? |
| `state-context` | How to propagate context implicitly through the call stack? |
