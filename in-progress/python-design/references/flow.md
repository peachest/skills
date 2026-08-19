## Pipeline Composition, Error Strategy, Sync/Async (17 patterns)

### Pipeline as named step chain
`P016` · 4 occurrences · 4 projects: celery, scikit-learn, polars, setuptools

**What**: A pipeline is an ordered list of `(name, estimator)` pairs; data flows through each step's `fit_transform`, and steps are addressable via `name__param` dotted syntax.

**Recognize**:
- Constructor takes a list of `(str, object)` tuples, e.g. `Pipeline([('scaler', StandardScaler()), ('svc', SVC())])`
- Steps expose parameters via `name__param` dotted access (`grid['svc__C']`)
- `__or__` overloaded to build chains declaratively (`add.s(2, 2) | add.s(4) | add.s(8)`)

**Why**: Naming steps gives stable handles for tuning, inspection, and serialization — `grid['svc__C']` reaches a specific stage without positional guesswork. The uniform step interface means any compatible transformer/estimator plugs in. Trade-off: the indirection adds a layer between caller and step, and the `name__param` scheme is a convention that can collide if two steps share a name.

**When**: Use when composing multi-stage data-processing or task graphs where each stage is independently configurable, inspectable, and replaceable.

**When not**: For a fixed single transformation, a plain function call is simpler; for branching/fan-out DAGs, use a graph executor rather than a linear named chain (see P017 Processor chain for linear-only cases).

**Without this pattern** (anti-pattern):
```python
def train(data):
    scaled = StandardScaler().fit_transform(data)   # ❌ can't tune/inspect/replace stages;
    model = SVC().fit(scaled)                        #   no stable handle to reach 'C'
    return model
```

**With this pattern**:
```python
# ✅ Good: the pattern applied
# scikit-learn — sklearn/pipeline.py
Pipeline([('scaler', StandardScaler()), ('svm', SVC())])

# celery — celery/canvas.py:758-785  (declarative __or__ chaining)
def __or__(self, other):
    """Chaining operator.
    >>> add.s(2, 2) | add.s(4) | add.s(8)
    """
    if isinstance(other, Signature):
        return _chain(self, other, app=self._app)
    return NotImplemented
```

### Processor chain: (logger, method_name, event_dict) → event_dict
`P017` · 6 occurrences · 5 projects: attrs, celery, structlog, toolz, jinja2

**What**: Each processor takes a dict and returns a (possibly modified) dict; the chain is a linear list of callables, with terminal processors returning str/bytes.

**Recognize**:
- A list of callables passed as `processors=[...]`, applied left-to-right
- Each non-terminal callable has signature `(value) -> value` (dict in, dict out)
- The last processor in the chain changes the return type (dict → str/bytes)

**Why**: A uniform `(dict) -> dict` contract makes processors trivially composable, reorderable, and testable in isolation — you can drop a new processor into the list without touching its neighbors. Trade-off: every processor must agree on the dict shape (a shared, implicit schema), and there is no static type checking of the flowing dict, so a typo'd key silently propagates to the end of the chain.

**When**: Use for transformation pipelines (logging, rendering, data shaping) where stages are independently swappable and the intermediate representation is a flexible dict.

**When not**: When stages have heterogeneous in/out types that a typed pipeline (see P016 Pipeline as named step chain) or a class-based stage hierarchy would express more safely.

**Without this pattern** (anti-pattern):
```python
def format_log(event):
    event["timestamp"] = now()           # ❌ monolithic: can't reorder/swap/extend stages
    event["level"] = event.pop("lvl")    #   without editing this whole function
    return json.dumps(event)
```

**With this pattern**:
```python
# ✅ Good: the pattern applied
# structlog — structlog/_config.py
processors = [add_log_level, TimeStamper(fmt='iso'), JSONRenderer()]
# dict flows: add_log_level → TimeStamper → JSONRenderer (dict → str)

# attrs — src/attr/setters.py:15-29  (same shape for attribute setters)
def pipe(*setters):
    def wrapped_pipe(instance, attrib, new_value):
        rv = new_value
        for setter in setters:
            rv = setter(instance, attrib, rv)
        return rv
    return wrapped_pipe
```

### IO manager: two-method serialization boundary
`P019` · 3 occurrences · 3 projects: celery, flask, dagster

**What**: The entire IO contract is two methods — `load_input(context)` (read) and `handle_output(context, obj)` (write); the IO manager never touches the compute function.

**Recognize**:
- A class defining exactly `load_input(context)` and `handle_output(context, obj)`, nothing else on the data path
- Symmetric `open_session`/`save_session` (or `load`/`store`) pairs with matching read/write signatures
- Compute functions are pure of IO; the manager is injected, not called inline

**Why**: Isolating IO behind two methods makes compute testable (inject a fake manager) and IO swappable (swap filesystem for S3 without touching compute logic). Trade-off: every IO variant must implement both methods even if it only reads or only writes, and the indirection hides where data physically moves.

**When**: Use in orchestration/ETL frameworks where the same compute should run against multiple storage backends.

**When not**: For one-off scripts with a single, known storage location, a direct read/write is simpler — the abstraction buys nothing.

**Without this pattern** (anti-pattern):
```python
def process(path):
    data = open(path).read()            # ❌ IO glued to compute; can't test without a file,
    result = transform(data)            #   can't swap storage backend
    open(path + ".out", "w").write(result)
```

**With this pattern**:
```python
# ✅ Good: the pattern applied
# dagster — dagster/_core/storage/io_manager.py:155-178
class IOManager:
    def load_input(self, context):
        ...
    def handle_output(self, context, obj):
        ...

# flask — src/flask/sessions.py:97-120  (SessionInterface: open_session / save_session)
class SessionInterface:
    def open_session(self, app: Flask, request: Request) -> SessionMixin | None:
        raise NotImplementedError()
    def save_session(self, app: Flask, session: SessionMixin, response: Response) -> None:
        raise NotImplementedError()
```

### Code generation via string templating + eval
`P040` · 5 occurrences · 4 projects: attrs, werkzeug, jinja2, beartype

**What**: Methods are generated by building Python source as strings, `compile()`-ing, and `exec()`-ing into a namespace at class-definition time, producing real function objects (correct `__qualname__`, `__doc__`, stack traces) rather than lambdas or wrappers.

**Recognize**:
- `compile(source_string, filename, 'exec')` followed by `exec(...)` into a locals dict
- A custom fake `<filename>` registered with `linecache` so debuggers show the generated source
- Generated method bodies built via f-strings / `lines.append(...)` then compiled once at definition time

**Why**: Hot-path methods (`__init__`, `__eq__`, `__repr__`, type-check wrappers) need direct bytecode (`self.x = value`) with zero dispatch overhead — string generation bakes the logic in at definition time, O(1) per call with no `getattr`/`setattr` loops or runtime dispatch. `linecache` registration closes the gap between generated and hand-written code so PDB can step through it. Trade-off: generated code is harder to read and modify than hand-written code, and bugs in the generator produce confusing errors at import time.

**When**: Use when generating per-class methods (`__init__`, validators, type checkers) that sit on every hot path and must be as fast as hand-written code.

**When not**: For one-off or rarely-called code, closures or descriptors are simpler and avoid the readability/maintainability cost of string-templated source.

**Without this pattern** (anti-pattern):
```python
def make_init(fields):
    def __init__(self, *args):              # ❌ generic setattr loop: slow on every call,
        for name, val in zip(fields, args): #   no real __qualname__, no debugger source
            setattr(self, name, val)
    return __init__
```

**With this pattern**:
```python
# ✅ Good: the pattern applied
# beartype — beartype/_util/func/utilfuncmake.py:60-120
def make_func(func_name, func_code, func_globals=None, func_locals=None, **kwargs):
    func_filename = f'<@beartype({func_filename_name}) at {id(func_filename_object):#x}>'
    func_code = func_code.strip()
    func_code_compiled = compile(func_code, func_filename, 'exec')
    exec(func_code_compiled, func_globals, func_locals)
    func = func_locals[func_name]
    if func_wrapped is not None:
        update_wrapper(wrapper=func, wrapped=func_wrapped)
    return func

# attrs — src/attr/_make.py:221-260  (linecache registration for debuggability)
#   lines = ["self.__attrs_pre_init__()"]
#   lines.append(f"self.{attr_name} = {value}")   # direct attribute access in generated bytecode
```

### on_setattr hook pipe for post-construction attribute mutation
`P046` · 3 occurrences · 2 projects: attrs, textual

**What**: After construction, attribute assignment triggers a composable pipeline of hooks (`convert → validate`) via `setters.pipe()`; each hook receives `(instance, attribute, new_value)` and returns the (possibly transformed) value, with a `NO_OP` sentinel disabling hooks per-attribute.

**Recognize**:
- An `on_setattr=` argument accepting a list of callables, auto-wrapped into `pipe(*setters)`
- Setter signature `(instance, attrib, value) -> value`; a `NO_OP` sentinel skips a field
- `__setattr__` overridden (or a descriptor `__set__`) to route assignment through the pipe

**Why**: Construction-time validation is common, but post-construction mutation (`obj.x = v`) usually bypasses validators/converter. The on_setattr pipe extends the same pipeline to every assignment, and `pipe` composition fixes ordering (convert before validate) while `NO_OP` gives per-field escape hatches without disabling the class-wide policy. Trade-off: every assignment pays the hook-dispatch cost, and a misconfigured pipe silently transforms values.

**When**: Use for value objects that must stay valid after mutation (attrs validate-on-setattr, reactive properties).

**When not**: For write-once or fully frozen objects, validation at construction is enough (see CONTEXT: Frozen + slots value object, P003) — runtime hooks add overhead with no benefit.

**Without this pattern** (anti-pattern):
```python
@attr.s
class User:
    email = attr.ib(validator=is_email)

u = User("x@y.com")
u.email = "not-an-email"   # ❌ validator bypassed on mutation; object now invalid
```

**With this pattern**:
```python
# ✅ Good: the pattern applied
# attrs — src/attr/setters.py:1-79
def pipe(*setters):
    def wrapped_pipe(instance, attrib, new_value):
        rv = new_value
        for setter in setters:
            rv = setter(instance, attrib, rv)
        return rv
    return wrapped_pipe

def validate(instance, attrib, new_value):
    v = attrib.validator
    if not v:
        return new_value
    v(instance, attrib, new_value)
    return new_value

def convert(instance, attrib, new_value):
    c = attrib.converter
    return c(new_value) if c else new_value

NO_OP = object()  # sentinel for per-attribute disable
# usage: @attr.s(on_setattr=[convert, validate])
```

### Stack-based resource lifecycle with finalizers
`P085` · 3 occurrences · 3 projects: click, aiohttp, pytest

**What**: A `SetupState` maintains a stack of `(node, finalizers)` pairs; `setup(item)` walks the collector chain root→item pushing nodes and running their `setup()`, while teardown pops nodes in reverse and runs their finalizers — so shared scoped resources are set up once and torn down only when the last item using them finishes.

**Recognize**:
- A dict/stack keyed by node, holding a list of finalizer callables per node
- `setup()` pushes outward-to-inward; teardown pops inward-to-outward (`reversed`)
- `addfinalizer()` registers teardown callbacks dynamically during setup; an `ExitStack` accumulates them

**Why**: Fixture scopes (function/class/module/session) create nested lifecycles: a session fixture must outlive module fixtures, which must outlive function fixtures. A stack naturally models this nesting, and the next-item parameter lets shared resources persist across items — only popping nodes the next item doesn't also need. Trade-off: the stack must stay consistent under partial failures (one broken finalizer shouldn't skip the rest), adding error-collection complexity.

**When**: Use in test runners and request/response lifecycles where resources have nested scopes and must tear down in reverse order of setup.

**When not**: For flat (non-nested) resource lifecycles, a single `try/finally` or `contextlib.ExitStack` is sufficient — the node-chain bookkeeping is unnecessary.

**Without this pattern** (anti-pattern):
```python
def run_test(test):
    db = setup_db()                  # ❌ flat: no nesting, no shared scope;
    try:                             #   session-scoped db re-created for every test
        test(db)
    finally:
        teardown_db(db)
```

**With this pattern**:
```python
# ✅ Good: the pattern applied
# pytest — src/_pytest/runner.py:402-482
class SetupState:
    def __init__(self) -> None:
        self.stack: Dict[Node, Tuple[List[Callable[[], object]], Optional[Exception]]] = {}

    def setup(self, item: Item) -> None:
        needed_collectors = item.listchain()
        for col in needed_collectors[len(self.stack):]:
            self.stack[col] = ([col.setup], None)
            ...

    def teardown_exact(self, nextitem: Optional[Item]) -> None:
        needed_collectors = nextitem.listchain() if nextitem is not None else []
        for node in reversed(list(self.stack)):
            if node in needed_collectors:
                break
            finalizers, _ = self.stack.pop(node)
            for fin in reversed(finalizers):
                fin()

# aiohttp — aiohttp/web_app.py:584-610  (CleanupContext: __aenter__ on setup, reversed __aexit__ on teardown)
```

### Prepare/send two-phase request lifecycle
`P097` · 4 occurrences · 4 projects: werkzeug, requests, cryptography, starlette

**What**: A user-facing `Request` container with optional fields is separated from a `PreparedRequest` internal representation with fully resolved URL, encoded body, and merged headers; `prepare()` runs a multi-step pipeline (`prepare_method → prepare_url → prepare_headers → prepare_cookies → prepare_body → prepare_auth → prepare_hooks`) that transforms the former into the latter.

**Recognize**:
- Two classes: a user-friendly `Request` (optional, loosely-typed fields) and a `PreparedRequest` (resolved, wire-ready)
- A `prepare()` method calling a sequence of `prepare_*` sub-steps in a fixed order
- Auth preparation explicitly ordered last (it may sign the already-prepared body)

**Why**: Users think in terms of "GET this URL with these params and this auth", but the wire needs a resolved URL string, encoded body bytes, and merged headers. Splitting the two phases lets a `Session` merge its own defaults (headers, cookies, auth) with per-request overrides during preparation, and makes each transformation step individually testable. Trade-off: two classes plus a multi-step prepare method add indirection versus a single `send(method, url, **kwargs)` call.

**When**: Use for HTTP/protocol clients where session-level defaults must merge with per-request settings and the wire format differs from the user-facing API.

**When not**: For a single-shot request with no shared session state, a direct `request(method, url, **kwargs)` is simpler — the prepare/PreparedRequest split buys nothing.

**Without this pattern** (anti-pattern):
```python
def get(url, headers=None, auth=None):     # ❌ no separation; session defaults can't merge,
    h = headers or {}                       #   auth can't sign the encoded body
    h["Authorization"] = auth
    return send("GET", url, headers=h, body=encode(data))
```

**With this pattern**:
```python
# ✅ Good: the pattern applied
# requests — src/requests/models.py:440-460
class PreparedRequest(RequestEncodingMixin, RequestHooksMixin):
    def prepare(self, method=None, url=None, headers=None, files=None,
                data=None, params=None, auth=None, cookies=None,
                hooks=None, json=None) -> None:
        self.prepare_method(method)
        self.prepare_url(url, params)
        self.prepare_headers(headers)
        self.prepare_cookies(cookies)
        self.prepare_body(data, files, json)
        self.prepare_auth(auth, url)
        # This MUST go after prepare_auth
        self.prepare_hooks(hooks)
```

### Iterator-first design: everything lazy, materialize on demand
`P188` · 7 occurrences · 5 projects: setuptools, toolz, more-itertools, jinja2, polars

**What**: All sequence functions return generators/iterators, never lists; the caller materializes with `list()`/`tuple()` or iterates directly, so functions compose without intermediate materialization.

**Recognize**:
- Sequence utilities implemented with `yield` or returning `itertools` constructs (`chain.from_iterable`, `islice`, `filterfalse`)
- Functions return iterators even when a list would be "easier"; materialization is the caller's job
- A `.lazy()` entry point that defers execution (e.g. `LazyFrame`) until an explicit collect

**Why**: Lazy evaluation enables infinite sequences and large datasets without memory pressure — `pipe(data, map(f), filter(g), unique)` processes each element through the full chain before the next is read. Trade-off: iterators are single-use (re-iteration needs re-creation), errors surface only at consumption time, and debugging is harder with no intermediate list to inspect.

**When**: Use for functional/sequence libraries and query engines where chains compose and datasets may be large or infinite.

**When not**: When callers always need the full materialized result and never benefit from laziness, returning a list is simpler and avoids single-use-iterator footguns.

**Without this pattern** (anti-pattern):
```python
def unique(seq):
    seen = []
    result = []          # ❌ eager: materializes everything, breaks on infinite input,
    for x in seq:        #   forces a full pass before the caller sees any element
        if x not in seen:
            seen.append(x)
            result.append(x)
    return result
```

**With this pattern**:
```python
# ✅ Good: the pattern applied
# toolz — toolz/itertoolz.py:15-35
def remove(predicate, seq):
    return filterfalse(predicate, seq)

def accumulate(binop, seq):
    seq = iter(seq)
    result = next(seq)
    yield result
    for elem in seq:
        result = binop(result, elem)
        yield result

def concat(seqs):
    return itertools.chain.from_iterable(seqs)

# polars — py-polars/.../frame.py:10412-10447  (defer to LazyFrame until collect)
def lazy(self) -> LazyFrame:
    """Start a lazy query from this point."""
    return wrap_ldf(self._df.lazy())
```

### Middleware as onion wrapping via reversed accumulation
`P370` · 3 occurrences · 3 projects: aiohttp, uvicorn, starlette

**What**: A middleware stack is built by wrapping inside-out: iterate `reversed(middleware)`, each middleware takes the current app and returns a wrapped app — the last middleware wraps the router (innermost), the first wraps everything (outermost), so the outermost sees the request first.

**Recognize**:
- `for cls, args, kwargs in reversed(middleware): app = cls(app, ...)` accumulation loop
- Each middleware signature `(app, ...) -> app` (wraps the next layer)
- The innermost app is the router; the outermost is returned as the final handler

**Why**: Reversed accumulation produces the natural request-processing order (outermost first, innermost last) with a simple fold — no explicit "before/after" hooks are needed, because wrapping handles both phases. Trade-off: the full call passes through every layer even for trivial requests, and debugging requires understanding the nested wrapper chain (stack traces get deep).

**When**: Use for HTTP/ASGI/WSGI frameworks and any layered request-processing pipeline where each layer wraps the next.

**When not**: For a single cross-cutting concern (one logger, one auth check), a decorator or plain wrapper function is simpler than building a full middleware stack.

**Without this pattern** (anti-pattern):
```python
def app(request):
    log(request)                       # ❌ hardcoded order; can't reorder/insert/remove layers
    if not authed(request):            #   without editing this function
        return 401
    return route(request)
```

**With this pattern**:
```python
# ✅ Good: the pattern applied
# starlette — starlette/applications.py:66-75
def build_middleware_stack(self) -> ASGIApp:
    middleware = [Middleware(ServerErrorMiddleware, handler=error_handler, debug=debug)]
    middleware += self.user_middleware
    middleware.append(Middleware(ExceptionMiddleware, handlers=exception_handlers, debug=debug))

    app = self.router
    for cls, args, kwargs in reversed(middleware):
        app = cls(app, *args, **kwargs)
    return app

# aiohttp — aiohttp/web_app.py:74-79
def _build_middlewares(handler, apps):
    for app in apps[::-1]:
        for m, _ in app._middlewares_handlers:
            handler = update_wrapper(partial(m, handler=handler), handler)
    return handler
```

### ValidationError aggregates multiple field errors
`P012` · 8 occurrences · 8 projects: attrs, celery, pydantic, hypothesis, setuptools, pytest, click, jsonschema

**What**: A validation error object holds a list of per-field errors (location, type, message), so a single validation pass surfaces every problem at once instead of stopping at the first.

**Recognize**:
- An exception class with an `.errors()` method returning a list of dicts with `loc`/`type`/`msg` keys
- The validation loop collects errors into a container rather than raising per-field
- A single `ValidationError` is raised at the end carrying the full error list

**Why**: Fail-fast on validation forces users into a fix-one-rerun-fix-next loop. Collecting all errors in one pass lets users fix every issue before resubmitting. Trade-off: the validator must run to completion even after finding errors (slightly more work, and it can't early-exit), and the error object is heavier than a single message string.

**When**: Use for user-facing input validation (forms, configs, schemas) where users benefit from seeing all problems at once.

**When not**: For internal invariants or programming errors where the first failure indicates corruption, prefer a single fail-fast exception (see P096 Exception hierarchy with context-carrying base).

**Without this pattern** (anti-pattern):
```python
def validate(data):
    if "email" not in data:
        raise ValueError("missing email")      # ❌ stops here, hides the password error
    if "password" not in data:
        raise ValueError("missing password")   # never reached
```

**With this pattern**:
```python
# ✅ Good: the pattern applied
# pydantic — pydantic/errors.py
try:
    Model(**data)
except ValidationError as e:
    for err in e.errors():
        print(err["loc"], err["msg"])   # surfaces BOTH missing fields at once

# attrs — src/attr/exceptions.py:1-95  (hierarchy of context-carrying validation errors)
class NotAnAttrsClassError(ValueError): ...
class DefaultAlreadySetError(RuntimeError): ...
class NotCallableError(TypeError):
    def __init__(self, msg, value):
        super(TypeError, self).__init__(msg, value)
        self.msg = msg
        self.value = value
```

### Result object for error isolation
`P014` · 7 occurrences · 7 projects: attrs, pytest, textual, requests, pluggy, toolz, more-itertools

**What**: A call's outcome (return value or exception) is captured in a Result object; callers retrieve it via `get_result()` (re-raise) or `force_result()` (suppress/replace), separating "an exception happened" from "what to do about it".

**Recognize**:
- A class with `from_call(func, ...)` that wraps a callable, storing either the value or an `ExceptionInfo`
- `get_result()` re-raises the captured exception; `force_result(value)` overrides it
- Result carries timing metadata (start/stop/duration) alongside the outcome

**Why**: Separating "an exception happened" from "what to do about it" lets middleware (hooks, test runners) observe failures without committing to re-raising — one caller re-raises, another collects-and-continues, a third substitutes a default. Trade-off: every call pays the cost of building a Result object and storing the exception, and the call site must explicitly call `get_result()` to surface errors (easy to forget).

**When**: Use in plugin/hook systems, test runners, and dispatch chains where multiple observers must see both success and failure outcomes.

**When not**: For straightforward "do it or fail" call sites, a direct function call with a try/except is simpler — the Result indirection adds ceremony with no benefit.

**Without this pattern** (anti-pattern):
```python
def run_hook(hook, *args):
    return hook(*args)        # ❌ exception propagates immediately; no chance to observe,
                              #   collect, or substitute before the caller sees it
```

**With this pattern**:
```python
# ✅ Good: the pattern applied
# pytest — src/_pytest/runner.py:269-365
@final
@dataclasses.dataclass
class CallInfo(Generic[TResult]):
    _result: Optional[TResult]
    excinfo: Optional[ExceptionInfo[BaseException]]
    start: float
    stop: float
    duration: float
    when: "Literal['collect', 'setup', 'call', 'teardown']"

    @classmethod
    def from_call(cls, func, when, reraise=None):
        excinfo = None
        start = timing.time()
        try:
            result = func()
        except BaseException:
            excinfo = ExceptionInfo.from_current()
            if reraise is not None and isinstance(excinfo.value, reraise):
                raise
            result = None
        duration = timing.perf_counter() - precise_start
        return cls(start=start, stop=stop, duration=duration, when=when,
                   result=result, excinfo=excinfo, _ispytest=True)

# pluggy — pluggy/_result.py
#   outcome = Result.from_call(lambda: hook_impl.function(*args))
#   outcome.get_result()   # re-raises captured exception (or force_result() to suppress)
```

### Error handler lookup by MRO + scope cascade
`P071` · 5 occurrences · 2 projects: flask, starlette

**What**: Error handlers are registered in a nested dict `{scope: {code: {exception_class: handler}}}`; lookup walks the exception's MRO to find the most specific handler, cascading through blueprint scope → app scope and HTTP code → generic.

**Recognize**:
- `error_handler_spec` / `_exception_handlers` dict keyed by exception class (and/or status code)
- Lookup loop `for cls in type(exc).__mro__:` returning the first registered handler
- Dual registries: status-code handlers AND exception-type handlers in the same system

**Why**: One registration system handles both HTTP status codes (404, 500) and arbitrary exception types (DatabaseError). The MRO walk means registering a handler for a base class catches all subclasses automatically; the scope cascade lets modules (blueprints) handle their own errors without affecting the rest of the app. Trade-off: the lookup is O(MRO depth × scopes) per error, and the nested-dict structure is non-obvious to new contributors.

**When**: Use in web frameworks / plugin systems where errors must map to handlers at multiple granularities (per-route, per-app, per-status, per-exception-type).

**When not**: For a single global error policy, a flat `except SpecificError` chain is simpler — the MRO/scope machinery is overkill.

**Without this pattern** (anti-pattern):
```python
def handle_error(e):                 # ❌ hardcoded chain; can't scope or subclass-match,
    if isinstance(e, NotFound):      #   every new error type requires editing this function
        return not_found_page()
    elif isinstance(e, DatabaseError):
        return server_error_page()
    raise e
```

**With this pattern**:
```python
# ✅ Good: the pattern applied
# flask — src/flask/sansio/app.py:823-860
def _find_error_handler(self, e: Exception, blueprints: list[str]):
    exc_class, code = self._get_exc_class_and_code(type(e))
    names = (*blueprints, None)  # blueprint scope → app scope

    for c in (code, None) if code is not None else (None,):
        for name in names:
            handler_map = self.error_handler_spec[name][c]
            if not handler_map:
                continue
            for cls in exc_class.__mro__:  # most specific first
                handler = handler_map.get(cls)
                if handler is not None:
                    return handler
    return None

# starlette — starlette/_exception_handler.py:12-16
def _lookup_exception_handler(exc_handlers, exc):
    for cls in type(exc).__mro__:
        if cls in exc_handlers:
            return exc_handlers[cls]
    return None
```

### Exception hierarchy with context-carrying base
`P096` · 23 occurrences · 17 projects: cryptography, beartype, Pillow, hypothesis, tornado, setuptools, jinja2, aiohttp, click, textual, requests, sqlalchemy, starlette, anyio, jsonschema, werkzeug, polars

**What**: A base exception class carries domain context (request, response, config) via kwargs in `__init__`, and a tree of specialized subclasses inherit and extend that context — so catching the base catches all errors of that category while catching a leaf catches only that specific failure, with multiple inheritance creating category overlaps.

**Recognize**:
- A base exception whose `__init__` pops domain objects from kwargs (`response`, `request`, `ctx`) and stores them as attributes
- Specialized subclasses that add their own context layer (e.g. `BadParameter` adds `param`, `param_hint`)
- Multiple-inheritance leaves like `ConnectTimeout(ConnectionError, Timeout)` mirroring domain overlap

**Why**: HTTP/CLI errors have rich context (which request, which parameter) that plain messages lose; carrying it on the exception lets catchers inspect without parsing strings. The multiple-inheritance tree (`ConnectTimeout ⊂ ConnectionError ∩ Timeout`) mirrors the domain so a connect-timeout is catchable as either category. Trade-off: the hierarchy must be designed up front, and deep trees can confuse catchers who must understand the MRO to predict what a broad `except` catches.

**When**: Use for domain error families (HTTP, CLI, task) where callers need both broad "catch all X errors" and narrow "catch only this specific failure" handling, plus attached context.

**When not**: For a flat set of unrelated errors, a simple exception per case is clearer; for aggregating multiple errors at once, use P012 (ValidationError aggregates multiple field errors).

**Without this pattern** (anti-pattern):
```python
def connect(url):
    if timeout:                                      # ❌ bare Exception: no context attached,
        raise Exception(f"timeout connecting to {url}")  #   uncatchable by type, message-only
# caller can't distinguish timeout from auth failure without string parsing
```

**With this pattern**:
```python
# ✅ Good: the pattern applied
# requests — src/requests/exceptions.py:17-36
class RequestException(IOError):
    response: Response | None
    request: Request | PreparedRequest | None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        response: Response | None = kwargs.pop("response", None)
        self.response = response
        self.request = kwargs.pop("request", None)
        if response is not None and not self.request and hasattr(response, "request"):
            self.request = response.request
        super().__init__(*args, **kwargs)

class ConnectTimeout(ConnectionError, Timeout):
    """Safe to retry — both a connection error and a timeout."""

# click — src/click/exceptions.py:39-100  (each level adds context in format_message)
class UsageError(ClickException):
    exit_code: t.ClassVar[int] = 2
    ctx: Context | None
```

### Exception as exit signal with exit_code class attribute
`P133` · 6 occurrences · 5 projects: setuptools, tornado, textual, click, starlette

**What**: `ClickException` carries an `exit_code` class attribute (default 1, `UsageError`=2); `Exit` is a `RuntimeError` with `__slots__=('exit_code',)` signalling the app should stop — the `main()` loop catches these, calls `show()` for user output, then `sys.exit(e.exit_code)`, replacing `sys.exit()` calls inside command logic with exception-based control flow.

**Recognize**:
- An exception class with `exit_code: ClassVar[int]` (or `__slots__ = ("exit_code",)`)
- A top-level `main()` that catches the exception, renders user output, then `sys.exit(e.exit_code)`
- A distinct `Exit`/`Finish` exception used to short-circuit request handling without producing an error response

**Why**: Commands deep in the call chain need to signal "stop with this code" without knowing if they run standalone or nested. Exceptions bubble naturally through the call stack, and the per-class `exit_code` maps error types to codes (usage=2, general=1) without the caller interpreting the type. Trade-off: using exceptions for normal control flow can mask real bugs (a stray `Exit` is easy to miss), and the exit-code-as-class-attribute convention must be learned.

**When**: Use in CLI frameworks and request handlers where nested code must signal termination with a specific code without unwinding the stack manually.

**When not**: For libraries (non-CLI), prefer returning error objects (see P014 Result object) or raising domain exceptions (see P096) — `sys.exit` and exit codes are a CLI concern, not a library one.

**Without this pattern** (anti-pattern):
```python
def cmd(args):
    if not args:
        print("usage: cmd <name>")
        sys.exit(2)                # ❌ exit buried in logic; can't be caught/tested/reused
    return process(args[0])
```

**With this pattern**:
```python
# ✅ Good: the pattern applied
# click — src/click/exceptions.py:31-50, 344-354
class ClickException(Exception):
    exit_code: t.ClassVar[int] = 1

    def show(self, file=None) -> None:
        echo(_("Error: {message}").format(message=self.format_message()), file=file, color=self.show_color)

class UsageError(ClickException):
    exit_code: t.ClassVar[int] = 2

class Exit(RuntimeError):
    __slots__ = ("exit_code",)
    exit_code: t.Final[int]
    def __init__(self, code: int = 0):
        self.exit_code = code

# main() loop: catch ClickException → show() → sys.exit(e.exit_code)

# tornado — tornado/web.py:2606-2640  (Finish: end request without error response)
class Finish(Exception):
    """An exception that ends the request without producing an error response."""
```

### Exception-to-warning degradation for robust batch processing
`P210` · 5 occurrences · 4 projects: beartype, setuptools, cryptography, more-itertools

**What**: A decorator factory accepts a `warning_cls_on_decorator_exception` config; when set, decoration failures are caught and converted to warnings (the original object returned unmodified) instead of raising — so one undecorable item doesn't crash an entire batch or import.

**Recognize**:
- A `try/except Exception` around decoration with a `warnings.warn(...)` in the handler, returning the original object
- A configurable `warning_cls_on_decorator_exception` (or similar) toggle between fail-fast and degrade
- Used by import hooks / batch processors that walk entire packages

**Why**: Import hooks (e.g. `beartype.claw`) auto-decorate every function in a package; real packages have functions that can't be decorated (C extensions, exotic signatures). Fail-fast would make such hooks useless — one bad function kills the entire import. Warning degradation type-checks what it can and warns about the rest. Trade-off: silently-degraded items lose the pattern's guarantees, and warnings are easy to overlook; users must actively check for them.

**When**: Use for batch/automatic processing (import hooks, mass-decoration, lint passes) where partial success is better than total failure.

**When not**: When decoration failures indicate a real bug the user must fix, fail-fast raising (no degradation) is correct — warnings would hide the problem.

**Without this pattern** (anti-pattern):
```python
def decorate_all(module):
    for name, obj in vars(module).items():       # ❌ one undecorable callable raises and
        if callable(obj):                         #   kills the entire import
            obj = typecheck(obj)
        setattr(module, name, obj)
```

**With this pattern**:
```python
# ✅ Good: the pattern applied
# beartype — beartype/_decor/decorcore.py:75-130,201-270
def _beartype_object_nonfatal(obj, conf, **kwargs):
    try:
        return _beartype_object_fatal(obj, conf=conf, **kwargs)
    except Exception:
        warning_message = (
            f'{prefix} not decoratable by @beartype, as:\n    {format_exc()}'
        )
        issue_warning(cls=warning_category, message=warning_message)
    return obj  # return unmodified

# more-itertools — more_itertools/more.py:3728-3745  (filter_except: skip items that raise)
def filter_except(validator, iterable, *exceptions):
    for item in iterable:
        try:
            validator(item)
        except exceptions:
            pass
        else:
            yield item
```

### Duplication over abstraction for sync/async
`P038` · 5 occurrences · 5 projects: celery, tornado, httpx, textual, sqlalchemy

**What**: Parallel sync and async APIs are maintained as separate (near-duplicate) classes rather than generated or unified, accepting ~400 lines of duplication for readability and debuggability.

**Recognize**:
- Two sibling classes `Client` and `AsyncClient` (or `*Sync`/`*Async` mixins) with mirrored method sets
- Sync methods use blocking calls; async counterparts are `async def` with `await`
- No shared metaclass or code generator producing one from the other

**Why**: Generated or unified sync-async code is hard to step through, hard to grep, and obscures the control flow. Hand-maintained duplicates are readable and debuggable, and each can be optimized independently. Trade-off: every API change must be made twice, and the two classes can drift out of sync.

**When**: Use for libraries offering both sync and async first-class APIs (HTTP clients, ORMs) where the API surface is stable and debuggability matters.

**When not**: When the sync version is a thin shim over async (or vice versa), prefer a single bridge (see P077 ensure_sync: sync/async transparent bridge) to avoid maintaining two copies.

**Without this pattern** (anti-pattern):
```python
async def request(url):              # ❌ only async; sync callers forced into an event loop
    return await client.get(url)

def request_sync(url):
    loop = asyncio.new_event_loop()  # awkward, error-prone re-entry
    return loop.run_until_complete(request(url))
```

**With this pattern**:
```python
# ✅ Good: the pattern applied
# httpx — httpx/_client.py
class Client(BaseClient):
    ...          # blocking, hand-written
class AsyncClient(BaseClient):
    ...          # async, hand-written (parallel, not generated)

# celery — celery/backends/base.py + asynchronous.py  (SyncBackendMixin / AsyncBackendMixin)
class SyncBackendMixin:
    def wait_for_pending(self, result, **kwargs): ...   # blocking poll

class AsyncBackendMixin:
    def iter_native(self, result, **kwargs): ...        # non-blocking, event-driven
```

### ensure_sync: sync/async transparent bridge
`P077` · 4 occurrences · 3 projects: anyio, flask, starlette

**What**: `app.ensure_sync(func)` returns `func` as-is if it's a plain `def`, or wraps it with `async_to_sync` if it's `async def`; every call site invoking user-provided callbacks routes through this single method, so overriding it changes how async code is run app-wide.

**Recognize**:
- A method `ensure_sync(self, func)` containing `if iscoroutinefunction(func): return self.async_to_sync(func)` else `return func`
- Every user-callback invocation site wrapped: `self.ensure_sync(callback)(...)`
- A single override point to swap the async runtime (e.g. gevent for asyncio)

**Why**: Flask supports sync and async views transparently without duplicating the request pipeline (unlike P038's parallel classes). The overhead is one `iscoroutinefunction()` check per call, and overriding `ensure_sync` swaps the async runtime. Trade-off: the sync-wrapping path runs an event loop under the hood, which has overhead and reentrancy caveats versus a native sync implementation.

**When**: Use when a framework must accept both sync and async user callbacks through one pipeline without maintaining duplicate code paths.

**When not**: When the library is async-first and sync is a rarely-used shim, or when performance-critical paths can't afford the per-call coroutine check — prefer dedicated parallel APIs (see P038).

**Without this pattern** (anti-pattern):
```python
def call_view(view, **kwargs):
    if iscoroutinefunction(view):              # ❌ check scattered at every call site;
        result = asyncio.get_event_loop().run_until_complete(view(**kwargs))  # duplicated in
    else:                                      #   before_request, after_request, teardown...
        result = view(**kwargs)
    return result
```

**With this pattern**:
```python
# ✅ Good: the pattern applied
# flask — src/flask/app.py:966-985
def ensure_sync(self, func: t.Callable[..., t.Any]) -> t.Callable[..., t.Any]:
    if iscoroutinefunction(func):
        return self.async_to_sync(func)
    return func

# Every call site routes through one method:
#   self.ensure_sync(before_func)()
#   self.ensure_sync(self.view_functions[rule.endpoint])(**view_args)
#   self.ensure_sync(handler)(e)

# starlette — starlette/concurrency.py:34-37  (run_in_threadpool: sync→async bridge)
async def run_in_threadpool(func: Callable[P, T], *args: P.args, **kwargs: P.kwargs) -> T:
    func = functools.partial(func, *args, **kwargs)
    return await anyio.to_thread.run_sync(func)
```
