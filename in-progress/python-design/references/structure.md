
## Interface Design (15 patterns)

### Protocol over ABC
*33 occurrences across 20 projects: Pillow, anyio, attrs, beartype, celery, click, cryptography, flask, httpx, hypothesis, jsonschema, more-itertools, polars, pytest, requests, rich, starlette, structlog, textual, tornado*

typing.Protocol for structural subtyping — any class with right methods satisfies interface, no inheritance needed. More Pythonic than ABCs for capability interfaces.

**Why**: Request bodies can come from files, streams, strings, or custom iterables — all need .read(). Rather than defining an ABC and requiring inheritance (which excludes third-party file-like objects), a Protocol accepts any object with the right method. This is the modern Python equivalent of the AuthBase __call__ pattern — structural typing via Protocol instead of nominal typing via ABC. The runtime_checkable flag allows defensive isinstance() checks where needed. [Merged from P364: Allows Pillow to accept numpy arrays, Arrow tables, or any future array format without hard dependencies. The Protocol describes the duck-typed interface — any object with __array_interface__ qualifies. This is the type-safe way to accept 'anything numpy-like' without importing numpy.]

```python
# flask — src/flask/typing.py:1-95
ResponseValue = t.Union[
    "Response", str, bytes, list[t.Any],
    t.Mapping[str, t.Any],
    t.Iterator[str], t.Iterator[bytes],
    cabc.AsyncIterable[str], cabc.AsyncIterable[bytes],
]

ResponseReturnValue = t.Union[
    ResponseValue,
    tuple[ResponseValue, HeadersValue],
    tuple[ResponseValue, int],
    tuple[ResponseValue, int, HeadersValue],
    "WSGIApplication",
]

RouteCallable = t.Union[
    t.Callable[..., ResponseReturnValue],
    t.Callable[..., t.Awaitable[ResponseReturnVal
```

### Small interface, deep implementation
*19 occurrences across 18 projects: Pillow, anyio, beartype, celery, click, cryptography, flask, httpx, hypothesis, jsonschema, loguru, more-itertools, polars, requests, starlette, textual, toolz, tornado*

Convenience functions lower barrier. Client methods allow reuse. Unified request() ensures all verb methods share behavior. Explicit __all__.

```python
# tornado — tornado/routing.py:501-580
class Matcher:
    """Represents a matcher for request features."""
    def match(self, request: httputil.HTTPServerRequest) -> Optional[Dict[str, Any]]:
        raise NotImplementedError()

class AnyMatches(Matcher):
    def match(self, request):
        return {}

class HostMatches(Matcher):
    def __init__(self, host_pattern):
        self.host_pattern = re.compile(host_pattern)
    def match(self, request):
        if self.host_pattern.match(request.host_name):
            return {}
       
```

### Transport as Protocol with adapter implementations
*14 occurrences across 10 projects: anyio, celery, flask, httpx, hypothesis, loguru, requests, starlette, textual, tornado*

Protocol defines one method. Multiple adapters: real (production), mock (testing), WSGI/ASGI (server-side testing).

```python
# tornado — tornado/routing.py:201-240
class Router(httputil.HTTPServerConnectionDelegate):
    """Abstract router interface."""
    def find_handler(
        self, request: httputil.HTTPServerRequest, **kwargs: Any
    ) -> Optional[httputil.HTTPMessageDelegate]:
        raise NotImplementedError()
    def start_request(
        self, server_conn: object, request_conn: httputil.HTTPConnection
    ) -> httputil.HTTPMessageDelegate:
        return _RoutingDelegate(self, server_conn, request_conn)

class RuleRouter(Router):
    def fin
```

### @final for non-extendable classes
*10 occurrences across 10 projects: Pillow, anyio, celery, click, hypothesis, pluggy, pytest, starlette, textual, tornado*

Building blocks marked @final. Extension through composition, not subclassing. Signals intent: fixed building block, extend elsewhere.

```python
# tornado — tornado/web.py:3270-3293
class OutputTransform:
    """A transform modifies the result of an HTTP request (e.g., GZip encoding)

    Applications are not expected to create their own OutputTransforms
    or interact with them directly; the framework chooses which transforms
    (if any) to apply.
    """
    def __init__(self, request: httputil.HTTPServerRequest) -> None:
        pass
    def transform_first_chunk(self, status_code, headers, chunk, finishing):
        return status_code, headers, chunk
    def transform
```

### __getattr__ as dynamic attribute factory
*8 occurrences across 7 projects: Pillow, cryptography, hypothesis, jsonschema, polars, pytest, textual*

MarkGenerator.__getattr__ creates a new MarkDecorator for any attribute name accessed on the pytest.mark singleton. Unknown names trigger a warning (configurable to hard error via strict_markers). Known names from config are cached in a set. The factory is the only way to access marks — there is no pre-registration step.

**Why**: Marks are open-ended: users define their own mark names without registration. Pre-defining all marks would require a registration step and still couldn't cover user-defined marks. __getattr__ makes any attribute access produce a valid MarkDecorator, then validation happens lazily (warning or error) based on config. This separates mark creation (always succeeds) from mark validation (configurable strictness). The warning-not-error default allows progressive adoption of mark registration.

```python
# pytest — src/_pytest/mark/structures.py:510-555
class MarkGenerator:
    def __getattr__(self, name: str) -> MarkDecorator:
        """Generate a new MarkDecorator with the given name."""
        if name[0] == "_":
            raise AttributeError("Marker name must NOT start with underscore")
        if self._config is not None:
            if name not in self._markers:
                for line in self._config.getini("markers"):
                    marker = line.split(":")[0].split("(")[0].strip()
                    self._markers.add(marker)
```

### MethodView: __init_subclass__ for automatic method dispatch
*7 occurrences across 4 projects: Pillow, anyio, flask, textual*

MethodView uses __init_subclass__ to scan the class for HTTP method names (get, post, put, etc.) and automatically populate the methods attribute. A class-based view dispatches by HTTP method to instance methods. init_every_request controls whether a new instance is created per request or shared.

**Why**: REST endpoints naturally map to HTTP methods. __init_subclass__ eliminates the boilerplate of manually listing methods — defining `def get(self)` automatically registers GET. The init_every_request flag (default True, set False for stateless views) is a performance optimization: a single instance handles all requests when no per-request state is needed on self. [Merged from P251: Eliminates boilerplate registration — defining a Message subclass automatically creates the handler name convention. The @on decorator provides selector-based routing (match by CSS selector) without a separate registration call. Metaclass collection at class-definition time means dispatch is O(1) lookup at runtime, not reflection per-message.]

```python
# flask — src/flask/views.py:37-100, 155-190
class View:
    init_every_request: t.ClassVar[bool] = True
    decorators: t.ClassVar[list] = []

    @classmethod
    def as_view(cls, name, *class_args, **class_kwargs):
        if cls.init_every_request:
            def view(**kwargs):
                self = view.view_class(*class_args, **class_kwargs)
                return self.dispatch_request(**kwargs)
        else:
            self = cls(*class_args, **class_kwargs)
            def view(**kwargs):
                return self.dispatch_re
```

### Mixin-based interface composition for model classes
*7 occurrences across 7 projects: Pillow, anyio, cryptography, polars, requests, starlette, textual*

Request and PreparedRequest are assembled from focused mixins: RequestEncodingMixin (URL/body encoding), RequestHooksMixin (hook registration/dispatch). Each mixin provides a cohesive set of methods and carries its own type annotations. The main class inherits multiple mixins to compose the full interface without a monolithic base class.

**Why**: Encoding logic (params, files, multipart) and hook logic (register, dispatch) are independent concerns. Putting them in mixins lets each be tested in isolation and reused in other contexts (e.g. PreparedRequest needs encoding but also hooks). This is the pre-Protocol era approach to interface composition — mixins define method bundles, and classes assemble them via multiple inheritance. Modern Python would use Protocol composition, but mixins remain useful when shared implementation (not just interface) is needed.

```python
# starlette — starlette/responses.py:39-127
class Response:
    media_type = None
    charset = "utf-8"

    def __init__(self, content=None, status_code=200, headers=None, media_type=None, background=None):
        self.status_code = status_code
        if media_type is not None:
            self.media_type = media_type
        self.background = background
        self.body = self.render(content)
        self.init_headers(headers)

    def render(self, content: Any) -> bytes | memoryview:
        ...

class HTMLResponse(Response):
    me
```

### Backend capability flags as class-level attributes
*5 occurrences across 5 projects: Pillow, celery, cryptography, textual, tornado*

A base Backend class declares boolean capability flags as class attributes: `supports_native_join`, `supports_autoexpire`, `persistent`. Subclasses (Redis, Database, RPC, etc.) override these to declare what they support. Callers check `backend.supports_native_join` instead of `isinstance(backend, RedisBackend)`, enabling capability-based dispatch without coupling to concrete types.

**Why**: Different result backends (Redis, database, S3, RPC, filesystem) have wildly different capabilities. Some support native join (Redis pipelining), some auto-expire results (TTL), some are persistent. Using isinstance checks creates tight coupling and makes adding new backends require modifying all check sites. Class-level capability flags shift the contract to 'what can you do' rather than 'what are you', following the Liskov substitution principle. [Merged from P273: Streaming vs buffering is a per-handler capability, not a per-request choice. Using a decorator to set a class flag is cleaner than checking for the presence of a data_received method (which might exist for other reasons) or requiring inheritance from a base class. The flag is checked once at _execute() entry, routing the request through the streaming path. This is a Python-specific alternative to interfaces/traits for declaring capabilities.]

```python
# celery — celery/backends/base.py:109-140
class Backend:
    READY_STATES = states.READY_STATES
    UNREADY_STATES = states.UNREADY_STATES
    EXCEPTION_STATES = states.EXCEPTION_STATES

    supports_native_join = False
    supports_autoexpire = False
    persistent = True

    retry_policy = {
        'max_retries': 20,
        'interval_start': 0,
        'interval_step': 1,
        'interval_max': 1,
    }

    def __init__(self, app, serializer=None, max_cached_results=None, accept=None, expires=None, **kwargs):
        self.app = a
```

### Dual-mode decorator via __call__ dispatch
*5 occurrences across 5 projects: anyio, click, loguru, pytest, starlette*

MarkDecorator.__call__ inspects its arguments: if called with a single callable or class (no extra kwargs), it stamps the mark onto that object and returns it. If called with any other arguments, it returns a NEW MarkDecorator with updated mark args/kwargs. This enables both @pytest.mark.skip (applied directly) and @pytest.mark.skip(reason='x') (returns new decorator) from the same object.

**Why**: A decorator that sometimes applies and sometimes returns a new decorator is the only way to support both @decorator and @decorator(args) syntax from a single object. The alternative (separate objects) requires the user to know which syntax is valid for each mark. This pattern makes all marks uniformly support both forms, which is critical for user experience: the distinction between parameterized and non-parameterized marks is invisible at the call site.

```python
# loguru — loguru/_logger.py:1225-1302
class Catcher:
    def __init__(self, from_decorator):
        self._from_decorator = from_decorator

    def __enter__(self):
        return None

    def __exit__(self, type_, value, traceback_):
        if type_ is None:
            return None
        # ... catch and log exception ...
        return not reraise

    def __call__(self, function):
        if iscoroutinefunction(function):
            async def catch_wrapper(*args, **kwargs):
                with catcher:
                    re
```

### Dual API: legacy aliases bridging to modern defaults
*4 occurrences across 4 projects: anyio, attrs, jsonschema, polars*

Two parallel APIs coexist: legacy (attr.s, attr.ib) with conservative defaults (slots=False, kw_only=False) and modern (attrs.define, attrs.field) with opinionated defaults (slots=True, weakref_slot=True, kw_only=True). The modern API is implemented as thin wrappers calling the legacy implementation with different defaults. Legacy aliases (s=attributes=attrs, ib=attr=attrib) provide backwards compatibility.

**Why**: Libraries with large user bases cannot break existing APIs. The dual API lets new code adopt better defaults (slots by default, keyword-only args) without forcing migration on existing users. The legacy API stays frozen; the modern API is a pure wrapper — no code duplication, just different default values. The aliases (s, ib) are for historical brevity and are never removed.

```python
# jsonschema — jsonschema/validators.py:44-72
def __getattr__(name):
    if name == "ErrorTree":
        warnings.warn("Importing ErrorTree from jsonschema.validators is deprecated. "
                      "Instead import it from jsonschema.exceptions.",
                      DeprecationWarning, stacklevel=2)
        from jsonschema.exceptions import ErrorTree
        return ErrorTree
    elif name == "RefResolver":
        warnings.warn(_RefResolver._DEPRECATION_MESSAGE, DeprecationWarning, stacklevel=2)
        return _RefResolver
    rai
```

### TypedDict kwargs for per-method parameter contracts
*4 occurrences across 4 projects: anyio, polars, requests, textual*

Defines TypedDict subclasses (BaseRequestKwargs, GetKwargs, PostKwargs, DataKwargs, RequestKwargs) that model the **kwargs of each HTTP verb method. Uses inheritance (GetKwargs extends BaseRequestKwargs) to express which kwargs each verb accepts. The TypedDicts are used with Unpack[] in type hints, enabling type-checker validation of keyword arguments per method.

**Why**: All HTTP verbs share most kwargs (headers, cookies, auth, timeout) but differ in specifics: GET has no body but has params; POST has data and json; HEAD defaults allow_redirects to False. Without TypedDict + Unpack, **kwargs is untyped and type checkers can't catch mistakes. By modeling each verb's kwargs as a TypedDict, the type checker knows that requests.get(url, data=...) is suspicious (GET shouldn't have a body) while requests.post(url, data=...) is fine.

```python
# textual — src/textual/_on.py:28-45
def on(message_type: type[Message], selector: str | None = None, **kwargs: str) -> Callable:
    selectors: dict[str, str] = {}
    if selector is not None:
        selectors["control"] = selector
    if kwargs:
        selectors.update(kwargs)

    parsed_selectors: dict[str, tuple[SelectorSet, ...]] = {}
    for attribute, css_selector in selectors.items():
        if attribute == "control":
            if message_type.control == Message.control:
                raise OnDecoratorError("...")
 
```

### opt() as immutable configuration overlay returning new instance
*4 occurrences across 4 projects: beartype, cryptography, loguru, polars*

The opt() method creates a new Logger instance sharing the same _core but with modified per-call options (exception, depth, record, lazy, colors, raw, capture, depth). It does not chain — the last opt() call takes precedence because it resets all options to defaults except the specified ones. The bind() and patch() methods work similarly but only modify their respective tuple positions.

**Why**: opt() enables per-call customization without polluting the global logger state. By returning a new Logger with the same core, the configuration is scoped to the returned instance. The 'last wins' rule (not chaining) keeps the mental model simple — you don't have to reason about accumulated options from multiple opt() calls. The shared _core means all loggers write to the same sinks — the options only affect how the record is created.

```python
# cryptography — src/cryptography/hazmat/primitives/_serialization.py:48-58
class KeySerializationEncryptionBuilder:
    def __init__(self, format: PrivateFormat, *, _kdf_rounds=None, _hmac_hash=None, _key_cert_algorithm=None) -> None:
        self._format = format
        self._kdf_rounds = _kdf_rounds
        self._hmac_hash = _hmac_hash
        self._key_cert_algorithm = _key_cert_algorithm

    def kdf_rounds(self, rounds: int) -> KeySerializationEncryptionBuilder:
        if self._kdf_rounds is not None:
            raise ValueError("kdf_rounds already set")
      
```

### Convenience-function layer over session-based API
*3 occurrences across 3 projects: anyio, polars, requests*

Module-level functions (requests.get, requests.post, etc.) are thin wrappers that create a Session, call the corresponding method, and return the response. Each verb function accepts the same kwargs as Session.request() plus verb-specific defaults (e.g. head sets allow_redirects=False). The convenience layer eliminates boilerplate for one-off requests while the Session API handles persistent connections.

**Why**: Most HTTP requests are one-off — the user wants 'GET this URL' without managing session lifecycle. But the implementation must still use a Session (for connection pooling, default headers, cookie handling). The convenience functions bridge this: they create a Session in a with-block (ensuring cleanup), delegate, and return. This is the 'small interface, deep implementation' pattern — the top-level API is 8 one-liner functions, but each delegates to the full Session machinery.

```python
# anyio — src/anyio/_core/_tasks.py:131-149
@contextmanager
def fail_after(delay: float | None, shield: bool = False) -> Generator[CancelScope, None, None]:
    current_time = get_async_backend().current_time
    deadline = (current_time() + delay) if delay is not None else math.inf
    with get_async_backend().create_cancel_scope(deadline=deadline, shield=shield) as cancel_scope:
        yield cancel_scope
    if cancel_scope.cancelled_caught and current_time() >= cancel_scope.deadline:
        raise TimeoutError
```

### Virtual base class with __new__ dispatching to backend factory
*3 occurrences across 2 projects: anyio, tornado*

Base classes (Event, Lock, Semaphore, CapacityLimiter, CancelScope) define the interface with all methods raising NotImplementedError. __new__ calls get_async_backend().create_X() to return a backend-specific implementation. Callers never instantiate the base — they get a concrete backend subclass transparently. This is the factory method pattern realized through __new__, so the constructor itself is the dispatch point.

**Why**: Allows user code to write Event() without knowing or caring which async backend (asyncio, trio) is active. The base class serves as a typed interface (type hints, docstrings, __slots__) while never being instantiated. Backend selection happens at runtime via sniffio, and the appropriate concrete class is returned. This eliminates the need for users to import backend-specific classes. [Merged from P109: Without the adapter, constructing Event() outside an event loop would crash. The adapter provides graceful degradation: it captures intent (set/wait) and replays it once a backend is available. This is essential for module-level or class-level initialization patterns where the event loop hasn't started yet.]

```python
# anyio — src/anyio/_core/_synchronization.py:114-155
class EventAdapter(Event):
    __slots__ = "_internal_event", "_is_set"

    def __new__(cls) -> EventAdapter:
        return object.__new__(cls)

    def __init__(self) -> None:
        self._internal_event: Event | None = None
        self._is_set = False

    @property
    def _event(self) -> Event:
        if self._internal_event is None:
            self._internal_event = get_async_backend().create_event()
            if self._is_set:
                self._internal_event.set()
        retur
```

### Function impersonation for transparent framework integration
*3 occurrences across 2 projects: hypothesis, more-itertools*

impersonate(target) is a decorator that overwrites a wrapper function's __code__ (filename, firstlineno), __name__, __module__, __doc__ to match the target. This makes the wrapper invisible to introspection tools — pytest sees the original test function, not the hypothesis wrapper. proxies(target) combines impersonate + wraps + define_function_signature to create a proxy with the exact signature of the target.

**Why**: Testing frameworks (pytest, unittest) use function introspection for discovery, fixture resolution, and traceback presentation. If the @given wrapper doesn't look like the original function, these frameworks break. Impersonation is a pragmatic hack: lie about where the code comes from so that error messages point to the user's test, not hypothesis internals. A __hypothesistracebackhide__ breadcrumb is left for hypothesis' own introspection.

```python
# hypothesis — hypothesis/src/hypothesis/internal/reflection.py:500-540
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

def proxies(target: T) -> Callable[[Callable], T
```

---

## Module Organization (7 patterns)

### _internal/ convention for public vs internal
*26 occurrences across 20 projects: Pillow, anyio, attrs, beartype, celery, click, cryptography, flask, hypothesis, jsonschema, loguru, more-itertools, polars, pydantic, pytest, requests, starlette, textual, toolz, tornado*

Public modules: main.py, fields.py. Internal: _internal/*.py. __init__.py uses __all__ + lazy __getattr__ for deferred module loading.

```python
# attrs — src/attr/__init__.py:1-104
from . import converters, exceptions, filters, setters, validators
from ._funcs import asdict, assoc, astuple, has, resolve_types
from ._make import (NOTHING, Attribute, Converter, Factory, attrib, attrs, evolve, fields, ...)
from ._next_gen import define, field, frozen, mutable

__all__ = ["NOTHING", "Attribute", "AttrsInstance", "Converter", ...]

def _make_getattr(mod_name: str) -> Callable:
    def __getattr__(name: str) -> str:
        if name not in ("__version__", "__version_info__"):
   
```

### Pre-instantiated singleton module object
*7 occurrences across 7 projects: Pillow, beartype, cryptography, loguru, more-itertools, starlette, tornado*

A module exports a single pre-configured instance of its main class, created at import time with sensible defaults. Users import the instance directly rather than constructing their own. The class itself is still importable for advanced use, but the singleton is the primary entry point. Auto-initialization (e.g. adding a default stderr handler) happens at module load, controllable via environment variable.

**Why**: Eliminates boilerplate of logger = getLogger(); logger.setLevel(); logger.addHandler(). Users get a working logger with `from loguru import logger`. The singleton pattern works for logging because there is conceptually one global logging pipeline. This contrasts with structlog's factory pattern where each module creates its own bound logger. The trade-off: simpler for users, less flexible for multi-tenant scenarios.

```python
# tornado — tornado/options.py:684-700
options = OptionParser()

def define(name, default=None, type=None, help=None, metavar=None,
           multiple=False, group=None, callback=None):
    """Defines a new command line option."""
    return options.define(name, default=default, type=type, help=help, ...)

def parse_command_line(args=None, final=True):
    return options.parse_command_line(args, final=final)

def parse_config_file(path, final=True):
    return options.parse_config_file(path, final=final)
```

### Thin Python wrappers over compiled core
*6 occurrences across 4 projects: Pillow, cryptography, msgspec, polars*

Each protocol module is a thin re-export from _core. Python-visible API is just aliases. Actual logic in C extension.

**Why**: The Python layer provides discoverable import paths, __all__ for public API control, and ABC registration for type checking. The Rust layer provides performance and memory safety. This separation means the Python API documentation (docstrings, types) lives in Python, while the implementation lives in Rust — each language does what it's best at.

```python
# cryptography — src/cryptography/hazmat/primitives/ciphers/aead.py:1-18
from cryptography.hazmat.bindings._rust import openssl as rust_openssl

__all__ = ["AESCCM", "AESGCM", "AESGCMSIV", "AESOCB3", "AESSIV", "ChaCha20Poly1305"]

AESGCM = rust_openssl.aead.AESGCM
ChaCha20Poly1305 = rust_openssl.aead.ChaCha20Poly1305
AESCCM = rust_openssl.aead.AESCCM
AESSIV = rust_openssl.aead.AESSIV
AESOCB3 = rust_openssl.aead.AESOCB3
AESGCMSIV = rust_openssl.aead.AESGCMSIV
```

### Compatibility shim: version-conditional imports with __all__
*6 occurrences across 4 projects: Pillow, cryptography, more-itertools, toolz*

A compatibility.py module centralizes Python 2/3 differences. It uses runtime version checks to assign the correct implementations (e.g., imap vs map) and exports them via __all__. Other modules import from compatibility rather than using conditional imports scattered throughout.

**Why**: Centralizing version differences in one module means the rest of the codebase is version-agnostic. The __all__ list documents the compatibility surface. When Python 2 support is eventually dropped, only compatibility.py needs updating. This is the adapter pattern at the module level: one indirection layer absorbs environmental variation.

```python
# toolz — toolz/compatibility.py:1-26
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
els
```

### One visual element per module
*4 occurrences across 4 projects: pytest, rich, textual, toolz*

Each visual element is its own module. Small helpers get _ prefix: _loop.py, _pick.py, _stack.py. Private implementation details.

```python
# toolz — toolz/itertoolz.py:1-10
import itertools
import heapq
import collections
import operator
from functools import partial
from toolz.compatibility import (map, filter, filterfalse, zip, zip_longest,
                                 iteritems)

__all__ = ('remove', 'accumulate', 'groupby', 'merge_sorted', 'interleave',
           'unique', 'isiterable', 'isdistinct', 'take', 'drop', 'take_nth',
           'first', 'second', 'nth', 'last', 'get', 'concat', 'concatv',
           'mapcat', 'cons', 'interpose', 'frequencies', 
```

### suppress(ImportError) for optional dependency registration
*4 occurrences across 3 projects: cryptography, jsonschema, more-itertools*

Optional format checkers (rfc3987, fqdn, webcolors, etc.) are registered inside `with suppress(ImportError):` blocks. If the optional library is installed, the format checker function is defined and registered. If not, the block is silently skipped — the format is simply not checked. No error, no warning, graceful degradation.

**Why**: Format validation for specific formats (URI, hostname, color) requires third-party libraries that may not be installed. Making them hard dependencies would bloat the install. try/except ImportError at import time is the standard pattern, but `with suppress(ImportError):` is cleaner — it scopes the optional registration to a block, making it visually clear which functions are optional and which library they need.

```python
# jsonschema — jsonschema/_format.py:210-225
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

    @_chec
```

### Lazy backend loading with module-level cache
*3 occurrences across 2 projects: Pillow, anyio*

Backend classes are loaded on demand via import_module(f'anyio._backends._{name}') and cached in a module-level dict (loaded_backends). The backend module exposes a 'backend_class' attribute that the loader reads. This avoids importing trio when only asyncio is used.

**Why**: Importing trio unconditionally would add startup overhead and require trio as a hard dependency. By lazy-loading, anyio only imports the backend the user actually needs. The cache dict avoids repeated import_module calls. Using a custom dict instead of sys.modules handles partially-initialized modules safely.

```python
# Pillow — src/PIL/Image.py:415-440
def _import_plugin_for_extension(ext: str | bytes) -> bool:
    if not ext:
        return False
    if isinstance(ext, bytes):
        ext = ext.decode()
    ext = ext.lower()
    if ext in EXTENSION:
        return True
    plugin = _EXTENSION_PLUGIN.get(ext)
    if plugin is None:
        return False
    try:
        __import__(f"{__spec__.parent}.{plugin}", globals(), locals(), [])
        return True
    except ImportError as e:
        logger.debug("Image: failed to import %s: %s", plugin
```

---
