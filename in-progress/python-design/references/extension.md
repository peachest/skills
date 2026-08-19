## Plugin Architecture, Config Management, State Context (10 patterns)

### Hook spec / impl separation
`P029` · 15 occurrences · 13 projects: celery, Pillow, hypothesis, tornado, setuptools, pytest, click, textual, requests, pluggy, loguru, sqlalchemy, flask

**What**: Two decorators (`@hookspec` and `@hookimpl`) define a contract and its implementation separately; they stamp attributes on functions rather than wrapping them, so functions stay directly callable.

**Recognize**:
- `@hookspec` marks a specification function and `@hookimpl` marks an implementation, both bearing the same function name
- The decorators attach metadata attributes to the function object instead of returning a wrapper — the original function remains directly callable
- Specs and impls are discovered by name matching against a hook caller registry, not via `isinstance`/inheritance checks
- A manager object collects impls and multicalls every registered impl for a given spec name

**Why**: Decouples contract definition from implementation discovery so multiple independent plugins can satisfy one named contract without inheriting from a base class. Trade-off: you gain dynamic, name-based multi-dispatch at the cost of indirection — call sites no longer show which concrete code runs, and the two-decorator protocol must be learned.

**When**: When you need a plugin system where multiple implementations satisfy a named contract that is discovered dynamically at runtime rather than fixed by inheritance.

**When not**: For single-implementation interfaces, use Protocol over ABC (P021) or pass a single callback directly; the spec/impl machinery is overkill when only one impl will ever exist.

**Without this pattern** (anti-pattern):
```python
# ❌ Bad: contract and implementation coupled via inheritance; every plugin must subclass
from abc import ABC, abstractmethod

class DataProcessor(ABC):
    @abstractmethod
    def process_data(self, data):
        ...

class MyPlugin(DataProcessor):
    def process_data(self, data):
        return data.upper()

# Discovery requires isinstance checks against the ABC; functions aren't directly
# callable until instantiated, and adding a plugin means editing a registration branch.
```

**With this pattern**:
```python
# pluggy — pluggy/_hooks.py
# ✅ Good: spec and impl are separate, discoverable by name, functions stay callable

@hookspec
def process_data(self, data):
    """Contract: any plugin may implement process_data(data)."""
    ...

@hookimpl
def process_data(data):
    """Implementation: registered by name, called directly if needed."""
    return data.upper()

# The PluginManager collects @hookimpl functions matching each @hookspec name
# and multicalls them — no subclassing, no isinstance checks, funcs stay callable.
```

### Swappable execution strategy
`P030` · 11 occurrences · 11 projects: cryptography, celery, beartype, hypothesis, tornado, Pillow, pytest, setuptools, textual, pluggy, anyio

**What**: A single function-reference attribute (e.g. `_inner_hookexec`) is swapped at runtime to change execution strategy; tracing or monitoring plug in by replacing one attribute, and `undo()` restores the previous value.

**Recognize**:
- An attribute holding a callable default, e.g. `self._inner_hookexec = _multicall`
- Instrumentation works by reassigning that one attribute to a wrapper (`self._inner_hookexec = traced_hookexec`) rather than decorating every call site
- An `undo()` / restore method that swaps the previous callable back
- The core dispatch path always calls through the swappable attribute, never a hardcoded function

**Why**: One attribute swap enables cross-cutting instrumentation (tracing, profiling, monitoring) around an entire execution path without touching any call site. Trade-off: you gain a single, reversible instrumentation seam at the cost of an extra indirection on every dispatch and the discipline to always `undo()`.

**When**: When an optional, cross-cutting concern (tracing, monitoring, debugging) must wrap a core execution path without modifying the path's call sites.

**When not**: For one-off instrumentation of a single function, a decorator on that function is simpler; for domain-level strategy selection, pass the strategy callable in as an explicit parameter.

**Without this pattern** (anti-pattern):
```python
# ❌ Bad: instrumentation scattered across every dispatch site
import time

def hookexec(hook, callers):
    try:
        start = time.time()
        result = _multicall(hook, callers)
        print(f"{hook} took {time.time() - start:.3f}s")
        return result
    except Exception:
        print(f"{hook} failed")
        raise

# Enabling or disabling tracing means editing each call site or hand-wrapping
# every function; there is no single seam and no clean undo.
```

**With this pattern**:
```python
# pluggy — pluggy/_manager.py:72,347-370
# ✅ Good: swap one attribute to install tracing, undo() restores it

class PluginManager:
    def __init__(self):
        self._inner_hookexec = _multicall      # default strategy

    def enable_tracing(self):
        oldcall = self._inner_hookexec

        def traced_hookexec(hook, callers, kwargs):
            # ... record before/after ...
            return oldcall(hook, callers, kwargs)

        self._inner_hookexec = traced_hookexec  # one-attribute swap
        return self.undo_tracing

    def undo_tracing(self):
        # restore is trivial because only one attribute changed
        self._inner_hookexec = _multicall
```

### Config layering with per-field merge semantics
`P033` · 10 occurrences · 9 projects: celery, setuptools, hypothesis, tornado, requests, sqlalchemy, dbt-core, jinja2, flask

**What**: A config cascade (project → profile → model → runtime) where different fields use different merge strategies — replace-if-none, append, or deep merge — rather than a single blanket override.

**Recognize**:
- A pairs/tuple list mapping attribute names to config keys: `from_config = (('serializer', 'task_serializer'), ...)`
- A merge loop that applies per-field rules, e.g. `if getattr(cls, attr, None) is None: setattr(cls, attr, conf[config_name])` (replace-if-none)
- Multiple `from_*` loaders (`from_pyfile`, `from_object`, `from_envvar`, `from_mapping`) each feeding one layered dict
- Per-key logic distinguishing "only inherit when unset" from "always overwrite" from "append to list"

**Why**: Different config fields need different precedence — some should inherit only when unset, some append across layers, some deep-merge nested dicts. A single `dict.update()` cannot express that. Trade-off: you gain correct field-specific precedence at the cost of more complex merge logic that is harder to reason about when inspecting the final resolved value.

**When**: When configuration originates from multiple layered sources (defaults, files, env, CLI) and individual fields require distinct merge rules.

**When not**: For flat single-source config, use Environment variable defaults with typed coercion (P173) or a plain config dict; the per-field machinery is unjustified when one override rule covers everything.

**Without this pattern** (anti-pattern):
```python
# ❌ Bad: blanket dict.update overwrites everything, losing append/deep-merge semantics
final_config = {}
final_config.update(defaults)
final_config.update(file_config)
final_config.update(env_config)

# list-valued keys (e.g. 'middleware') are replaced instead of appended across layers;
# nested dicts are overwritten wholesale rather than deep-merged; 'replace-if-none'
# fields get clobbered even when a higher layer left them intentionally unset.
```

**With this pattern**:
```python
# celery — celery/app/task.py:344-375
# ✅ Good: per-field mapping with replace-if-none merge semantics

from_config = (
    ('serializer', 'task_serializer'),
    ('rate_limit', 'task_default_rate_limit'),
    ('priority', 'task_default_priority'),
    ('track_started', 'task_track_started'),
    ('acks_late', 'task_acks_late'),
    # ... more (attr_name, config_name) pairs ...
)

@classmethod
def bind(cls, app):
    conf = app.conf
    for attr_name, config_name in cls.from_config:
        # replace-if-none: only inherit from config when the attr is unset
        if getattr(cls, attr_name, None) is None:
            setattr(cls, attr_name, conf[config_name])
```

### Signal: observer pattern with weak references and robust dispatch
`P058` · 8 occurrences · 7 projects: celery, Pillow, hypothesis, textual, sqlalchemy, matplotlib, polars

**What**: A `Signal` object maintains a list of receiver callables; `connect()` registers receivers with optional `dispatch_uid` dedup, `weak` references for automatic cleanup, and `sender` filtering, while `send()` invokes all live receivers, isolating exceptions per-receiver and returning `(receiver, response_or_exception)` pairs.

**Recognize**:
- A `Signal` class with `connect()` / `send()` methods and a `self.receivers` list
- Receivers stored via `weakref.ref` so dead bound methods are garbage-collected, with a `_dead_receivers` flag for lazy cleanup
- A `dispatch_uid` parameter that deduplicates registrations, and a `sender` filter so receivers fire only for matching senders
- `send()` catches exceptions per receiver and returns a list of `(receiver, response_or_exception)` tuples rather than propagating the first failure

**Why**: A distributed task system emits events at many lifecycle points (received, started, succeeded, failed, retried); the observer pattern decouples emission from handling. Weak references prevent leaks when bound-method handlers are GC'd, and per-receiver exception isolation stops one broken handler from crashing the dispatch chain. Trade-off: you gain loose, leak-free, fault-isolated eventing at the cost of weakref indirection, silent dropping of dead receivers, and exception isolation that can mask handler bugs.

**When**: When a system emits lifecycle events that multiple independent extensions must observe without coupling to the emitter.

**When not**: For 1:1 notifications where the sender knows its single listener, pass a callback directly; for typed multi-implementation contracts, use Hook spec/impl separation (P029).

**Without this pattern** (anti-pattern):
```python
# ❌ Bad: plain callback list with no dedup, no weakrefs, no exception isolation
class Signal:
    def __init__(self):
        self.receivers = []

    def connect(self, fn):
        self.receivers.append(fn)   # duplicates accumulate; bound methods leak

    def send(self, **kwargs):
        for fn in self.receivers:
            fn(**kwargs)            # one raising handler aborts all subsequent ones
```

**With this pattern**:
```python
# celery — celery/utils/dispatch/signal.py:81-130
# ✅ Good: weakrefs, dispatch_uid dedup, sender filter, per-receiver isolation

import threading
import weakref

class Signal:
    def __init__(self, providing_args=None, use_caching=False, name=None):
        self.receivers = []
        self.lock = threading.Lock()
        self.use_caching = use_caching
        self.name = name
        self.sender_receivers_cache = weakref.WeakKeyDictionary() if use_caching else {}
        self._dead_receivers = False

    def connect(self, *args, **kwargs):
        def _handle_options(sender=None, weak=True, dispatch_uid=None, retry=False):
            def _connect_signal(fun):
                options = {'dispatch_uid': dispatch_uid, 'weak': weak}
                if retry:
                    options['weak'] = False
                    if not dispatch_uid:
                        options['dispatch_uid'] = _make_id(fun)
                    fun = _retry_receiver(fun)
                    fun._dispatch_uid = options['dispatch_uid']
                # weak=True stores a weakref so dead handlers are GC'd;
                # dispatch_uid dedups; sender filters who receives the event.
                self._connect_signal(fun, sender, options['weak'], options['dispatch_uid'])
                return fun
            return _connect_signal
        if args and callable(args[0]):
            return _handle_options(*args[1:], **kwargs)(args[0])
        return _handle_options(*args, **kwargs)

    # send() (not shown) iterates live receivers, catches exceptions per receiver,
    # and returns [(receiver, response_or_exc), ...] — one bad handler can't
    # crash the chain, and dead weakrefs are cleaned lazily.
```

### Registry as dict subclass with __missing__ guard
`P064` · 7 occurrences · 6 projects: celery, Pillow, setuptools, click, starlette, polars

**What**: A registry that inherits from `dict` and overrides `__missing__` to raise a custom `NotRegistered` error when an unregistered key is accessed; registration accepts either a class (auto-instantiated) or an instance, keyed by the item's `.name` attribute.

**Recognize**:
- `class FooRegistry(dict):` with a `__missing__(self, key)` override that raises a domain-specific error (e.g. `NotRegistered`)
- A `register()` method that does `inspect.isclass(task) and task() or task` to auto-instantiate classes
- Registered items must expose a `.name` attribute used as the dict key
- Free `dict` ergonomics: iteration, `in`, `.get()`, serialization all work without extra code

**Why**: Inheriting from `dict` gives free serialization, iteration, and standard operations; the `__missing__` override turns a silent `KeyError` into a meaningful domain error users can catch; auto-instantiation lets callers write `registry.register(MyTaskClass)` instead of `registry.register(MyTaskClass())`. Trade-off: you gain dict ergonomics and clear errors at the cost of coupling the registry's mutation surface to all of `dict`'s methods, and auto-instantiation hides construction side effects.

**When**: When you need a name-keyed lookup of plugins, tasks, or components with a clear "not registered" error and want standard dict ergonomics for free.

**When not**: For structural interfaces without a central registry, use Protocol over ABC (P021); when entries have complex lifecycle or ordering needs, use a dedicated registry class instead of a `dict` subclass.

**Without this pattern** (anti-pattern):
```python
# ❌ Bad: plain dict with cryptic KeyError and manual instantiation
registry = {}
registry["send_email"] = SendEmailTask()   # must instantiate by hand every time
registry["send_email"] = SendEmailTask()   # silent duplicate, no dedup

def get_task(name):
    return registry[name]   # KeyError('send_emial') — a typo gives no domain hint
```

**With this pattern**:
```python
# celery — celery/app/registry.py:14-50
# ✅ Good: dict subclass, __missing__ domain error, auto-instantiation, .name key

import inspect

class TaskRegistry(dict):
    """Map of registered tasks."""
    NotRegistered = NotRegistered

    def __missing__(self, key):
        raise self.NotRegistered(key)          # meaningful domain error

    def register(self, task):
        if task.name is None:
            raise InvalidTaskError(
                'Task class {!r} must specify .name attribute'.format(
                    type(task).__name__))
        task = inspect.isclass(task) and task() or task   # auto-instantiate
        add_autoretry_behaviour(task)
        self[task.name] = task                 # keyed by .name

    def unregister(self, name):
        try:
            self.pop(getattr(name, 'name', name))
        except KeyError:
            raise self.NotRegistered(name)
```

### ContextVar + LocalProxy for implicit context access
`P068` · 9 occurrences · 6 projects: hypothesis, textual, loguru, anyio, flask, werkzeug

**What**: Per-request/per-app state is stored in `ContextVar` objects; module-level `LocalProxy` instances read from those ContextVars, providing implicit access to `current_app`, `request`, `session`, and `g` without passing them as parameters, and raising a descriptive error when accessed outside a context.

**Recognize**:
- Module-level `ContextVar` declarations: `_cv_app = ContextVar("flask.app_ctx")`
- `LocalProxy(cv, "attr", unbound_message=...)` proxies bound to those ContextVars
- Familiar module-level names (`request`, `current_app`, `g`, `session`) that are proxies, not real objects
- Accessing a proxy outside its context raises a descriptive `RuntimeError` via `unbound_message`

**Why**: View functions and helpers access request/app state without explicit parameter passing, keeping signatures clean. `ContextVar` (over `threading.local`) is async-safe — it works correctly with asyncio, greenlets, and concurrent requests. The `LocalProxy` transparently delegates attribute access so `request.json` behaves exactly as if `request` were a local variable. Trade-off: you gain clean signatures and async-safe implicit access at the cost of state that is harder to test and trace, with proxy errors surfacing only at access time rather than at bind time.

**When**: When a framework needs request-scoped, global-like access (current request, app, session) that must be async-safe and correct across concurrent requests.

**When not**: When you can pass context explicitly, prefer explicit parameters for testability; for thread-only code where async safety is irrelevant, `threading.local` may suffice.

**Without this pattern** (anti-pattern):
```python
# ❌ Bad: module-level mutable globals clobbered by concurrent requests
_request = None
_app = None

def handle(request):
    global _request, _app
    _request = request     # concurrent requests overwrite each other's state
    _app = current_app
    return view()

# Under asyncio or threads, _request from request A is visible to request B.
```

**With this pattern**:
```python
# flask — src/flask/globals.py:1-50
# ✅ Good: ContextVar + LocalProxy — async-safe implicit per-request access

from contextvars import ContextVar
from werkzeug.local import LocalProxy

_cv_app: ContextVar[AppContext] = ContextVar("flask.app_ctx")
current_app: Flask = LocalProxy(_cv_app, "app", unbound_message=_no_app_msg)
g = LocalProxy(_cv_app, "g", unbound_message=_no_app_msg)

_cv_request: ContextVar[RequestContext] = ContextVar("flask.request_ctx")
request: Request = LocalProxy(_cv_request, "request", unbound_message=_no_req_msg)
session: SessionMixin = LocalProxy(_cv_request, "session", unbound_message=_no_req_msg)

# Each request gets its own ContextVar binding; concurrent requests are isolated.
# `request.json` works as if request were local; accessing it outside a context
# raises a descriptive error instead of returning stale data.
```

### Context manager as request/app lifecycle boundary
`P069` · 10 occurrences · 9 projects: setuptools, aiohttp, click, loguru, sqlalchemy, starlette, flask, polars, uvicorn

**What**: `AppContext` and `RequestContext` implement `__enter__`/`__exit__`; `push()` binds the context to the current `ContextVar`, `pop()` runs teardown handlers and resets the token, and the request lifecycle (`ctx.push()` → dispatch → `ctx.pop(error)`) is wrapped in `try/finally` so teardown always runs.

**Recognize**:
- A context class with `push()`/`pop()` plus `__enter__`/`__exit__`
- `push()` calls `_cv_app.set(self)` and stores the returned `Token`; `pop()` calls `_cv_app.reset(token)` in a `finally`
- `pop()` runs `do_teardown_*()` handlers before resetting the token, even when an exception was passed in
- The dispatcher wraps handling in `try: ctx.push(); ... finally: ctx.pop(exc)` — the pipeline boundary between HTTP transport and app logic

**Why**: Context managers guarantee cleanup (teardown handlers, DB disconnection) runs regardless of success or failure; the `try/finally` in the dispatcher guarantees `ctx.pop()` even on unhandled exceptions. This is the boundary between HTTP transport and application logic — everything inside is per-request scoped. Trade-off: you gain guaranteed, ordered cleanup at the cost of teardown state that must be carefully sequenced and nested contexts that need depth tracking.

**When**: When a framework needs guaranteed setup/teardown around request handling that survives exceptions and nests correctly.

**When not**: For single-resource cleanup, a plain `with` on the resource itself suffices; for long-lived app configuration, use Pluggable class attributes for framework extension points (P073).

**Without this pattern** (anti-pattern):
```python
# ❌ Bad: ad-hoc try/finally with cleanup scattered per handler
def handle(request):
    db = connect_db()
    try:
        result = view(request)
    finally:
        db.close()      # every handler must remember its own cleanup;
    return result        # a new error path that skips finally leaks the connection
```

**With this pattern**:
```python
# flask — src/flask/ctx.py:241-290
# ✅ Good: __enter__/__exit__ with push/pop binding ContextVar + guaranteed teardown

from contextvars import ContextVar

_cv_app: ContextVar["AppContext"] = ContextVar("flask.app_ctx")

class AppContext:
    def __init__(self, app: Flask):
        self.app = app
        self.g = app.app_ctx_globals_class()
        self._cv_tokens: list[contextvars.Token] = []

    def push(self) -> None:
        self._cv_tokens.append(_cv_app.set(self))   # bind to current ContextVar
        appcontext_pushed.send(self.app)

    def pop(self, exc=_sentinel) -> None:
        try:
            if len(self._cv_tokens) == 1:
                self.app.do_teardown_appcontext(exc)  # teardown always runs
        finally:
            _cv_app.reset(self._cv_tokens.pop())      # always reset the token

    def __enter__(self) -> "AppContext":
        self.push()
        return self

    def __exit__(self, exc_type, exc_value, tb) -> None:
        self.pop(exc_value)

# The dispatcher wraps handling so ctx.pop() runs even on unhandled exceptions:
#   try:
#       ctx.push()
#       response = self.full_dispatch_request()
#   except Exception as e:
#       error = e
#   finally:
#       ctx.pop(error)
```

### Pluggable class attributes for framework extension points
`P073` · 16 occurrences · 12 projects: setuptools, aiohttp, jsonschema, textual, click, sqlalchemy, starlette, jinja2, flask, werkzeug, polars, uvicorn

**What**: The framework's main class declares overridable class attributes (`request_class`, `response_class`, `session_interface`, `json_provider_class`, `url_map_class`, etc.) that serve as extension points; subclassing and overriding an attribute customizes behavior without rewriting methods — a declarative plugin system where setting the class yields the behavior.

**Recognize**:
- Class-body assignments declaring defaults: `request_class: type[Request] = Request`, `response_class = Response`, `json_provider_class: type[JSONProvider] = DefaultJSONProvider`
- Many such attributes clustered on the framework's central class, each naming a swappable component
- Customization is via subclass + attribute override, not method override or registration
- Methods instantiate these attributes (e.g. `self.request_class(...)`) so overriding the attribute changes behavior everywhere

**Why**: Class attributes are the simplest possible extension point — no registry, no decorator, no hook; just subclass and set an attribute. This is sufficient for most customization needs (custom Request, custom JSON provider, custom session backend) and avoids the complexity of a full plugin system for the common case. The defaults also document exactly what is pluggable. Trade-off: you gain low-ceremony, declarative customization at the cost of all-or-nothing replacement (only one class per attribute, no multi-plugin composition) and no runtime swapping.

**When**: When a framework wants a declarative, low-ceremony way for users to swap default component classes (Request, Response, session backend, JSON provider).

**When not**: When multiple plugins must compose around the same extension point, use Hook spec/impl separation (P029) or Signal (P058); when behavior must swap at runtime, use Swappable execution strategy (P030).

**Without this pattern** (anti-pattern):
```python
# ❌ Bad: component classes hardcoded inside methods
class App:
    def dispatch_request(self, environ):
        request = Request(environ)      # hardcoded; to customize, users must
        response = Response()           # copy-paste and override the whole method
        ...
        return response

# Swapping the Request class means rewriting the entire method body, and the
# pluggable surface is undocumented.
```

**With this pattern**:
```python
# flask — src/flask/app.py:207-250
# ✅ Good: overridable class attributes as declarative extension points

class Flask(App):
    request_class: type[Request] = Request
    response_class: type[Response] = Response
    session_interface: SessionInterface = SecureCookieSessionInterface()

# In sansio/app.py — the base declares the full pluggable surface:
class App(Scaffold):
    config_class = Config
    jinja_environment = Environment
    json_provider_class: type[JSONProvider] = DefaultJSONProvider
    url_rule_class = Rule
    url_map_class = Map
    test_client_class: type[FlaskClient] | None = None
    aborter_class = Aborter

# Users customize by subclassing and setting one attribute — no methods rewritten:
#   class MyApp(Flask):
#       request_class = MyRequest
#       json_provider_class = MyJSONProvider
```

### Environment variable defaults with typed coercion
`P173` · 4 occurrences · 4 projects: beartype, loguru, uvicorn, starlette

**What**: All default configuration values are read from environment variables via a single `env()` helper that performs type coercion (`str`, `bool`, `int`) with appropriate parsing and validation, and each parameter has a sensible fallback default when the env var is unset.

**Recognize**:
- A central `env(key, type_, default=...)` helper that reads `os.environ` and coerces
- Bool parsing that maps `"1"`, `"true"`, `"yes"`, `"on"` → `True` and `"0"`, `"false"`, `"no"`, `"off"` → `False`, raising `ValueError` on anything else
- A naming convention like `PREFIX_PARAM` (e.g. `LOGURU_...`) making env vars discoverable
- Every config parameter passes a `default=` so missing env vars don't yield `None`

**Why**: Environment variables enable configuration without code changes — essential for Docker, CI, and 12-factor apps. Typed coercion ensures bool env vars are actual booleans (not the string `"true"`, which is truthy by accident), and centralizing the env-reading logic avoids scattered `os.environ.get()` calls with inconsistent parsing. Trade-off: you gain one consistent, typed config source at the cost of a single helper that must handle every type, and env var typos silently fall back to defaults rather than erroring.

**When**: When configuration must be overridable via environment variables with type safety, as is typical of 12-factor and containerized applications.

**When not**: For layered multi-source config with per-field merge semantics, use Config layering with per-field merge semantics (P033); for swapping app component classes, use Pluggable class attributes for framework extension points (P073).

**Without this pattern** (anti-pattern):
```python
# ❌ Bad: scattered os.environ.get with string results and inconsistent parsing
import os

DEBUG = os.environ.get("DEBUG", "false")   # a string, not a bool
PORT = os.environ.get("PORT", 8000)         # default is int, env value is str
TIMEOUT = os.environ.get("TIMEOUT")         # no default — returns None silently

# 'DEBUG = "false"' is a non-empty string, which is truthy — debug mode is
# always on. PORT from the env is a string and breaks int arithmetic.
```

**With this pattern**:
```python
# loguru — loguru/_defaults.py:4-28
# ✅ Good: single env() helper with typed coercion and defaults

from os import environ

def env(key, type_, default=None):
    if key not in environ:
        return default
    val = environ[key]
    if type_ is str:
        return val
    if type_ is bool:
        if val.lower() in ["1", "true", "yes", "y", "ok", "on"]:
            return True
        if val.lower() in ["0", "false", "no", "n", "nok", "off"]:
            return False
        raise ValueError(
            "Invalid environment variable '%s' (expected a boolean): '%s'" % (key, val))
    if type_ is int:
        try:
            return int(val)
        except ValueError:
            raise ValueError(
                "Invalid environment variable '%s' (expected an integer): '%s'"
                % (key, val)) from None

# Each config param uses a typed default:
#   LOGURU_DEBUG = env("LOGURU_DEBUG", bool, False)
#   LOGURU_DIAGNOSE = env("LOGURU_DIAGNOSE", bool, False)
```

### Scope as shared mutable context dict
`P386` · 3 occurrences · 3 projects: aiohttp, uvicorn, starlette

**What**: All request context flows through a mutable dict (`scope`) passed by reference; middleware adds keys (`scope["app"] = self`), routes update path params (`scope.update(child_scope)`), and downstream code reads via `scope.get()` — there is no immutable request object; the dict IS the context.

**Recognize**:
- An ASGI-style `(scope, receive, send)` call signature across every middleware and app
- Middleware mutates the shared dict in place: `scope["app"] = self`, `scope["scheme"] = ...`, `scope.update(child_scope)`
- Downstream code reads context via `scope.get(key)` or `scope[key]` rather than from a typed request object
- No new context object is constructed per layer — the same dict reference threads through the entire stack

**Why**: Mutable dict passing avoids creating new objects at each middleware layer; each layer can add context without return values, and in a cooperative framework this simplicity wins over defensive copying. Trade-off: you gain minimal allocation and a uniform context shape at the cost of any layer being able to mutate anything (no immutability guarantee) and key typos failing silently.

**When**: When a cooperative framework needs layers of middleware to accumulate per-request context with minimal allocation and a single shared shape.

**When not**: When you need immutability guarantees or typed access, use ContextVar + LocalProxy for implicit context access (P068) or a typed request object; mutable scope is harder to reason about in tests.

**Without this pattern** (anti-pattern):
```python
# ❌ Bad: each middleware rebuilds and returns a new immutable request object
async def auth_middleware(request, receive, send):
    user = authenticate(request.headers)
    new_request = request.replace(user=user)   # rebuild on every layer
    return new_request                          # every downstream layer must
                                                # thread the returned object,
                                                # and allocations pile up

async def logging_middleware(request, receive, send):
    request = await auth_middleware(request, receive, send)
    request = request.replace(log_id=generate_id())   # another rebuild
    return await handler(request, receive, send)
```

**With this pattern**:
```python
# starlette — starlette/applications.py:82-84, 488-490
# ✅ Good: shared mutable scope dict threaded through every layer

class Starlette:
    async def __call__(self, scope, receive, send):
        scope["app"] = self                         # middleware adds context in place
        await self.middleware_stack(scope, receive, send)

# Router updates scope with the matched route's child_scope:
#   if match == Match.FULL:
#       scope.update(child_scope)                   # path params merged in place
#       await route.handle(scope, receive, send)

# Downstream reads via scope.get(); the same dict reference threads through
# proxy-headers middleware (scope["scheme"] = ...), the router, and the endpoint.
```
