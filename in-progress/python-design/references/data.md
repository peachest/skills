## Data Modeling, Validation, Serialization (16 patterns)

### Metaclass-driven model construction
`P001` · 6 occurrences · 5 projects: attrs, pydantic, sqlalchemy, jinja2, polars

**What**: A metaclass (or equivalent class decorator with a builder) intercepts class creation to compile field metadata, validators, and serializers once at definition time, so `__init__` becomes a thin delegate to precomputed structure.

**Recognize**: How to identify this pattern in code. List 2-4 concrete signals:
- A metaclass subclassing `type`/`ABCMeta` overrides `__new__`/`__init__` and calls a `complete_model_class`/builder before returning the class
- A class decorator (`@attrs`, `@define`) returns `builder.build_class()` after calling `add_init`/`add_eq`/`add_repr`
- A class-level compiled-metadata attribute appears as a tuple (e.g. `__attrs_attrs__`, `__pydantic_validator__`, `__pydantic_fields__`)
- `__init__` is generated code that assigns from positional/keyword args with no per-instance schema discovery

**Why**: Compiled field metadata stored as a class-level singleton makes introspection (`fields()`, `has()`, `asdict()`) O(1) — it reads a precomputed tuple instead of re-scanning `__annotations__` or `inspect.signature`. The named-property tuple subclass allows both index access (`fields(Cls)[0]`) and name access (`fields(Cls).x`). Benefit: one-time compile cost, constant-time introspection, consistent generated dunder methods. Cost: class definition becomes slower and harder to debug — the metaclass is invisible machinery that surprises users expecting plain classes.

**When**: Use when building a library that derives multiple behaviors (validation, serialization, equality, hashing) from a declarative field list and introspects fields frequently at runtime.

**When not**: For plain data holders with no derived behavior, prefer `@dataclass(frozen=True, slots=True)` (P003) directly — a metaclass adds indirection with no payoff.

**Without this pattern** (anti-pattern):
```python
# ❌ Bad: metadata recomputed on every introspection; __init__ hand-written
class User:
    def __init__(self, name, age):
        self.name = name
        self.age = age

def fields(cls):
    # Re-scan __annotations__ every call — O(n) per introspection
    return list(cls.__annotations__.keys())

def asdict(inst):
    return {name: getattr(inst, name) for name in fields(type(inst))}
```

**With this pattern**:
```python
# pydantic — pydantic/_internal/_model_construction.py:75-100
# ✅ Good: metaclass compiles field metadata once at class-definition time
class ModelMetaclass(ABCMeta):
    def __new__(mcs, cls_name, bases, namespace, **kwargs):
        ...
        complete_model_class(cls, ...)
```

### @dataclass(frozen=True, slots=True) as validator container
`P003` · 10 occurrences · 8 projects: attrs, pydantic, hypothesis, aiohttp, pytest, textual, anyio, werkzeug

**What**: Value objects that carry no behavior beyond identity are declared as `@dataclass(frozen=True, slots=True)` (or `@attrs(slots=True, frozen=True)`), signaling a fixed-shape, immutable data object.

**Recognize**: How to identify this pattern in code. List 2-4 concrete signals:
- `@dataclasses.dataclass(frozen=True, slots=True)` (or `@attrs(slots=True, frozen=True)`) decorates a class whose fields are all typed
- The class holds configuration/validator/marker state (e.g. `AfterValidator`, `FixtureFunctionMarker`) rather than domain logic
- No methods mutate `self`; instances are constructed once and compared by value
- Instances are hashable and usable as dict keys / shared defaults

**Why**: `frozen=True` makes instances hashable and safe to share as keys/defaults; `slots=True` prevents accidental attribute creation, shrinks memory, and signals "this is a fixed-shape data object." Benefit: immutability guarantees + memory efficiency + clear intent. Cost: cannot subclass flexibly (slots inheritance is fiddly) and cannot add ad-hoc attributes during debugging.

**When**: Use for configuration markers, validator specs, and small value objects whose shape is known at design time and should not change after construction.

**When not**: For objects that must evolve state over their lifetime, use a mutable dataclass or plain class; for objects needing rich validation/serialization, use a metaclass-driven model (P001).

**Without this pattern** (anti-pattern):
```python
# ❌ Bad: mutable holder; no shape guarantee; accidentally extensible
class AfterValidator:
    def __init__(self, func):
        self.func = func
        # callers can later do v.extra = 1 — no protection, not hashable
```

**With this pattern**:
```python
# pydantic — pydantic/functional_validators.py:24-310
# ✅ Good: frozen+slots signals a fixed-shape immutable value object
@dataclasses.dataclass(frozen=True, slots=True)
class AfterValidator:
    func: ...
```

### __init__ as the parameter contract
`P004` · 25 occurrences · 21 projects: attrs, Pillow, tornado, pytest, scikit-learn, click, toolz, jinja2, celery, beartype, hypothesis, more-itertools, flask, polars, aiohttp, textual, cryptography, requests, loguru, starlette, uvicorn

**What**: The constructor signature IS the parameter schema, discovered via `inspect.signature()`; there is no `*args`/`**kwargs` catch-all, and fitted/learned state uses a `_` suffix.

**Recognize**: How to identify this pattern in code. List 2-4 concrete signals:
- `__init__` lists every parameter explicitly with defaults; no `**kwargs` swallowing unknown args
- Configuration is introspected via `inspect.signature(self.__init__)` (e.g. scikit-learn clones params from the signature)
- Learned/fitted state is stored on attributes suffixed with `_` (e.g. `self.coef_`)
- Factory functions (`Image.open`, `Image.new`) are alternative construction paths that still funnel parameters through `__init__`

**Why**: Making the signature the single source of truth means tooling, cloning, and documentation all read one place — `get_params()` reflects `inspect.signature` automatically, and there's no hidden state outside the declared parameters. Benefit: introspectable, cloneable, self-documenting APIs. Cost: every parameter must be explicit (verbose signatures) and you cannot silently accept forward-compatible kwargs.

**When**: Use for objects whose parameters must be introspectable and cloneable — estimators, configurable services, anything where `get_params()`/`set_params()` matters.

**When not**: For thin proxies or wrappers that genuinely forward arbitrary kwargs, accept `**kwargs` deliberately and document the contract rather than forcing an exhaustive signature.

**Without this pattern** (anti-pattern):
```python
# ❌ Bad: signature hides the real schema; not introspectable or cloneable
class LogisticRegression:
    def __init__(self, **kwargs):
        self._params = kwargs  # what params exist? tooling can't tell

    def get_params(self):
        return dict(self._params)  # ad hoc, not tied to signature
```

**With this pattern**:
```python
# scikit-learn — sklearn/base.py:223-241
# ✅ Good: the signature IS the schema — no separate param definition
def __init__(self, penalty='l2', *, C=1.0):
    self.penalty = penalty
    self.C = C
# get_params() reflects inspect.signature(__init__) — no separate schema
```

### __slots__ everywhere for value objects
`P005` · 25 occurrences · 17 projects: attrs, celery, beartype, hypothesis, tornado, aiohttp, pytest, jinja2, click, textual, pluggy, loguru, toolz, more-itertools, anyio, sqlalchemy, werkzeug

**What**: Every value-object class declares `__slots__`, preventing accidental attribute creation, reducing per-instance memory, and signaling a fixed-shape data object.

**Recognize**: How to identify this pattern in code. List 2-4 concrete signals:
- `__slots__ = ('field1', 'field2', ...)` appears as the first body statement of a class
- Even small internal classes (`HookImpl`, `Factory`, `Converter`, `Proxy`) define `__slots__`
- Assigning an undeclared attribute raises `AttributeError`
- No per-instance `__dict__`

**Why**: `__slots__` eliminates the per-instance `__dict__`, cutting memory roughly in half for many small objects, and turns typo/attribute-creation bugs into immediate `AttributeError`s. Benefit: memory + safety + intent signaling. Cost: cannot add attributes dynamically (harder for interactive debugging, pickling needs care), and slots inheritance rules are subtle.

**When**: Use for high-cardinality internal value objects (hook impls, validators, proxies, markers) where instances number in the thousands or millions.

**When not**: For classes that need dynamic attributes (ORM-mapped objects, debug-friendly user models), or where pickling/inheritance complexity outweighs memory savings; prefer a plain class or `@dataclass` without slots.

**Without this pattern** (anti-pattern):
```python
# ❌ Bad: every instance carries a __dict__; typos silently create attributes
class HookImpl:
    def __init__(self, function, plugin_name):
        self.function = function
        self.plugin_name = plugin_name

impl = HookImpl(fn, "myplugin")
impl.funtion = None  # typo — silently creates a new attribute, no error
```

**With this pattern**:
```python
# pluggy — pluggy/_hooks.py
# ✅ Good: __slots__ locks the shape and drops the per-instance __dict__
class HookImpl:
    __slots__ = ('function', 'plugin_name', ...)
```

### Input validation via check_array / validate_params
`P009` · 5 occurrences · 4 projects: attrs, scikit-learn, hypothesis, cryptography

**What**: Two-tier validation: a decorator-based parameter validator checks hyperparameters once (at call time), while a runtime `check_X_y`/`check_array` validates input data shapes and types on every call.

**Recognize**: How to identify this pattern in code. List 2-4 concrete signals:
- `@validate_params({'X': ['array-like']})` decorates a method, declaring expected param types
- A `check_X_y(X, y)` / `check_array(X)` call appears at the top of `fit`/`transform`
- `@check_function` wraps internal helpers that raise `InvalidArgument` with a formatted message
- Validator factories (`instance_of(type)`, `deep_iterable(...)`) return callable validator objects

**Why**: Separating hyperparameter validation (decorator, declared once) from input validation (runtime, per-call) keeps the method body focused on logic while still failing fast with clear messages. Benefit: declarative param contracts + runtime data guards + consistent error formatting. Cost: two validation code paths to maintain, and the decorator overhead runs on every call.

**When**: Use for APIs where hyperparameters are stable but input data varies per call (estimators, hypothesis strategies, attrs validators).

**When not**: For pure functions with trivial inputs, inline asserts suffice; for schema-driven validation, prefer types-as-schemas (P010).

**Without this pattern** (anti-pattern):
```python
# ❌ Bad: validation mixed into logic, repeated and inconsistent
def fit(self, X, y):
    if not isinstance(X, list):
        raise ValueError("X must be a list")  # ad hoc, repeated everywhere
    if y is None:
        raise ValueError("y required")
    # ... logic interleaved with checks, no separation
```

**With this pattern**:
```python
# scikit-learn — sklearn/utils/validation.py
# ✅ Good: decorator declares param types; check_X_y validates data at runtime
@validate_params({'X': ['array-like']})
def fit(self, X, y):
    X, y = check_X_y(X, y)
```

### Types as schemas — no separate schema object
`P010` · 3 occurrences · 3 projects: attrs, msgspec, beartype

**What**: The type annotation IS the schema — there is no separate `Schema()`/`Model()`/`Field()` definition step; the decoder/validator reads annotations directly.

**Recognize**: How to identify this pattern in code. List 2-4 concrete signals:
- A decoder is constructed from a bare type: `msgspec.json.Decoder(list[Point | None])`
- A decorator (`@beartype`, `@attrs(auto_attribs=True)`) reads `__annotations__` and generates checking code
- No `Schema(...)` class is instantiated; the generic type parameter carries the shape
- Validation/serialization is dispatched from the annotation, not from a parallel schema object

**Why**: One source of truth — the type — drives validation, serialization, and documentation, eliminating the drift between a model and its schema. Benefit: no duplication; type checkers and runtime share the same spec. Cost: the annotation language must be expressive enough (generic aliases, `|` unions), and custom validation rules that don't map to types still need escape hatches.

**When**: Use when your types already fully describe the data shape (PEP 604 unions, generics) and you want runtime checking without a parallel schema layer.

**When not**: When validation rules are richer than types express (cross-field constraints, conditional rules), use an explicit validator model (P001 / P009).

**Without this pattern** (anti-pattern):
```python
# ❌ Bad: a parallel schema object that must be kept in sync with the type
class Point:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

class PointSchema:           # duplicates Point's shape — drifts easily
    fields = {"x": float, "y": float}

def decode(data):
    return Point(data["x"], data["y"])  # no validation, manual mapping
```

**With this pattern**:
```python
# msgspec — msgspec/json.pyi:49-73
# ✅ Good: the bare type is the schema — no separate Schema() object
dec = msgspec.json.Decoder(list[Point | None])
points = dec.decode(data)
```

### model_dump() / model_dump_json() with mode selection
`P035` · 3 occurrences · 3 projects: attrs, pydantic, pytest

**What**: Separate the Python-native dump (`model_dump()` → `dict`) from the JSON dump (`model_dump_json()` → `str`), with include/exclude, `by_alias`, and `exclude_unset` controls; the serializer is built once at class definition time.

**Recognize**: How to identify this pattern in code. List 2-4 concrete signals:
- `model.model_dump(indent=2, exclude={'password'})` returns a `dict`; `model_dump_json()` returns a `str`
- An `asdict(inst, recurse=True, filter=..., value_serializer=...)` function recurses through attrs fields
- Serialization respects field metadata (aliases, excluded fields) rather than dumping raw `__dict__`
- The serializer is compiled at class-definition time, not rebuilt per call

**Why**: Splitting dict-dump from JSON-dump lets callers get mutable Python structures for further processing or a lossless JSON string for transport, both honoring the same field controls. Benefit: one declarative field spec drives both outputs; callers choose the representation. Cost: two methods to maintain and the serializer-build adds class-definition cost.

**When**: Use when models must round-trip to both Python dicts (templating/testing) and JSON (APIs/storage) with consistent field filtering.

**When not**: For objects whose only serialization target is JSON, a single `to_json()` suffices; for opaque binary state crossing process boundaries, use `__getstate__`/`__setstate__` (P103).

**Without this pattern** (anti-pattern):
```python
# ❌ Bad: dump leaks internals; dict and JSON handled ad hoc, inconsistent
class User:
    def to_dict(self):
        return self.__dict__  # leaks password, includes private fields

    def to_json(self):
        import json
        return json.dumps(self.__dict__)  # duplicated logic, no field control
```

**With this pattern**:
```python
# pydantic — pydantic/main.py
# ✅ Good: dict-dump and JSON-dump share field controls (exclude, indent)
# model_dump() → dict; model_dump_json() → str — same field controls
model.model_dump(indent=2, exclude={'password'})
```

### Sentinel object for distinguishing 'no value' from None
`P042` · 21 occurrences · 17 projects: attrs, beartype, Pillow, hypothesis, tornado, setuptools, jinja2, aiohttp, click, textual, sqlalchemy, more-itertools, starlette, anyio, jsonschema, werkzeug, polars

**What**: A dedicated sentinel object (commonly an `enum.Enum` member, or `object()`) is used as the default for optional fields where `None` is itself a valid user-supplied value, so "not provided" is distinguishable from "explicitly None."

**Recognize**: How to identify this pattern in code. List 2-4 concrete signals:
- A module-level sentinel: `NOTHING = _Nothing.NOTHING` (enum) or `undefined = object()`
- The sentinel has a custom `__repr__` (returns `"NOTHING"`) and is often falsy (`__bool__` → `False`)
- A `Literal[Sentinel.UNSET]` type alias annotates parameters so type checkers see the sentinel option
- Callers compare with `is` (`if default is NOTHING`), never `==`

**Why**: When `None` is a legitimate value (e.g. `autoescape=None` means "disable escaping"), a plain `default=None` is ambiguous — you can't tell whether the user chose `None` or omitted the argument. A sentinel is identity-comparable (`is _UNSET`), has no false-positive collisions, and self-documents intent via its type annotation. An enum variant (vs bare `object()`) gives stable identity for pickling and a meaningful repr in errors. Benefit: disambiguates "unset" from "None" with zero collision risk. Cost: one extra symbol per parameter and callers must remember to use `is`.

**When**: Use whenever `None` is a semantically valid value and you need to detect "argument omitted."

**When not**: When `None` is never a valid value, just use `None` as the default — the sentinel adds noise. For a picklable, self-describing default across module/process boundaries, the string-sentinel variant (P197) is an alternative.

**Without this pattern** (anti-pattern):
```python
# ❌ Bad: None is ambiguous — can't tell "unset" from "user passed None"
def render(template, autoescape=None):
    if autoescape is None:
        autoescape = True  # but what if the user *meant* None == disable?
    # caller passing autoescape=None silently becomes True — wrong
```

**With this pattern**:
```python
# attrs — src/attr/_make.py:60-87
# ✅ Good: enum sentinel distinguishes 'unset' from an explicit None
class _Nothing(enum.Enum):
    NOTHING = enum.auto()
    def __repr__(self):
        return "NOTHING"
    def __bool__(self):
        return False

NOTHING = _Nothing.NOTHING
NothingType = Literal[_Nothing.NOTHING]
```

### evolve() for non-destructive immutable updates
`P049` · 10 occurrences · 9 projects: attrs, cryptography, aiohttp, textual, loguru, sqlalchemy, more-itertools, jinja2, jsonschema

**What**: `evolve(inst, **changes)` creates a new instance of the same class with specified fields overridden, reading unchanged field values from the original via `getattr` and constructing via `cls(**changes)`; works for both frozen and mutable classes.

**Recognize**: How to identify this pattern in code. List 2-4 concrete signals:
- A function `evolve(inst, **changes)` (or a `bind`/`patch`/`opt` method) returns a new instance rather than mutating `self`
- It iterates compiled field metadata (`fields(cls)`) to fill in unchanged fields from the original
- The class is frozen/immutable, so in-place update is impossible
- `redefine`/`remove` methods return `evolve(self, ...)` — copy-on-modify style

**Why**: Frozen classes can't be updated in place, yet you still need to "change" a field. `evolve()` provides a functional copy-with-changes that reads compiled field metadata to know which fields to copy and which to override. Benefit: immutable safety with ergonomic updates; the original stays valid for any code holding a reference. Cost: allocates a new object per update (more GC pressure than mutation) and requires init-time field metadata.

**When**: Use with frozen value objects (P003) whenever a derived or updated value is needed.

**When not**: For mutable objects, just assign `obj.x = new_x`; for builder-style fluent mutation, prefer a mutable builder separate from the immutable result.

**Without this pattern** (anti-pattern):
```python
# ❌ Bad: frozen object "updated" by reaching past the freeze — fragile and unsafe
import dataclasses

@dataclasses.dataclass(frozen=True)
class Point:
    x: float
    y: float

p = Point(1, 2)
object.__setattr__(p, 'x', 3)  # bypasses immutability — breaks invariants, surprising
```

**With this pattern**:
```python
# attrs — src/attr/_make.py:587-620
# ✅ Good: evolve() returns a new frozen instance with overrides applied
def evolve(*args, **changes):
    (inst,) = args
    cls = inst.__class__
    attrs = fields(cls)
    for a in attrs:
        if not a.init:
            continue
        attr_name = a.name
        init_name = a.alias
        if init_name not in changes:
            changes[init_name] = getattr(inst, attr_name)
    return cls(**changes)
```

### TypedDict-style protocol aliases for callback contracts
`P078` · 4 occurrences · 4 projects: flask, hypothesis, aiohttp, uvicorn

**What**: Framework callback signatures are defined as type aliases (often `Union` of sync and `Callable[..., Awaitable]` async variants, or `TypedDict`s for event scopes) in a dedicated `typing.py` module, then used as parameter types throughout the codebase — documentation and type-checking with zero runtime overhead.

**Recognize**: How to identify this pattern in code. List 2-4 concrete signals:
- A `typing.py`/`_types.py` module centralizes aliases like `BeforeRequestCallable`, `ASGIReceiveCallable`
- Aliases are `Union[Callable[...], Callable[..., Awaitable[...]]]` (sync + async variants)
- `TypedDict` subclasses with `Literal` discriminators define event/scope shapes (`HTTPScope`, `HTTPRequestEvent`)
- A `TypeAlias` aggregates several constraint dicts (`ChoiceConstraintsT = A | B | C`)

**Why**: Callback contracts are the framework's API surface — aliases make them explicit, machine-checkable, and self-documenting; the sync/async `Union` documents that both are accepted. Centralizing in one file gives users a single place to read the full callback API and lets aliases evolve (e.g. adding async) without touching call sites. Benefit: typed, discoverable, runtime-free contracts. Cost: an extra module to keep in sync and a learning curve for the Union-of-Callable form.

**When**: Use for framework callback/extension points and protocol message shapes (ASGI events) that users implement and the framework dispatches.

**When not**: For internal-only helper signatures, inline annotations are simpler; for runtime-enforced interfaces, use a `Protocol` (P021).

**Without this pattern** (anti-pattern):
```python
# ❌ Bad: callback contract buried in the handler; no reuse, no type-checking
def add_before_request(self, fn):
    self.before_request_funcs.append(fn)
    # what signature must fn have? sync or async? undocumented, untyped

def add_after_request(self, fn):
    self.after_request_funcs.append(fn)
    # duplicated, ad hoc — each site re-derives the contract
```

**With this pattern**:
```python
# flask — src/flask/typing.py:1-95
# ✅ Good: callback contracts as Union-of-Callable aliases, zero runtime cost
BeforeRequestCallable = t.Union[
    t.Callable[[], t.Optional[ResponseReturnValue]],
    t.Callable[[], t.Awaitable[t.Optional[ResponseReturnValue]]],
]

AfterRequestCallable = t.Union[
    t.Callable[[ResponseClass], ResponseClass],
    t.Callable[[ResponseClass], t.Awaitable[ResponseClass]],
]
```

### ImmutableDict for framework defaults
`P079` · 6 occurrences · 6 projects: setuptools, hypothesis, sqlalchemy, starlette, flask, werkzeug

**What**: Framework-wide default configurations and options use an `ImmutableDict` (a `dict`/`Mapping` subclass that raises `TypeError` on mutation), so class-level defaults like `default_config` are read-only templates to be copied, never mutated in place.

**Recognize**: How to identify this pattern in code. List 2-4 concrete signals:
- `default_config = ImmutableDict({...})` appears as a class attribute
- `__setitem__`/`__delitem__` (and `update`, `pop`) raise `TypeError`/`AttributeError`
- A metaclass `__setattr__` raises `AttributeError` for non-underscore names ("the settings class is immutable")
- `ImmutableMultiDict` is a `Mapping` subclass; mutation lives only in the mutable `MultiDict` subclass

**Why**: Class attributes are shared across all instances — if `default_config` were a plain `dict`, mutating it in one instance would corrupt every other instance. `ImmutableDict` prevents this at the language level: the only way to customize is to copy and modify, which is the correct pattern. It also signals intent to readers: this value is a specification, not a working copy. Benefit: shared-default safety enforced structurally. Cost: callers must copy before modifying (extra step) and the immutability can surprise users expecting dict semantics.

**When**: Use for class-level default templates and global option registries that are shared and must not be mutated by instance code.

**When not**: For per-instance working state that is meant to be mutated, use a plain dict copied from the immutable default in `__init__`.

**Without this pattern** (anti-pattern):
```python
# ❌ Bad: shared mutable default — one instance corrupts all others
class App:
    default_config = {"DEBUG": False, "SECRET_KEY": None}

a = App()
a.default_config["DEBUG"] = True        # mutates the CLASS attribute
b = App()
print(b.default_config["DEBUG"])        # True — leaked across instances!
```

**With this pattern**:
```python
# flask — src/flask/app.py:185-220
# ✅ Good: ImmutableDict makes the shared default copy-only, not mutate-in-place
from werkzeug.datastructures import ImmutableDict

class Flask(App):
    default_config = ImmutableDict({
        "DEBUG": None,
        "TESTING": False,
        "SECRET_KEY": None,
        "PERMANENT_SESSION_LIFETIME": timedelta(days=31),
        "SESSION_COOKIE_NAME": "session",
        "MAX_CONTENT_LENGTH": None,
        # ... 30+ keys
    })
```

### Type-safe heterogeneous container (StashKey + Stash)
`P082` · 3 occurrences · 3 projects: anyio, aiohttp, pytest

**What**: A `Stash` is a dict-like container keyed by `StashKey[T]` objects (opaque `Generic[T]` instances with no value); each key is bound to type `T` at definition time, so `__getitem__` returns `T`, letting plugins attach private typed data to shared objects without modifying their class definitions.

**Recognize**: How to identify this pattern in code. List 2-4 concrete signals:
- `class StashKey(Generic[T]): __slots__ = ()` — opaque key with no `__eq__`/`__hash__` override (identity-based)
- `stash[key] = value` / `stash[key]` where `key: StashKey[T]` and the return is typed `T`
- Module-level `StashKey` instances created by plugins (`my_key = StashKey[int]()`)
- `TypedAttributeSet`/`AppKey` variants: class-level descriptors that yield unique typed keys

**Why**: A plain `dict` with string keys has no type safety and risks collisions between plugins. `StashKey` objects are unique by identity (no `__eq__`/`__hash__` override), so different modules cannot accidentally collide, and the `Generic[T]` parameter lets type checkers infer the return type from the key. Benefit: type-safe, collision-free plugin data attachment without subclassing. Cost: callers must hold a `StashKey` reference; less discoverable than named attributes.

**When**: Use when multiple independent plugins need to attach private, typed data to a shared framework object (`Config`, `Node`, request scope).

**When not**: For a fixed, known set of attributes, just use typed class attributes or a `dataclass`; the stash is for open-ended extension.

**Without this pattern** (anti-pattern):
```python
# ❌ Bad: string keys collide and are untyped
class Config:
    def __init__(self):
        self._stash = {}

config = Config()
config._stash["timeout"] = 30      # plugin A
config._stash["timeout"] = "30s"   # plugin B — collision! silent overwrite, type unknown
value: int = config._stash["timeout"]  # type checker can't verify
```

**With this pattern**:
```python
# pytest — src/_pytest/stash.py:16-75
# ✅ Good: StashKey[T] gives type-safe, collision-free plugin data attachment
class StashKey(Generic[T]):
    """A StashKey is associated with the type T of the value of the key."""
    __slots__ = ()

class Stash:
    __slots__ = ("_storage",)
    def __init__(self) -> None:
        self._storage: Dict[StashKey[Any], object] = {}
    def __setitem__(self, key: StashKey[T], value: T) -> None:
        self._storage[key] = value
    def __getitem__(self, key: StashKey[T]) -> T:
        return cast(T, self._storage[key])
```

### Ordered enum with navigation methods
`P089` · 7 occurrences · 7 projects: cryptography, beartype, Pillow, setuptools, pytest, textual, anyio

**What**: An `Enum` decorated with `@total_ordering` defines a semantically ordered set (e.g. fixture scopes) with `__lt__` based on a declaration-order index, plus navigation helpers (`next_lower()`, `next_higher()`) and a `from_user()` classmethod that converts strings to members with context-rich errors.

**Recognize**: How to identify this pattern in code. List 2-4 concrete signals:
- `@total_ordering` on an `Enum`/`IntEnum` with a `__lt__` keyed off a declaration-order index
- Navigation methods: `next_lower()`, `next_higher()` returning adjacent members
- A `from_user(value, *, where=...)` classmethod raises a friendly error naming where conversion happened
- Members carry a value alias (e.g. `Function = "function"`) mapping user-facing strings to enum members

**Why**: Fixture scopes form a containment hierarchy — a session-scoped fixture must be set up before any module-scoped one and torn down after all. An ordered enum with navigation lets the framework compare scopes (`scope_a < scope_b`), find adjacent scopes for caching decisions, and convert user strings to enums with context-rich errors. `@total_ordering` derives all comparisons from `__lt__` + `__eq__` for free. Benefit: declarative ordering + safe string conversion + rich errors. Cost: the index map must stay in sync with member order, and `@total_ordering` adds reflection overhead on comparisons.

**When**: Use for any enumerated set with a meaningful total order and user-facing string input that needs friendly conversion (scopes, levels, statuses).

**When not**: For unordered enumerations or simple flag sets, a plain `Enum`/`IntFlag` is clearer and cheaper.

**Without this pattern** (anti-pattern):
```python
# ❌ Bad: ordering re-derived by hand; string conversion with no context
SCOPE_ORDER = ["function", "class", "module", "package", "session"]

def is_wider(a, b):
    return SCOPE_ORDER.index(a) > SCOPE_ORDER.index(b)  # O(n) scan, typo-prone

def from_user(s):
    if s not in SCOPE_ORDER:
        raise ValueError(f"bad scope {s}")  # no context on *where* it failed
    return s
```

**With this pattern**:
```python
# pytest — src/_pytest/scope.py:18-60
# ✅ Good: @total_ordering + index gives ordered scopes with navigation
@total_ordering
class Scope(Enum):
    Function: "_ScopeName" = "function"
    Class: "_ScopeName" = "class"
    Module: "_ScopeName" = "module"
    Package: "_ScopeName" = "package"
    Session: "_ScopeName" = "session"

    def next_lower(self) -> "Scope":
        index = _SCOPE_INDICES[self]
        if index == 0:
            raise ValueError(f"{self} is the lower-most scope")
        return _ALL_SCOPES[index - 1]

    def __lt__(self, other: "Scope") -> bool:
        return _SCOPE_INDICES[self] < _SCOPE_INDICES[other]
```

### Immutable invocation spec with copy-on-modify
`P092` · 3 occurrences · 3 projects: jsonschema, loguru, pytest

**What**: A `@dataclass(frozen=True)` spec (e.g. `CallSpec2`) represents a planned invocation; `setmulti()` returns a NEW spec with updated fields instead of mutating `self`, so multiple parametrize calls compose as a cartesian product of immutable specs.

**Recognize**: How to identify this pattern in code. List 2-4 concrete signals:
- `@dataclasses.dataclass(frozen=True)` on a spec/marker class with dict-typed fields
- An updater method (`setmulti`, `redefine`, `opt`, `bind`) returns a new instance, copying internal dicts before mutating the copy
- Methods use `evolve(self, ...)` or construct `cls(...)` explicitly with copied state
- Multiple updates compose multiplicatively (cartesian product of specs)

**Why**: Parametrization is multiplicative — `@parametrize('x',[1,2])` then `@parametrize('y',[3,4])` yields 4 invocations. Copy-on-modify makes this clean: for each existing spec, create a new spec per new value. If specs were mutable, the cartesian product would require careful cloning to avoid aliasing bugs; freezing prevents accidental post-collection mutation that would break test isolation. Benefit: composable, aliasing-free multiplicative builds; post-build immutability guarantees isolation. Cost: allocates O(n·m) specs and copies dicts on each update.

**When**: Use when building collections of invocation/config specs via repeated multiplicative updates, especially where isolation between specs matters.

**When not**: For a single mutable config object built incrementally, a plain mutable dataclass is simpler; for updates to a single frozen instance, `evolve()` (P049) suffices.

**Without this pattern** (anti-pattern):
```python
# ❌ Bad: mutable spec shared across the cartesian product — aliasing bug
class CallSpec:
    def __init__(self):
        self.params = {}

    def setmulti(self, arg, val):
        self.params[arg] = val      # mutates self — all references see the change
        return self                 # returns same object, no copy

base = CallSpec()
a = base.setmulti("x", 1)
b = base.setmulti("x", 2)
print(a.params["x"])  # 2 — a and b alias the same object!
```

**With this pattern**:
```python
# pytest — src/_pytest/python.py:1114-1170
# ✅ Good: setmulti() copies and returns a new frozen spec — no aliasing
@dataclasses.dataclass(frozen=True)
class CallSpec2:
    funcargs: Dict[str, object] = dataclasses.field(default_factory=dict)
    params: Dict[str, object] = dataclasses.field(default_factory=dict)

    def setmulti(self, *, valtypes, argnames, valset, id, marks, scope, param_index) -> "CallSpec2":
        funcargs = self.funcargs.copy()
        params = self.params.copy()
        for arg, val in zip(argnames, valset):
            if valtypes[arg] == 'params':
                params[arg] = val
            else:
                funcargs[arg] = val
        return CallSpec2(funcargs=funcargs, params=params, ...)
```

### __getstate__/__setstate__ for pickleable objects with non-pickleable internals
`P103` · 20 occurrences · 12 projects: beartype, Pillow, hypothesis, tornado, requests, loguru, sqlalchemy, more-itertools, starlette, jinja2, werkzeug, polars

**What**: Objects with non-pickleable internals (sockets, pool managers, `threading.local`) define `__getstate__`/`__setstate__` (or `__reduce__`) using a `__attrs__` whitelist of serializable field names; `__getstate__` extracts only those, and `__setstate__` restores them while re-initializing the non-pickleable parts from stored config.

**Recognize**: How to identify this pattern in code. List 2-4 concrete signals:
- `__attrs__ = ["headers", "cookies", ...]` class attribute lists picklable fields
- `__getstate__` returns `{attr: getattr(self, attr) for attr in self.__attrs__}`
- `__setstate__` restores fields and re-creates non-pickleable internals (`threading.local()`, `PoolManager(...)`)
- `__reduce__` returns `(type(self), (args,))` to degrade gracefully when tracebacks/frames can't pickle

**Why**: HTTP clients, loggers, and exception records contain non-pickleable objects (socket connections, urllib3 `PoolManager`, `threading.local`, tracebacks). But users need to pickle them for multiprocessing, caching, or cross-process logging. The `__attrs__` whitelist ensures only serializable state survives, while `__setstate__` reconstructs the rest from stored config; `__reduce__` degrades gracefully — preserving type and value, dropping what can't pickle. Benefit: pickle survives process boundaries with controlled, whitelisted state. Cost: the whitelist must be maintained (new fields won't pickle unless added) and reconstruction logic must rebuild valid internal state.

**When**: Use for objects that mix serializable config with non-pickleable runtime resources and must cross process boundaries.

**When not**: For purely serializable data objects, default pickling works — don't add `__getstate__`/`__setstate__`. For structured dict/JSON export, use `model_dump` (P035).

**Without this pattern** (anti-pattern):
```python
# ❌ Bad: pickling the whole object fails on the non-pickleable connection
class Session:
    def __init__(self):
        self.headers = {}
        self._pool = urllib3.PoolManager()  # not pickleable

import pickle
pickle.dumps(Session())  # TypeError: can't pickle PoolManager
```

**With this pattern**:
```python
# requests — src/requests/sessions.py:760-770
# ✅ Good: __attrs__ whitelist pickles only serializable state, rebuilds the rest
class Session(SessionRedirectMixin):
    __attrs__ = ["headers", "cookies", "auth", "proxies", "hooks",
                 "params", "verify", "cert", "adapters", "stream",
                 "trust_env", "max_redirects"]

    def __getstate__(self) -> dict[str, Any]:
        return {attr: getattr(self, attr, None) for attr in self.__attrs__}

    def __setstate__(self, state: dict[str, Any]) -> None:
        for attr, value in state.items():
            setattr(self, attr, value)
```

### Sentinel string as module-level default marker
`P197` · 6 occurrences · 5 projects: beartype, Pillow, toolz, more-itertools, starlette

**What**: A module-level sentinel string (e.g. `no_default = '__no__default__'`) distinguishes "no value provided" from `None` (which is a valid default); functions check `if default is no_default` to detect whether the caller passed a default at all.

**Recognize**: How to identify this pattern in code. List 2-4 concrete signals:
- A module-level string constant: `no_default = '__no__default__'`
- An integer magic constant: `ARG_VALUE_UNPASSED = 0xBABECAFE` annotated with `Literal`
- Comparison via `is`/`==` against the sentinel, with `None` treated as a valid value
- Self-describing value visible in tracebacks (unlike `object()`)

**Why**: Python's `None`-as-default convention breaks when `None` is a valid value. The string sentinel is simple, picklable, and visible in tracebacks — unlike `object()` sentinels (which require module-level singletons and aren't picklable). It survives serialization, so it works across module/process boundaries. Benefit: picklable, self-describing "unset" marker usable across boundaries. Cost: a magic string/integer that could (in theory) collide with a real user value, and less type-safety than the enum sentinel (P042).

**When**: Use when you need a picklable, serialization-safe "unset" marker and `None` is a valid value, especially across module/process boundaries.

**When not**: For strong identity guarantees and zero collision risk, prefer the enum sentinel (P042); when `None` is never valid, just use `None`.

**Without this pattern** (anti-pattern):
```python
# ❌ Bad: None can't distinguish "unset" from "user passed None"
def nth(iterable, n, default=None):
    if default is None:
        default = []  # caller passing default=None silently gets [] — wrong
    ...
```

**With this pattern**:
```python
# toolz — toolz/utils.py:1-7
# ✅ Good: string sentinel is picklable and self-describing across boundaries
no_default = '__no__default__'

def get_in(keys, coll, default=no_default):
    if default is no_default:
        ...  # caller omitted default — distinct from default=None
```
