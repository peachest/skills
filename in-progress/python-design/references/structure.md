### Protocol over ABC
`P021` · 41 occurrences · 26 projects: attrs, setuptools, Pillow, tornado, pytest, click, ...

**What**: Use `typing.Protocol` for structural subtyping — any object with the right methods satisfies the interface, with no inheritance required.

**Recognize**:
- `class X(Protocol):` appears in a typing module
- Interface methods have type annotations but no body, just `...`
- `@runtime_checkable` decorates a Protocol class
- Functions accept parameters typed as the Protocol rather than a concrete class or ABC

**Why**: Benefit: any object with the right method satisfies the interface — third-party file-like, array-like, or transport objects work without inheriting your base, and you avoid a hard dependency on the concrete library (Pillow can accept "anything numpy-like" without importing numpy). Cost: a Protocol carries no implementation (you get no shared methods), and `@runtime_checkable` only verifies attribute presence, not signatures or behavior.

**When**: Use for capability interfaces where you want to accept any object with the right shape (duck typing) without forcing inheritance — file-like objects, array-like objects, transport backends.

**When not**: When you need shared concrete behavior on the base, a Protocol's empty body gives you nothing — use an ABC base class or a mixin instead. If you need construction-time enforcement that subclasses actually implement methods, ABC + `@abstractmethod` fails at instantiation; `runtime_checkable` Protocol only checks method presence.

**Without this pattern** (anti-pattern):
```python
# ❌ Bad: ABC requires explicit inheritance, so third-party file-like objects are excluded
from abc import ABC, abstractmethod


class BaseTransport(ABC):
    @abstractmethod
    def handle_request(self, request) -> "Response": ...


class HTTPTransport(BaseTransport):  # must inherit explicitly
    def handle_request(self, request) -> "Response":
        return Response()


# A third-party transport that already has handle_request but doesn't
# inherit BaseTransport fails isinstance checks:
class ThirdPartyTransport:
    def handle_request(self, request) -> "Response":
        return Response()


isinstance(ThirdPartyTransport(), BaseTransport)  # False — silently excluded
```

**With this pattern**:
```python
# httpx — httpx/_transports/base.py
# ✅ Good: Protocol accepts any object with the right method, no inheritance needed
from typing import Protocol, runtime_checkable


@runtime_checkable
class BaseTransport(Protocol):
    def handle_request(self, request: "Request") -> "Response": ...


# Any class with handle_request qualifies — even third-party, no inheritance:
class HTTPTransport:
    def handle_request(self, request: "Request") -> "Response":
        return Response()


class ThirdPartyTransport:
    def handle_request(self, request: "Request") -> "Response":
        return Response()


isinstance(ThirdPartyTransport(), BaseTransport)  # True — structurally compatible
```

### Transport as Protocol with adapter implementations
`P022` · 16 occurrences · 11 projects: celery, hypothesis, tornado, httpx, textual, requests, ...

**What**: A minimal Protocol (often a single method) is realized by multiple adapter implementations — real (production), mock (testing), and server-side (WSGI/ASGI) — swapped at construction time.

**Recognize**:
- A Protocol/base interface with one method (`handle_request`, `send`, `dumps`/`loads`)
- Sibling adapter classes for the same interface: real, mock, WSGI, ASGI variants
- The client constructor takes the transport/provider as a parameter
- Transport selection happens at client construction, not via per-call branching

**Why**: Benefit: one minimal contract with multiple adapters lets production, test, and server-side transports be swapped without touching callers — the same client works against a real socket, an in-memory mock, or an embedded WSGI/ASGI app. Cost: the thin interface pushes any shared behavior into each adapter or a shared mixin, and you must keep adapter semantics consistent across implementations.

**When**: Use when one interface must have several swappable implementations selected at runtime or config time (production vs test, different schemes or backends).

**When not**: When there is only one realistic implementation and no testing or swap need, a Protocol plus adapters is ceremony — use a plain class. The interface itself should follow Protocol over ABC (P021).

**Without this pattern** (anti-pattern):
```python
# ❌ Bad: one class branches on environment — hard to test, can't mock cleanly
class Transport:
    def __init__(self, environment="production"):
        self.environment = environment

    def handle_request(self, request):
        if self.environment == "production":
            return self._real_http(request)      # real socket I/O
        elif self.environment == "test":
            return self._mock_response(request)  # canned response
        elif self.environment == "wsgi":
            return self._wsgi_roundtrip(request) # embedded WSGI app
        raise ValueError(self.environment)
```

**With this pattern**:
```python
# httpx — httpx/_transports/base.py
# ✅ Good: one Protocol, multiple adapter implementations selected at construction
from typing import Protocol


class BaseTransport(Protocol):
    def handle_request(self, request: "Request") -> "Response": ...


class HTTPTransport:        # production
    def handle_request(self, request):
        return self._real_http(request)


class MockTransport:        # testing
    def handle_request(self, request):
        return self._mock_response(request)


class WSGITransport:        # server-side (sync) testing
    def handle_request(self, request):
        return self._wsgi_roundtrip(request)


class ASGITransport:        # server-side (async) testing
    async def handle_handle_request(self, request):
        return await self._asgi_roundtrip(request)
```

### Small interface, deep implementation
`P023` · 21 occurrences · 20 projects: Pillow, tornado, click, toolz, jinja2, jsonschema, ...

**What**: A small public surface (convenience functions plus a client class) delegates through verb methods to a single deep implementation core, with an explicit `__all__`.

**Recognize**:
- A top-level convenience function (`get`, `post`) that constructs a Client and delegates
- Client verb methods all call one shared `request()` / `send()` core
- An explicit `__all__` listing the small public surface
- `__init__.py` re-exports using `from .x import Y as Y` form

**Why**: Benefit: convenience functions make one-liners trivial, while the shared `request()` core guarantees every verb gets auth, cookies, redirects, and transport handling for free — no duplicated logic. Cost: the layered call chain adds a few stack frames and indirection that readers must trace from the convenience function down to the transport.

**When**: Use for public APIs where a few convenience functions plus a richer client class serve both quick one-liners and reusable stateful sessions.

**When not**: When there is no reuse pattern (no state to hold across calls), convenience wrappers just add indirection — expose the function directly.

**Without this pattern** (anti-pattern):
```python
# ❌ Bad: each convenience function reimplements the full logic — duplicated,
# inconsistent auth/redirect handling across verbs
def get(url, **kwargs):
    with open_socket(url, "GET", **kwargs) as resp:
        return resp.read()  # auth, cookies, redirects hand-rolled here


def post(url, **kwargs):
    with open_socket(url, "POST", **kwargs) as resp:
        return resp.read()  # same handling duplicated, drifts from get()


def put(url, **kwargs):
    with open_socket(url, "PUT", **kwargs) as resp:
        return resp.read()
```

**With this pattern**:
```python
# httpx — httpx/_client.py
# ✅ Good: convenience function → Client verb method → shared request() core → transport
def get(url, **kwargs):
    with Client() as client:
        return client.get(url, **kwargs)


class Client:
    def get(self, url, **kwargs):
        return self.request("GET", url, **kwargs)

    def post(self, url, **kwargs):
        return self.request("POST", url, **kwargs)

    def request(self, method, url, **kwargs):
        # single deep implementation: auth, cookies, redirects, transport
        request = self.build_request(method, url, **kwargs)
        return self.send(request)
```

### @final for non-extendable classes
`P025` · 11 occurrences · 11 projects: celery, Pillow, hypothesis, tornado, aiohttp, pytest, ...

**What**: Building blocks are marked `@final` to signal they are used as-is and extended through composition, not subclassing.

**Recognize**:
- `@final` (from `typing` or `typing_extensions`) decorates a class
- The class is a "building block" (marker, enum, plugin manager) with no extension hooks
- Extension points live elsewhere (a registry, composition), not via subclassing this class

**Why**: Benefit: `@final` communicates "this is a fixed building block — extend by composition, not inheritance" and lets type checkers (mypy/pyright) reject subclasses before runtime. Cost: it forecloses subclassing even for legitimate future needs, so you must be confident the class is truly complete.

**When**: Use for building blocks meant to be used as-is and composed, where subclassing would break invariants (enums, plugin managers, hook markers).

**When not**: For classes designed as extension points, `@final` prevents the intended extension — use an ABC or Protocol (P021) instead.

**Without this pattern** (anti-pattern):
```python
# ❌ Bad: intent is "do not subclass", but nothing enforces it — relies on a comment
import enum


class ExitCode(enum.IntEnum):
    """Do not subclass this."""
    OK = 0
    TESTS_FAILED = 1


# Nothing stops a future maintainer from subclassing and breaking invariants:
class MyExitCode(ExitCode):
    EXTRA = 99  # adds a member the rest of the code never expected
```

**With this pattern**:
```python
# pytest — src/_pytest/config/__init__.py:85-86, 380-381
# ✅ Good: @final signals a fixed building block; extend via composition, not subclassing
import enum
from typing import final


@final
class ExitCode(enum.IntEnum):
    OK = 0
    TESTS_FAILED = 1
    INTERRUPTED = 2
    INTERNAL_ERROR = 3
    USAGE_ERROR = 4
    NO_TESTS_COLLECTED = 5


@final
class PytestPluginManager(PluginManager):
    ...
```

### _internal/ convention for public vs internal
`P026` · 29 occurrences · 22 projects: attrs, setuptools, Pillow, tornado, pytest, click, ...

**What**: `__init__.py` defines the public surface via `__all__`, keeps internals in `_`-prefixed modules, and uses a lazy `__getattr__` to defer heavy imports until first access.

**Recognize**:
- `__all__` defined in `__init__.py`
- Internal modules prefixed with `_` (`_make.py`, `_funcs.py`, `_internal/`)
- A module-level `__getattr__` that `import_module`s on demand
- Imports use `from ._x import name as name` re-export style

**Why**: Benefit: `__all__` defines the exact public surface, `_`-prefixed modules mark internals, and a lazy `__getattr__` defers heavy imports until first use — faster startup and a clean public/private boundary. Cost: lazy `__getattr__` hides import errors until the attribute is accessed and defeats some static-analysis and import-time checks.

**When**: Use for packages with a large surface where you want a curated public API, lazy imports, and a clear public/internal boundary.

**When not**: For tiny single-module packages, `__all__` plus `__getattr__` machinery is more code than the module itself — just use a plain module with a leading-underscore convention.

**Without this pattern** (anti-pattern):
```python
# ❌ Bad: eager star-imports, no __all__, internals leak into the public namespace
from ._make import *           # everything, including _private helpers
from ._next_gen import define, field, frozen
from ._config import _settings  # internal config exposed to users
# no __all__ — `from package import *` drags in every name, startup imports all
```

**With this pattern**:
```python
# attrs — src/attr/__init__.py:1-104
# ✅ Good: __all__ defines the public surface; _prefixed modules stay internal;
# __getattr__ defers heavy imports until first access
from ._funcs import asdict, astuple, has, resolve_types
from ._make import NOTHING, Attribute, attrib, attrs, evolve, fields
from ._next_gen import define, field, frozen, mutable

__all__ = ["NOTHING", "Attribute", "attrs", "attrib", "define", "field", ...]


def _make_getattr(mod_name):
    def __getattr__(name):
        if name not in ("__version__", "__version_info__"):
            raise AttributeError(f"module {mod_name} has no attribute {name}")
        from importlib.metadata import metadata
        ...
    return __getattr__


__getattr__ = _make_getattr(__name__)
```

### One visual element per module
`P027` · 4 occurrences · 4 projects: textual, toolz, rich, pytest

**What**: Each primary element or concern gets its own module file; small shared helpers live in `_`-prefixed modules.

**Recognize**:
- One primary class per module file (`table.py` → `Table`, `panel.py` → `Panel`)
- Small shared helpers in `_`-prefixed modules (`_loop.py`, `_pick.py`, `_io/`)
- `__all__` lists only that module's public element

**Why**: Benefit: one element per file means each can change and be navigated independently, and `_`-prefixed helper modules keep shared internals out of the public tree. Cost: more files and import statements to manage; for small libraries the granularity is overhead.

**When**: Use for UI/component libraries and large frameworks where each element or concern deserves its own file for navigation and independent change.

**When not**: For small utility collections, splitting each function into its own module creates import churn — group related helpers in one module.

**Without this pattern** (anti-pattern):
```python
# ❌ Bad: one monolithic utils.py holds every element and helper — 2000 lines,
# every change risks merge conflicts, elements and helpers interleaved
# project/utils.py
class Table: ...
class Panel: ...
class Columns: ...


def _loop(seq): ...
def _pick(options): ...
def _stack(items): ...
```

**With this pattern**:
```python
# rich — rich/table.py, rich/panel.py, rich/_loop.py
# ✅ Good: one element per module; small helpers get a _ prefix
# rich/table.py
class Table: ...


# rich/panel.py
class Panel: ...


# rich/columns.py
class Columns: ...


# rich/_loop.py        # private helper
def loop(seq): ...


# rich/_pick.py        # private helper
def pick(options): ...
```

### Thin Python wrappers over compiled core
`P028` · 7 occurrences · 5 projects: cryptography, Pillow, msgspec, aiohttp, polars

**What**: Python modules are thin re-export and wrapper layers over a compiled core (C extension or Rust bindings); the Python-visible API is aliases plus wrapper classes that hold a compiled handle and delegate.

**Recognize**:
- Python module is mostly `from ._core import ... as ...` re-exports
- Classes hold a handle to a compiled type (`_df: PyDataFrame`) and delegate every operation
- `_from_py*` classmethods construct wrappers from compiled handles
- The `Py*` types come from a compiled extension module

**Why**: Benefit: the Python layer provides discoverable import paths, `__all__`, docstrings, and type hints, while the compiled (C/Rust) layer delivers performance and memory safety — each language does what it is best at. Cost: two languages to build, debug, and keep in sync; the Python wrapper must forward every API change to the compiled layer.

**When**: Use when the performance-critical core is written in C or Rust and Python is the import, type, and documentation surface.

**When not**: For pure-Python libraries, a `_core` split with no compiled backing is pointless indirection.

**Without this pattern** (anti-pattern):
```python
# ❌ Bad: Python reimplements core logic; no clean re-export boundary — slow and
# divergent from any compiled layer
class DataFrame:
    def __init__(self, data):
        self._columns = {k: list(v) for k, v in data.items()}

    def filter(self, mask):
        # slow Python loop instead of compiled vectorized op
        return DataFrame(
            {k: [v for v, m in zip(col, mask) if m]
             for k, col in self._columns.items()}
        )
```

**With this pattern**:
```python
# polars — py-polars/src/polars/_utils/wrap.py:1-26, dataframe/frame.py:378-380
# ✅ Good: Python layer is a thin wrapper; logic lives in the compiled (Rust) core
import polars._reexport as pl


def wrap_df(df: "PyDataFrame") -> "DataFrame":
    return pl.DataFrame._from_pydf(df)


class DataFrame:
    _df: "PyDataFrame"  # compiled core handle

    @classmethod
    def _from_pydf(cls, py_df: "PyDataFrame") -> "DataFrame":
        df = cls.__new__(cls)
        df._df = py_df
        return df

    def filter(self, mask):
        return wrap_df(self._df.filter(mask._pyexpr))  # delegates to Rust
```

### Dual API: legacy aliases bridging to modern defaults
`P047` · 5 occurrences · 5 projects: attrs, setuptools, anyio, jsonschema, polars

**What**: Two parallel APIs coexist — a frozen legacy API with conservative defaults and a modern API that is a thin wrapper over the same implementation with opinionated defaults; legacy aliases provide backwards compatibility.

**Recognize**:
- Short legacy aliases (`s = attributes = attrs`, `ib = attr = attrib`)
- A modern function (`define`, `field`) calling the legacy one with different defaults
- A module `__getattr__` returning deprecated names with `DeprecationWarning`
- Two API generations documented side by side

**Why**: Benefit: the modern API can adopt better defaults (slots, kw_only) for new code while the legacy API stays frozen — no migration forced and no logic duplicated (modern wraps legacy with different defaults). Cost: two API surfaces to document and maintain, plus a permanent compatibility surface that can never be silently dropped.

**When**: Use when you ship a widely-used API and want to introduce better defaults without breaking existing callers.

**When not**: For new libraries with no installed base, ship one good API — dual APIs add maintenance surface. Once the legacy API is actually removed, the alias bridge is dead code.

**Without this pattern** (anti-pattern):
```python
# ❌ Bad: change defaults in place — breaks every existing user — OR duplicate logic
# Option A: silently change the existing default
def attrs(maybe_cls=None, *, slots=True, frozen=False, kw_only=True):
    ...  # callers relying on slots=False now get different behavior


# Option B: two separate implementations that drift apart
def attrs(maybe_cls=None, *, slots=False, **kw):
    ...  # legacy copy of all the logic


def define(maybe_cls=None, *, slots=True, **kw):
    ...  # modern copy of all the logic — duplicated, diverges over time
```

**With this pattern**:
```python
# attrs — src/attr/__init__.py:33-35, _next_gen.py:23-60
# ✅ Good: legacy API frozen; modern API is a thin wrapper with better defaults
# legacy aliases (never removed)
s = attributes = attrs
ib = attr = attrib


# modern API — same implementation, opinionated defaults, no duplication
def define(maybe_cls=None, *, slots=True, frozen=False,
           weakref_slot=True, kw_only=False, auto_exc=True):
    # wraps the legacy attrs() with modern defaults
    return attrs(maybe_cls, slots=slots, frozen=frozen,
                 weakref_slot=weakref_slot, kw_only=kw_only)
```

### Backend capability flags as class-level attributes
`P060` · 8 occurrences · 8 projects: cryptography, celery, Pillow, tornado, aiohttp, textual, ...

**What**: A base class declares boolean capability flags as class attributes; subclasses override them to declare what they support; callers check the flag rather than the concrete type.

**Recognize**:
- Base class with boolean class attributes (`supports_native_join = False`, `persistent = True`)
- Subclasses override specific flags to `True`
- Callers test `backend.supports_x` rather than `isinstance(backend, X)`
- Sometimes a decorator sets `cls._capability = True`

**Why**: Benefit: callers branch on `backend.supports_native_join` rather than `isinstance(backend, RedisBackend)`, so adding a new backend requires no edits to call sites — capability-based dispatch, not type-based. Cost: the flag set is fixed at base-class design time; a backend needing an unanticipated capability forces a base-class change, and forgotten flags fail silently.

**When**: Use when multiple backends or implementations have different capabilities and callers must branch on capability, not type.

**When not**: When all implementations are feature-equivalent, capability flags that are always True/False are noise — just use the base method. If capabilities are rare and ad hoc, a single `supports(feature)` method may be cleaner.

**Without this pattern** (anti-pattern):
```python
# ❌ Bad: isinstance checks at every call site — tight coupling; adding a backend
# means editing every check, and missing branches fail silently
def join_results(backend, keys):
    if isinstance(backend, RedisBackend):
        return backend.mget(keys)                  # native join
    return [backend.get(k) for k in keys]           # fallback


def expire_results(backend, key, ttl):
    if isinstance(backend, (RedisBackend, DatabaseBackend)):
        backend.expire(key, ttl)
    # filesystem backend silently skipped — forgot to add the branch
```

**With this pattern**:
```python
# celery — celery/backends/base.py:109-140
# ✅ Good: base declares capability flags; subclasses override; callers check the
# flag, not the concrete type
class Backend:
    supports_native_join = False
    supports_autoexpire = False
    persistent = True


class RedisBackend(Backend):
    supports_native_join = True
    supports_autoexpire = True


# caller — capability-based dispatch, no isinstance
def join_results(backend, keys):
    if backend.supports_native_join:
        return backend.get_many(keys)
    return [backend.get(k) for k in keys]
```

### Sans-IO architecture: protocol-agnostic core + IO adapter subclass
`P066` · 3 occurrences · 2 projects: flask, werkzeug

**What**: Split the application into a sans-IO base class holding all protocol-agnostic logic (routing, config, error handlers) and a concrete subclass that adds WSGI/async IO, so the base is reusable across server interfaces.

**Recognize**:
- A `sansio/` subpackage with a base class containing no `environ`/socket/async I/O
- A concrete subclass in the parent package adds WSGI/ASGI I/O
- The base class takes parsed values (method, scheme, headers), not raw protocol bytes

**Why**: Benefit: all routing, config, and error handling live in a transport-agnostic base reused by WSGI, ASGI, and test harnesses — no forking the framework per server interface, and core behavior is testable without HTTP. Cost: two class layers and a `sansio/` package to maintain; the IO subclass must carefully translate protocol specifics into the base's neutral calls.

**When**: Use for servers or clients that must support multiple transport protocols (WSGI, ASGI, test) sharing the same routing/config/error logic.

**When not**: For single-protocol libraries the sansio/base split doubles the class hierarchy for no reuse; if I/O and logic are genuinely inseparable, forcing a split obscures the code.

**Without this pattern** (anti-pattern):
```python
# ❌ Bad: routing/config logic fused with WSGI I/O — can't reuse for ASGI or tests
class Flask:
    def __init__(self, import_name):
        self.url_map = Map()
        self.config = Config()

    def __call__(self, environ, start_response):  # WSGI fused in
        path = environ["PATH_INFO"]
        method = environ["REQUEST_METHOD"]
        # routing, error handling, response building ALL here, mixed with WSGI
        response = self.full_dispatch(path, method)
        start_response("200 OK", [])
        return [response.body]
# To support ASGI you'd have to fork the whole class and duplicate routing
```

**With this pattern**:
```python
# flask — src/flask/sansio/app.py:63-301, src/flask/app.py
# ✅ Good: protocol-agnostic core in sansio/; WSGI I/O added by a subclass
class App(Scaffold):                       # sansio/app.py — no I/O
    def __init__(self, import_name):
        self.config = self.make_config(...)
        self.url_map = self.url_map_class()

    def full_dispatch_request(self):
        # routing, error handling, template setup — all transport-agnostic
        ...


class Flask(App):                          # app.py — adds WSGI I/O
    def wsgi_app(self, environ, start_response):
        ctx = self.request_context(environ)
        try:
            ctx.push()
            response = self.full_dispatch_request()
        except Exception as e:
            response = self.handle_exception(e)
        finally:
            ctx.pop()
        return response(environ, start_response)
```

### MethodView: __init_subclass__ for automatic method dispatch
`P076` · 11 occurrences · 8 projects: Pillow, aiohttp, jinja2, textual, sqlalchemy, anyio, flask, werkzeug

**What**: `__init_subclass__` scans a class for method names (HTTP verbs, `on_<name>` handlers) at definition time and auto-populates a dispatch registry, so defining a method registers it with no manual list.

**Recognize**:
- `def __init_subclass__(cls, **kwargs)` scanning `dir(cls)` or a method-name set
- Handler methods named by convention (`get`, `post`, or `on_<name>`)
- A `methods`/registry attribute auto-populated, not manually set on subclasses
- Dispatch is a dict / O(1) lookup, not `if request.method == ...`

**Why**: Benefit: `__init_subclass__` auto-populates `methods` from defined handlers, so there is no manual list to drift, and dispatch is O(1) at runtime. Cost: behavior is implicit (magic at class-definition time) — readers can't see the registration without knowing the base class, and misnamed methods silently fail to register.

**When**: Use when subclasses should auto-register or auto-derive metadata (HTTP methods, handler names, validation) at class-definition time without explicit registration calls.

**When not**: When registration needs runtime or context info not available at class-definition time, use an explicit `register()` call or decorator; if subclasses are few and stable, manual registration is simpler than `__init_subclass__` magic.

**Without this pattern** (anti-pattern):
```python
# ❌ Bad: manual methods list that drifts from actual handlers, plus per-request
# if/elif dispatch
class UserAPI(MethodView):
    methods = ["GET", "POST"]  # must hand-maintain; forget PUT → 405

    def dispatch_request(self, **kwargs):
        if request.method == "GET":
            return self.get(**kwargs)
        elif request.method == "POST":
            return self.post(**kwargs)
        # added def put() but forgot to update methods and this branch → 405
```

**With this pattern**:
```python
# flask — src/flask/views.py:37-100, 155-190
# ✅ Good: __init_subclass__ auto-populates methods from defined handlers
class MethodView(View):
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if "methods" not in cls.__dict__:
            methods = set()
            for key in http_method_funcs:        # {"get", "post", "put", ...}
                if hasattr(cls, key):
                    methods.add(key.upper())
            if methods:
                cls.methods = methods


class UserAPI(MethodView):
    def get(self, id): ...    # → GET registered automatically
    def post(self): ...       # → POST registered automatically
    def put(self, id): ...    # → PUT registered automatically


# UserAPI.methods == {"GET", "POST", "PUT"} — no manual list, no drift
```

### Dual-mode decorator via __call__ dispatch
`P086` · 6 occurrences · 6 projects: setuptools, pytest, click, loguru, starlette, anyio

**What**: A single `__call__` inspects its arguments: called with a bare callable/class it applies the decorator and returns the object; called with other args it returns a new decorator — supporting both `@deco` and `@deco(args)` from one object.

**Recognize**:
- One `__call__(self, *args, **kwargs)` that inspects `args[0]`
- If `args[0]` is a callable/class → apply and return it
- Otherwise → return `self.with_args(...)` (a new decorator)
- Both `@deco` and `@deco(arg=...)` work from the same object

**Why**: Benefit: one object supports both `@deco` and `@deco(args)` from a single `__call__`, so users don't have to know which syntax each decorator accepts — the parameterized/bare distinction is invisible at the call site. Cost: the `__call__` argument inspection is subtle and easy to get wrong, and static type checkers can't always distinguish the two modes.

**When**: Use for decorators that must support both `@deco` and `@deco(args)` uniformly from one object (marks, caches, commands).

**When not**: When the parameterized and bare forms have genuinely different semantics, a single `__call__` dispatch hides the distinction and confuses users — use two clearly-named decorators.

**Without this pattern** (anti-pattern):
```python
# ❌ Bad: separate objects for each form — users must know which syntax applies
def mark_skip(func):                       # only @mark_skip works
    store_mark(func, Mark("skip"))
    return func


def mark_skip_with(reason):                # only @mark_skip_with(reason=...) works
    def deco(func):
        store_mark(func, Mark("skip", (), {"reason": reason}))
        return func
    return deco


# User can't write both @pytest.mark.skip and @pytest.mark.skip(reason="x") uniformly
```

**With this pattern**:
```python
# pytest — src/_pytest/mark/structures.py:451-480
# ✅ Good: one __call__ inspects args — applies directly OR returns a new decorator
class MarkDecorator:
    def __call__(self, *args, **kwargs):
        if args and not kwargs:
            func = args[0]
            if len(args) == 1 and (istestfunc(func) or inspect.isclass(func)):
                store_mark(func, self.mark)
                return func                      # @pytest.mark.skip
        return self.with_args(*args, **kwargs)   # @pytest.mark.skip(reason="x")


# Both @pytest.mark.skip and @pytest.mark.skip(reason="x") work from one object
```

### __getattr__ as dynamic attribute factory
`P087` · 12 occurrences · 9 projects: cryptography, setuptools, Pillow, hypothesis, pytest, textual, ...

**What**: A `__getattr__` fabricates a valid object for any attribute name on demand, with no pre-registration — creation always succeeds, and validation is deferred and configurable.

**Recognize**:
- A class-level or module-level `__getattr__(self, name)` that constructs and returns objects
- No pre-defined attributes for the fabricated names
- Unknown names yield a warning or error rather than only `AttributeError`
- The fabricated object is usually cached or stateless

**Why**: Benefit: any attribute access yields a valid decorator — marks are open-ended and user-defined with no registration step; creation always succeeds and validation is deferred and configurable (warning by default, hard error under strict mode). Cost: typos silently produce valid-but-unknown marks (only warned unless strict), and static analyzers can't see the fabricated attributes.

**When**: Use when attribute names are open-ended or user-defined and can't be pre-enumerated (marks, lazy module attributes).

**When not**: When the set of attributes is fixed and small, a class with explicit attributes is clearer, statically analyzable, and won't surprise type checkers; for deprecation aliases prefer a narrow `__getattr__` that warns (see P047).

**Without this pattern** (anti-pattern):
```python
# ❌ Bad: pre-register every name — can't cover user-defined marks, bloated module
class MarkGenerator:
    skip = MarkDecorator(Mark("skip"))
    slow = MarkDecorator(Mark("slow"))
    xfail = MarkDecorator(Mark("xfail"))
    # ... must enumerate every mark here


mark = MarkGenerator()
mark.smoke  # AttributeError — not pre-registered, user's custom mark rejected
```

**With this pattern**:
```python
# pytest — src/_pytest/mark/structures.py:510-555
# ✅ Good: __getattr__ fabricates a MarkDecorator on demand; validation is lazy
class MarkGenerator:
    def __getattr__(self, name):
        if name[0] == "_":
            raise AttributeError("Marker name must NOT start with underscore")
        if self._config is not None and name not in self._markers:
            if self._config.option.strict_markers:
                fail(f"{name!r} not found in `markers` configuration option")
            warnings.warn(f"Unknown pytest.mark.{name} - is this a typo?")
        return MarkDecorator(Mark(name, (), {}))


mark = MarkGenerator()
mark.anything      # always succeeds — fabricates a decorator
mark.skip          # known mark, no warning
mark.typo_xyz      # warning (or error if strict_markers)
```

### Adapter mounting as transport strategy by URL prefix
`P093` · 3 occurrences · 3 projects: anyio, werkzeug, requests

**What**: A client keeps a prefix-ordered registry of `{url_prefix: adapter}`; `get_adapter(url)` matches the longest prefix, and `mount(prefix, adapter)` lets users register custom transports without editing the client.

**Recognize**:
- A `mount(prefix, adapter)` method on a client or session
- An `OrderedDict`/list of `{prefix: adapter}` kept sorted by prefix length
- `get_adapter(url)` does `url.startswith(prefix)` matching
- All adapters implement a common `send`/`handle_request` interface

**Why**: Benefit: a prefix-ordered adapter registry lets users mount custom transports for any scheme or host without editing the Session, and longest-prefix matching allows host-specific overrides over scheme-wide defaults. Cost: the registry adds indirection and a linear prefix scan per request; mis-ordered prefixes can route to the wrong adapter.

**When**: Use when transport selection depends on URL scheme or host and users need to register custom adapters without editing the client.

**When not**: When transport is fixed or chosen by explicit argument, a prefix registry adds indirection — pass the adapter directly; for capability-based selection see P060.

**Without this pattern** (anti-pattern):
```python
# ❌ Bad: hardcoded scheme dispatch inside Session — can't add schemes without
# editing Session, no host-specific overrides
class Session:
    def send(self, request):
        if request.url.startswith("https://"):
            return HTTPAdapter().send(request)
        elif request.url.startswith("http://"):
            return HTTPAdapter(insecure=True).send(request)
        # want ftp:// or https://api.example.com via a proxy? edit Session source
        raise InvalidSchema(request.url)
```

**With this pattern**:
```python
# requests — src/requests/sessions.py:730-755
# ✅ Good: prefix-ordered adapter registry; longest-prefix wins; mountable by users
from collections import OrderedDict


class Session:
    def __init__(self):
        self.adapters = OrderedDict()
        self.mount("https://", HTTPAdapter())
        self.mount("http://", HTTPAdapter())

    def get_adapter(self, url):
        for prefix, adapter in self.adapters.items():
            if url.lower().startswith(prefix.lower()):
                return adapter
        raise InvalidSchema(f"No connection adapters were found for {url!r}")

    def mount(self, prefix, adapter):
        self.adapters[prefix] = adapter
        # keep longest prefixes first so host-specific overrides win
        keys_to_move = [k for k in self.adapters if len(k) < len(prefix)]
        for key in keys_to_move:
            self.adapters[key] = self.adapters.pop(key)


# user code — no Session edits needed:
session.mount("https://api.example.com/", ProxyAdapter(proxy="..."))
```
### Convenience-function layer over session-based API
`P102` · 4 occurrences · 4 projects: anyio, polars, requests, setuptools

**What**: Module-level one-liner functions that construct a session-like object, delegate the call, and return the result — eliminating boilerplate for one-off uses while keeping the full session API for advanced cases.

**Recognize**:
- Module-level functions named after verbs (`get`, `post`, `head`) that each delegate to a single `request()` helper
- The helper opens a `with Session():` block and returns the inner call result
- Each verb function applies verb-specific defaults (e.g. `head` sets `allow_redirects=False`) then forwards `**kwargs`
- The kwargs accepted by `Session.request()` surface verbatim on the convenience functions

**Why**: Most uses are one-offs where the user wants "do X" without managing object lifecycle, but the implementation still needs the persistent-object machinery (connection pooling, default headers, cookies). The convenience layer bridges this — the top-level API is a handful of one-liners, each delegating to full session machinery. Benefit: a tiny, trivial-to-learn top-level API. Cost: each one-off call reconstructs the session, so it cannot reuse connections across calls — users who hit that cost should reach for the Session API directly.

**When**: When a class-based API carries real setup/teardown cost and most callers only want a single operation.

**When not**: When the object is cheap to construct or stateless — just call the class directly. Also skip when callers always need persistence; use the session/object API instead.

**Without this pattern** (anti-pattern):
```python
# ❌ Bad: every one-off caller must manage session lifecycle and boilerplate
session = requests.Session()
try:
    response = session.request(method="get", url="https://example.com")
finally:
    session.close()
```

**With this pattern**:
```python
# requests — src/requests/api.py:30-45
# ✅ Good: one-liner verbs delegate to a single helper that owns the session lifecycle
def request(method, url, **kwargs) -> Response:
    with sessions.Session() as session:
        return session.request(method=method, url=url, **kwargs)

def get(url, params=None, **kwargs) -> Response:
    return request("get", url, params=params, **kwargs)

def head(url, **kwargs) -> Response:
    kwargs.setdefault("allow_redirects", False)
    return request("head", url, **kwargs)
```

### Mixin-based interface composition for model classes
`P106` · 9 occurrences · 9 projects: cryptography, Pillow, jinja2, textual, requests, starlette, anyio, werkzeug, polars

**What**: Focused mixin classes each carry one cohesive set of methods, and concrete classes assemble the full interface via multiple inheritance rather than a monolithic base class.

**Recognize**:
- Small classes named `...Mixin` (or focused base classes) each holding one concern's methods
- Concrete classes inherit from several mixins in a single bases tuple: `class X(A, B, C):`
- Each mixin is independently testable and reused across multiple concrete classes
- Methods carry their own type annotations; mixins rarely call `super().__init__`

**Why**: Encoding logic, hook registration, etc. are independent concerns. Splitting them into mixins lets each be tested in isolation and reused in contexts that need only a subset. This is the pre-Protocol approach to interface composition. Benefit: shared *implementation* (not just signatures) across classes that pick different subsets. Cost: MRO complexity, and mixins that assume state set by another mixin create implicit coupling between the concrete class and its mixin ordering — when only signatures matter, Protocol composition is the modern alternative.

**When**: When several classes share the same *implementation* of a cohesive method group, and individual classes pick different subsets.

**When not**: When you only need to share *signatures* — use Protocol composition (P021, Protocol over ABC). Also skip when mixins would need fragile cooperative `super()` chains.

**Without this pattern** (anti-pattern):
```python
# ❌ Bad: one monolithic base class stuffed with every concern, untestable in isolation
class Request:
    def _encode_params(self, params): ...
    def _encode_files(self, files): ...
    def path_url(self): ...
    def register_hook(self, event, hook): ...
    def deregister_hook(self, event, hook): ...
    # encoding + hooks + everything else tangled together in one class
```

**With this pattern**:
```python
# requests — src/requests/models.py:85-87, 175-178
# ✅ Good: each concern is a focused mixin; concrete classes assemble the subset they need
class RequestEncodingMixin:
    # _encode_params, _encode_files, path_url property

class RequestHooksMixin:
    def register_hook(self, event, hook) -> None: ...
    def deregister_hook(self, event, hook) -> bool: ...

class Request(RequestHooksMixin): ...
class PreparedRequest(RequestEncodingMixin, RequestHooksMixin): ...
```

### TypedDict kwargs for per-method parameter contracts
`P107` · 5 occurrences · 5 projects: setuptools, textual, requests, anyio, polars

**What**: Per-method `**kwargs` contracts modeled as `TypedDict` subclasses (often inheriting a shared base) and applied via `Unpack[...]` so type checkers validate which keyword each method accepts.

**Recognize**:
- `class XKwargs(TypedDict, total=False):` subclasses, often extending a `BaseXKwargs`
- Method signatures read `def method(self, ..., **kwargs: Unpack[XKwargs]) -> ...`
- Fields declared per-method express which kwargs that method accepts (e.g. `GetKwargs` has no `data`)
- TypedDicts live in a `_types.py`-style module imported by the implementation

**Why**: Shared kwargs with per-method variation (GET has `params` but no `data`; POST has `data`/`json`) cannot be expressed in plain `**kwargs`. TypedDict + `Unpack` lets the type checker flag `requests.get(url, data=...)` as suspicious while accepting `requests.post(url, data=...)`. Benefit: per-method keyword validation with no runtime cost. Cost: a parallel TypedDict hierarchy must be kept in sync with the real implementation, and `Unpack` requires a recent Python/typeshed baseline.

**When**: When several methods share most kwargs but differ in specifics, and you want static checking of which keyword each accepts.

**When not**: When all methods take identical kwargs (a single shared TypedDict suffices) or when the API is so dynamic that maintaining the TypedDicts costs more than the checking gains.

**Without this pattern** (anti-pattern):
```python
# ❌ Bad: untyped **kwargs — the type checker cannot catch GET-with-a-body
def get(self, url, params=None, **kwargs) -> Response: ...
def post(self, url, data=None, **kwargs) -> Response: ...

# requests.get("https://x", data={"a": 1})  # silent bug, no warning anywhere
```

**With this pattern**:
```python
# requests — src/requests/_types.py:140-168
# ✅ Good: each verb's kwargs are a TypedDict; Unpack[] gives the type checker a per-method contract
class BaseRequestKwargs(TypedDict, total=False):
    headers: HeadersType
    cookies: ...
    auth: AuthType
    timeout: TimeoutType
    # ...shared by all verbs

class GetKwargs(BaseRequestKwargs, total=False):
    data: DataType
    json: JsonType

class PostKwargs(BaseRequestKwargs, total=False):
    params: ParamsType

# Usage:
def get(self, url, params=None, **kwargs: Unpack[GetKwargs]) -> Response: ...
```

### Virtual base class with `__new__` dispatching to backend factory
`P108` · 3 occurrences · 2 projects: anyio, tornado

**What**: A base class declares the interface (methods raising `NotImplementedError`) while `__new__` dispatches to a backend factory, returning a concrete subclass — so callers write `Event()` and transparently get the right backend implementation.

**Recognize**:
- Base class whose methods all `raise NotImplementedError` (or carry only `...` with `@abstractmethod`)
- `def __new__(cls):` calls a factory like `get_async_backend().create_event()` instead of `super().__new__`
- A fallback branch returns an adapter/substitute when no backend is available (e.g. `EventAdapter()`)
- Callers never import the concrete backend class — they instantiate the base

**Why**: Lets user code write `Event()` without knowing or importing which async backend (asyncio, trio) is active; backend selection happens at runtime via sniffio. The base doubles as the typed interface (docstrings, `__slots__`, type hints) while never being instantiated. The adapter fallback (merged from P109) captures intent before the loop starts and replays it once a backend exists. Benefit: zero-import backend abstraction with graceful pre-loop construction. Cost: `__new__` returning a different class surprises readers and debuggers, and dispatch is hidden inside construction rather than expressed as an explicit factory call.

**When**: When you want callers to write `Thing()` and get a backend-specific subclass chosen at runtime, especially across async backends or pluggable implementations.

**When not**: When backend selection is static/config-time (use an explicit factory or `__init_subclass__` registration) or when there's only one implementation — no dispatch is needed. See also P060 (backend capability flags) for declaring per-backend features.

**Without this pattern** (anti-pattern):
```python
# ❌ Bad: callers must know and import the backend-specific class
from anyio._backends._asyncio import Event as AsyncioEvent
from anyio._backends._trio import Event as TrioEvent

if current_backend() == "asyncio":
    event = AsyncioEvent()
elif current_backend() == "trio":
    event = TrioEvent()
else:
    raise RuntimeError("no backend available")
```

**With this pattern**:
```python
# anyio — src/anyio/_core/_synchronization.py:82-110
# ✅ Good: __new__ dispatches to the backend factory; an adapter handles the no-loop case
class Event:
    __slots__ = ("__weakref__",)

    def __new__(cls) -> Event:
        try:
            return get_async_backend().create_event()
        except NoEventLoopError:
            return EventAdapter()

    def set(self) -> None:
        """Set the flag, notifying all listeners."""
        raise NotImplementedError

    async def wait(self) -> None:
        raise NotImplementedError
```

### Lazy backend loading with module-level cache
`P110` · 4 occurrences · 3 projects: anyio, Pillow, uvicorn

**What**: Backend/plugin classes are imported on demand via `import_module(...)` and cached in a module-level dict, so only the backend the user actually needs is ever imported.

**Recognize**:
- A module-level `loaded_backends: dict[str, type] = {}` (or similar cache) populated lazily
- `import_module(f"pkg._backends._{name}")` called inside a lookup function, reading `module.backend_class`
- A `KeyError`/cache-miss path that performs the import then stores it before returning
- Optional plugins imported via `__import__(f"{__spec__.parent}.{plugin}")` on first use

**Why**: Importing trio (or every image plugin, every crypto backend) unconditionally adds startup overhead and forces hard dependencies. Lazy loading imports only what's used; the cache avoids repeated `import_module` calls. Benefit: fast startup and soft dependencies — users without trio pay nothing. Cost: first use is slower (the import happens on demand), errors surface at use time rather than import time, and the cache must handle partially-initialized modules.

**When**: When you support multiple backends/plugins and importing all of them eagerly is too costly or would force unwanted hard dependencies.

**When not**: When there's only one backend (just import it) or when backends are tiny and always needed — eager import is simpler. For sophisticated deferred loading with lazy proxy modules, see P235 (optional dependency handling, sophisticated variation).

**Without this pattern** (anti-pattern):
```python
# ❌ Bad: eager top-level imports force every backend as a hard dependency
from anyio._backends._asyncio import AsyncioBackend
from anyio._backends._trio import TrioBackend
# trio is now a hard dependency; startup pays for both even if only asyncio is used
```

**With this pattern**:
```python
# anyio — src/anyio/_core/_eventloop.py:198-208
# ✅ Good: backends are imported on first use and cached; only the requested backend loads
loaded_backends: dict[str, type[AsyncBackend]] = {}

def get_async_backend(asynclib_name: str | None = None) -> type[AsyncBackend]:
    if asynclib_name is None:
        asynclib_name = current_async_library()
    try:
        return loaded_backends[asynclib_name]
    except KeyError:
        module = import_module(f"anyio._backends._{asynclib_name}")
        loaded_backends[asynclib_name] = module.backend_class
        return module.backend_class
```

### Function impersonation for transparent framework integration
`P157` · 3 occurrences · 2 projects: hypothesis, more-itertools

**What**: A decorator that overwrites a wrapper function's `__code__` (filename, firstlineno), `__name__`, `__module__`, `__doc__` to match a target, so introspection tools see the original function rather than the wrapper.

**Recognize**:
- A decorator that reassigns `f.__code__ = f.__code__.replace(co_filename=..., co_firstlineno=...)`
- `f.__name__`, `f.__module__`, `f.__doc__` overwritten to the target's values
- Often paired with `functools.wraps` and signature rebuilding into a `proxies(target)` helper
- A hidden breadcrumb attribute (e.g. `__hypothesistracebackhide__`) left for the library's own introspection

**Why**: Testing frameworks (pytest, unittest) discover tests, resolve fixtures, and build tracebacks by introspecting functions. If a `@given` wrapper doesn't look like the user's test, discovery and error reporting break. Impersonation lies about where the code comes from so tracebacks point at the user's test, not library internals. Benefit: transparent framework integration — the wrapper is invisible to consumers. Cost: it deliberately corrupts debuggability of the wrapper itself, so you must leave a breadcrumb and accept that `inspect` lies about the function's origin.

**When**: When a decorator must remain invisible to a host framework that introspects `__name__`/`__code__`/`__module__` (test runners, profilers, traceback formatters).

**When not**: When the host only needs `__wrapped__`/`functools.wraps` (use that instead) or when honest introspection matters more than transparency — `@wraps` alone is usually enough.

**Without this pattern** (anti-pattern):
```python
# ❌ Bad: functools.wraps copies metadata, but __code__.co_filename still points at the library
def given(*given_args):
    def decorator(test_function):
        @wraps(test_function)
        def wrapper(*args, **kwargs):
            ...  # run the property test
        return wrapper
    return decorator
# pytest's traceback now shows "hypothesis/.../core.py" instead of the user's test file
```

**With this pattern**:
```python
# hypothesis — hypothesis/src/hypothesis/internal/reflection.py:500-540
# ✅ Good: impersonate overwrites __code__/__name__/__module__/__doc__ so the wrapper is invisible
def impersonate(target):
    def accept(f):
        f.__code__ = f.__code__.replace(
            co_filename=target.__code__.co_filename,
            co_firstlineno=target.__code__.co_firstlineno,
        )
        f.__name__ = target.__name__
        f.__module__ = target.__module__
        f.__doc__ = target.__doc__
        f.__globals__["__hypothesistracebackhide__"] = True
        f.__wrapped_target = target
        return f
    return accept

def proxies(target: T) -> Callable[[Callable], T]:
    replace_sig = define_function_signature(target.__name__, target.__doc__, get_signature(target))
    def accept(proxy):
        return impersonate(target)(wraps(target)(replace_sig(proxy)))
    return accept
```

### Pre-instantiated singleton module object
`P159` · 9 occurrences · 9 projects: cryptography, beartype, Pillow, tornado, setuptools, loguru, sqlalchemy, more-itertools, starlette

**What**: A module exports a single pre-configured instance of its main class, created at import time with sensible defaults, so users `from pkg import instance` and get a working object immediately.

**Recognize**:
- A module-level `logger = _Logger(...)` / `options = OptionParser()` assignment at import time
- Auto-initialization (e.g. `logger.add(sys.stderr)`) gated by an env var, run at module load
- Module-level functions that delegate to the singleton (`def define(...): return options.define(...)`)
- The class itself remains importable for advanced or manual construction

**Why**: Eliminates the boilerplate of `logger = getLogger(); logger.setLevel(); logger.addHandler()` — users get a working logger with `from loguru import logger`. The singleton works for logging because there is conceptually one global pipeline. Benefit: lowest-friction entry point with sensible defaults out of the box. Cost: global mutable state shared by all callers, hard to isolate in tests or multi-tenant scenarios — a factory pattern where each module builds its own bound logger is the explicit alternative.

**When**: When there is conceptually one global resource (logging, CLI options) and most users want sensible defaults with zero configuration.

**When not**: When callers need isolated or per-context instances (use a factory/class API) or when import-time side effects (handlers, env reads) are undesirable.

**Without this pattern** (anti-pattern):
```python
# ❌ Bad: every caller repeats construction and default configuration
logger = Logger()
logger.add(sys.stderr)
logger.setLevel("INFO")
logger.info("hello")
# the same four lines get repeated in every module that wants logging
```

**With this pattern**:
```python
# loguru — loguru/__init__.py:15-30
# ✅ Good: a pre-configured singleton is the import surface; auto-init is env-gated
logger = _Logger(
    core=_Core(),
    exception=None,
    depth=0,
    record=False,
    lazy=False,
    colors=False,
    raw=False,
    capture=True,
    patchers=[],
    extra={},
)

if _defaults.LOGURU_AUTOINIT and _sys.stderr:
    logger.add(_sys.stderr)

_atexit.register(logger.remove)
```

### opt() as immutable configuration overlay returning new instance
`P177` · 5 occurrences · 5 projects: cryptography, beartype, setuptools, loguru, polars

**What**: A method that returns a *new* instance sharing the same core but with modified per-call options, applying a "last wins" (non-chaining) reset so the returned object is fully configured for one call.

**Recognize**:
- A method named `opt`/`bind`/`patch` (or `set_*` classmethods returning `cls`) that returns a new instance, not `self`
- The new instance shares an immutable `_core` with the original (same sinks/backend)
- Options reset to defaults except the ones passed — calling `opt()` again does not accumulate
- Classmethods like `set_verbose` returning `type[Config]` to enable chaining at the class level

**Why**: `opt()` enables per-call customization (colors, exception capture, depth) without polluting the global logger state — each call site gets a configured view over the shared core. The "last wins" rule keeps the mental model simple: you never reason about accumulated options from multiple calls. Benefit: scoped, composable configuration that never mutates global state. Cost: every `opt()` allocates a new instance, and "last wins" surprises users who expect chaining — the contract must be documented.

**When**: When a shared object (logger, config) needs per-call or per-scope option overrides without mutating the shared state.

**When not**: When options should accumulate across calls (use a chaining builder) or when the object holds no shared core worth preserving — a plain mutable config suffices.

**Without this pattern** (anti-pattern):
```python
# ❌ Bad: mutate the shared logger, leaking per-call options to every later call
logger.colors = True
logger.exception = sys.exc_info()
logger.info("one-off colored message with exception")
# logger is now permanently colors=True / exception=... for ALL subsequent calls
```

**With this pattern**:
```python
# loguru — loguru/_logger.py:1313-1340
# ✅ Good: opt() returns a new Logger over the same _core; last-wins, never mutates the original
def opt(self, *, exception=None, record=False, lazy=False, colors=False,
        raw=False, capture=True, depth=0, ansi=False):
    args = self._options[-2:]
    return Logger(self._core, exception, depth, record, lazy, colors, raw, capture, *args)
```

### Compatibility shim: version-conditional imports with `__all__`
`P198` · 10 occurrences · 7 projects: cryptography, setuptools, Pillow, toolz, more-itertools, sqlalchemy, uvicorn

**What**: A dedicated `compatibility.py` module centralizes version/environment differences via runtime checks, assigning the correct implementation and exporting a documented surface through `__all__`.

**Recognize**:
- A module named `compatibility.py` / `_compat.py` with `PY3 = sys.version_info[0] > 2` style guards
- `if PY3: ... else: ...` blocks reassigning the same names (`map`, `range`, `reduce`) to the right implementation
- An `__all__` tuple listing the normalized compatibility surface
- Other modules `from .compatibility import map, range` instead of scattering conditional imports

**Why**: Centralizing version differences in one module makes the rest of the codebase version-agnostic — `__all__` documents the compatibility surface, and when old-Python support is dropped only this one file changes. This is the adapter pattern at module level. Benefit: one indirection layer absorbs all environmental variation, with a clean removal path. Cost: an extra module/indirection, and the shim can linger long after the version gap closes, accruing dead branches.

**When**: When you support multiple Python versions or environments with divergent stdlib APIs and want a single place to absorb the differences.

**When not**: When supporting only one target version (delete the shim) or for a single isolated conditional import — a local `try/except ImportError` (P233) is lighter than a whole module.

**Without this pattern** (anti-pattern):
```python
# ❌ Bad: version conditionals scattered through every module that uses map/reduce
# module_a.py
try:
    from itertools import imap as map
except ImportError:
    pass
# module_b.py
try:
    from functools import reduce
except ImportError:
    reduce = reduce  # py2 builtin
# duplicated, inconsistent, no single source of truth for the compat surface
```

**With this pattern**:
```python
# toolz — toolz/compatibility.py:1-26
# ✅ Good: one module owns every version difference; __all__ documents the compat surface
PY3 = sys.version_info[0] > 2

__all__ = ('PY3', 'map', 'filter', 'range', 'zip', 'reduce', 'zip_longest',
           'iteritems', 'iterkeys', 'itervalues', 'filterfalse')

if PY3:
    map = map
    filter = filter
    range = range
    zip = zip
    from functools import reduce
    from itertools import zip_longest
    from itertools import filterfalse
    iteritems = operator.methodcaller('items')
    iterkeys = operator.methodcaller('keys')
    itervalues = operator.methodcaller('values')
else:
    range = xrange
    reduce = reduce
    from itertools import imap as map
    from itertools import ifilter as filter
```

### Module-level deprecation via `__getattr__` with name remapping
`P221` · 3 occurrences · 3 projects: beartype, uvicorn, cryptography

**What**: A module defines `__getattr__` (PEP 562) that intercepts access to deprecated names, looks them up in a remapping dict (old → new), emits a `DeprecationWarning`, and returns the renamed attribute — unknown names raise `AttributeError`.

**Recognize**:
- A module-level `def __getattr__(attr_name: str) -> object:` function (PEP 562)
- A remapping dict `{old_name: new_name}` consulted inside `__getattr__`
- A `warnings.warn(..., DeprecationWarning)` (or delegated helper) emitted on the old name
- `raise AttributeError(...)` for genuinely unknown names

**Why**: Renaming public API attributes breaks downstream code. PEP 562 module `__getattr__` gives a clean deprecation path: old names still work but warn, guiding users to new names, with the remapping dict as the single source of truth. Isolating imports inside `__getattr__` keeps the deprecated names out of the module namespace. Benefit: backward-compatible renames with automatic migration guidance. Cost: deprecated names keep working silently if users suppress warnings, so removal must be scheduled explicitly; `__getattr__` adds a lookup hop on first access.

**When**: When you rename a public module-level attribute and need the old import path to keep working with a deprecation warning.

**When not**: For class/method renames (use a property or wrapper) or when a major version permits a hard break — a plain `OldName = NewName` alias is simpler if no warning is needed. (P198's compatibility shim is for environment variation, not renames.)

**Without this pattern** (anti-pattern):
```python
# ❌ Bad: a silent alias with no warning — users never learn the new name
BeartypeAbbyException = BeartypeDoorException
# downstream keeps importing the old name forever; there is no migration pressure
```

**With this pattern**:
```python
# beartype — beartype/roar/__init__.py:112-155
# ✅ Good: __getattr__ remaps old→new names and warns; unknown names raise AttributeError
def __getattr__(attr_deprecated_name: str) -> object:
    from beartype._util.module.utilmoddeprecate import deprecate_module_attr
    return deprecate_module_attr(
        attr_deprecated_name=attr_deprecated_name,
        attr_deprecated_name_to_nondeprecated_name={
            'BeartypeAbbyException': 'BeartypeDoorException',
            'BeartypeAbbyHintViolation': 'BeartypeDoorHintViolation',
            'BeartypeCallHintPepException': 'BeartypeCallHintViolation',
        },
        attr_nondeprecated_name_to_value=globals(),
    )
```

### suppress(ImportError) for optional dependency registration
`P233` · 11 occurrences · 6 projects: cryptography, setuptools, aiohttp, more-itertools, jsonschema, uvicorn

**What**: Optional-feature registrations are wrapped in `with suppress(ImportError):` blocks so that if the optional library isn't installed the block is silently skipped — the feature is simply unavailable, with no error.

**Recognize**:
- `from contextlib import suppress` then `with suppress(ImportError):` blocks at module top
- Inside the block: an import of the optional lib plus a registration call (e.g. a `@_checks_drafts(...)`-decorated validator)
- Multiple adjacent `with suppress(ImportError):` blocks, one per optional feature
- A companion boolean flag (`_bcrypt_supported = True/False`) sometimes set in the try path

**Why**: Format validation for URI/hostname/color etc. needs third-party libs users may not have. Making them hard dependencies bloats the install. `try/except ImportError` works, but `with suppress(ImportError):` scopes the optional registration to a visually clear block — readers see exactly which functions are optional and which lib each needs. Benefit: graceful degradation with minimal ceremony; soft dependencies. Cost: failures are silent, so a genuinely broken optional install looks identical to "not installed" — debugging requires opting into louder errors. For sophisticated deferred loading, see P235.

**When**: When an optional feature maps 1:1 to an optional import and you want it auto-enabled if the lib is present, silently absent otherwise.

**When not**: When the optional dependency is large or its failure modes matter (use the lazy-proxy module approach, P235) or when absence should be a loud error — then don't suppress.

**Without this pattern** (anti-pattern):
```python
# ❌ Bad: a hard import turns the optional lib into a required dependency
from fqdn import FQDN

def is_host_name(instance) -> bool:
    return FQDN(instance, min_labels=1).is_valid
# ImportError at module load — jsonschema now requires fqdn to even import
```

**With this pattern**:
```python
# jsonschema — jsonschema/_format.py:210-225
# ✅ Good: each optional checker is registered inside its own suppress(ImportError) block
with suppress(ImportError):
    from fqdn import FQDN

    @_checks_drafts(
        draft3="host-name", draft4="hostname", draft6="hostname",
        draft7="hostname", draft201909="hostname", draft202012="hostname",
        raises=ValueError,
    )
    def is_host_name(instance) -> bool:
        if not isinstance(instance, str):
            return True
        return FQDN(instance, min_labels=1).is_valid

with suppress(ImportError):
    from rfc3339_validator import validate_rfc3339

    @_checks_drafts(name="date-time")
    def is_datetime(instance) -> bool:
        if not isinstance(instance, str):
            return True
        return validate_rfc3339(instance.upper())
```

### Pre-instantiated module-level constants for hot-path objects
`P289` · 3 occurrences · 3 projects: aiohttp, uvicorn, cryptography

**What**: Expensive-to-construct objects used in hot paths are pre-instantiated once at module level and reused across all calls, amortizing construction cost.

**Recognize**:
- Module-level UPPER_SNAKE constants holding fully-constructed objects: `_PKCS7_128 = padding.PKCS7(128)`
- A comment like "Hoisted to module level so each operation doesn't reconstruct them"
- `Final[...]` type annotations signaling "construct once, never rebind"
- Pre-built lookup dicts (`STATUS_PHRASES = {... for status_code in range(100, 600)}`)

**Why**: Crypto padding/hash objects and large lookup tables are stateless after construction but carry configuration; building them per-call adds overhead in tight loops (decrypting many tokens, mapping every status code). Module-level singletons amortize the cost to once per process. Benefit: hot-path speedup with zero per-call allocation. Cost: module import pays the construction cost up front (even if the feature is never used), and the objects must be truly stateless/reentrant — any mutation breaks all callers.

**When**: When a stateless, configuration-carrying object (or a large immutable lookup) is constructed inside a hot loop and used many times.

**When not**: When the object is cheap to construct, carries per-call state, or is rarely used — construct it lazily/locally instead (see P110 for rarely-used backends).

**Without this pattern** (anti-pattern):
```python
# ❌ Bad: reconstruct the padding object on every decrypt call
def decrypt(self, token):
    padder = padding.PKCS7(128)          # rebuilt every call
    hasher = hashes.SHA256()             # rebuilt every call
    ...
# N tokens = N constructions of identical, stateless objects
```

**With this pattern**:
```python
# cryptography — src/cryptography/fernet.py:28-30
# ✅ Good: stateless hot-path objects are hoisted to module level and reused
# Hoisted to module level so each operation doesn't reconstruct them.
_PKCS7_128 = padding.PKCS7(128)
_SHA256 = hashes.SHA256()
```

### Type alias as complete protocol contract
`P369` · 3 occurrences · 3 projects: aiohttp, uvicorn, starlette

**What**: An entire application interface is expressed as a `Callable` type alias (e.g. `ASGIApp = Callable[[Scope, Receive, Send], Awaitable[None]]`) — no ABC, no Protocol class, no abstract methods.

**Recognize**:
- A type alias assigned a `Callable[[...], ...]` form, often in a `types.py` module
- No `class X(Protocol):` and no `@abstractmethod` — the alias *is* the contract
- Companion aliases for the parameters (`Scope`, `Receive`, `Send`) are also plain aliases/Mappings
- Anything matching the signature satisfies the protocol at runtime (pure duck typing)

**Why**: Type aliases are zero-overhead at runtime — no metaclass, no ABC registration, no `isinstance` checks. The `Callable` signature is both the contract and the documentation; any callable matching it qualifies. Benefit: maximum duck-typing flexibility with zero runtime cost and minimal ceremony. Cost: no runtime checkability (unlike `@runtime_checkable` Protocol, P021) and no place to hang docstrings or shared methods — the contract lives only in the type checker.

**When**: When the interface is a single callable shape shared across many implementations and you want zero runtime overhead (framework protocols like ASGI/WSGI).

**When not**: When you need runtime `isinstance` checks, shared method implementations, or rich per-method documentation — use `Protocol` (P021, Protocol over ABC) or an ABC instead.

**Without this pattern** (anti-pattern):
```python
# ❌ Bad: an ABC for a single-callable protocol adds metaclass overhead and registration ceremony
class ASGIApp(ABC):
    @abstractmethod
    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None: ...

# every app must subclass ASGIApp — but the protocol is really just "be callable"
```

**With this pattern**:
```python
# starlette — starlette/types.py:17-19
# ✅ Good: the entire ASGI interface is one Callable alias — zero runtime overhead, pure duck typing
Scope = MutableMapping[str, Any]
Message = MutableMapping[str, Any]
Receive = Callable[[], Awaitable[Message]]
Send = Callable[[Message], Awaitable[None]]
ASGIApp = Callable[[Scope, Receive, Send], Awaitable[None]]
```
