
## Error Strategy (6 patterns)

### Exception hierarchy with context-carrying base
*16 occurrences across 12 projects: Pillow, anyio, beartype, click, cryptography, hypothesis, jsonschema, polars, requests, starlette, textual, tornado*

A single RequestException base class accepts request and response objects via kwargs in __init__, automatically deriving request from response if not provided. All specialized exceptions (ConnectionError, Timeout, SSLError, etc.) inherit from it, forming a tree where catching the base catches all request errors, but catching a leaf catches only that specific failure. Multiple inheritance creates category overlaps (ConnectTimeout inherits both ConnectionError and Timeout).

**Why**: HTTP errors have rich context (which request failed, what response was received) that plain exception messages lose. Carrying request/response on the exception lets catchers inspect context without parsing strings. The multiple-inheritance tree (ConnectTimeout ⊂ ConnectionError ∩ Timeout) mirrors the domain: a connect timeout is both a connection error and a timeout, and catchers should be able to catch it as either. This is more expressive than a flat exception enum. [Merged from P134: CLI errors need progressively more context: a bad parameter needs to say which parameter, a usage error needs to show usage, a missing command needs suggestions. The hierarchy lets each level add its layer of context in format_message() without the caller needing to assemble it. The 'did you mean' pattern turns a cryptic error into a helpful suggestion using stdlib difflib.]

```python
# click — src/click/exceptions.py:55-100, 200-260
class UsageError(ClickException):
    exit_code: t.ClassVar[int] = 2
    def __init__(self, message: str, ctx: Context | None = None):
        super().__init__(message)
        self.ctx = ctx
        self.cmd = self.ctx.command if self.ctx else None

    def show(self, file=None):
        # prints usage + 'Try --help for help' + error message

class BadParameter(UsageError):
    def __init__(self, message, ctx=None, param=None, param_hint=None):
        super().__init__(message, ctx)
        sel
```

### ValidationError aggregates multiple field errors
*7 occurrences across 7 projects: attrs, celery, click, hypothesis, jsonschema, pydantic, pytest*

ValidationError contains a list of errors, each with location, type, and message. One validation pass collects all field-level errors.

```python
# celery — celery/exceptions.py:75-167
class CeleryError(Exception):
    """Base class for all Celery errors."""

class TaskPredicate(CeleryError):
    """Base class for task-related semi-predicates."""

class Retry(TaskPredicate):
    """The task is to be retried later."""
    message = None
    exc = None
    when = None

class Ignore(TaskPredicate):
    """A task can raise this to ignore doing state updates."""

class Reject(TaskPredicate):
    """A task can raise this if it wants to reject/re-queue the message."""

class TaskErro
```

### Result object for error isolation
*7 occurrences across 7 projects: attrs, more-itertools, pluggy, pytest, requests, textual, toolz*

Call results wrapped in Result object capturing both success and exception. Callers can get_result() (re-raise) or force_result() (suppress).

```python
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
            excinfo = ExceptionInfo.from_current
```

### Error handler lookup by MRO + scope cascade
*5 occurrences across 2 projects: flask, starlette*

Error handlers are registered in a nested dict: {scope: {code: {exception_class: handler}}}. Lookup walks the exception's MRO to find the most specific handler, cascading through blueprint scope → app scope, and HTTP code → generic. This allows registering handlers at different granularities: per-blueprint 404, app-wide DatabaseError, etc.

**Why**: Flexible error handling without a class hierarchy. A single registration system handles both HTTP status codes (404, 500) and arbitrary exception types (DatabaseError, ValidationError). MRO walk means registering a handler for HTTPException catches all subclasses. Blueprint scoping allows modules to handle their own errors without affecting the rest of the app. [Merged from P380: Enables registering a single handler for a base exception class (e.g. ValueError) that catches all subclasses automatically. No need to register every possible subclass. The MRO walk ensures the most specific handler is found first.] [Merged from P381: HTTP errors can be categorized by either status code (404, 500) or exception type (ValueError, KeyError). Two registries let users register handlers in whichever dimension is natural for their error. HTTPException bridges both: it carries a status code AND is an exception class.]

```python
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
                handler = handler_map.ge
```

### Exception as exit signal with exit_code class attribute
*5 occurrences across 4 projects: click, starlette, textual, tornado*

ClickException carries an exit_code class attribute (default 1, UsageError=2). Exit is a RuntimeError with __slots__=('exit_code',) that signals the application should stop. The main() method catches ClickException subclasses, calls show() for user-facing output, then sys.exit(e.exit_code). Abort is another RuntimeError that maps to exit code 1. This replaces sys.exit() calls inside command logic with exception-based control flow.

**Why**: Commands deep in the call chain need to signal 'stop the program with this code' without knowing whether they're running in standalone mode or being invoked from another command. Exceptions bubble naturally through the call stack. The exit_code on the exception class means different error types map to different codes (usage error=2, general error=1) without the caller needing to interpret the error type.

```python
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
```

### Exception-to-warning degradation for robust batch processing
*4 occurrences across 3 projects: beartype, cryptography, more-itertools*

A decorator factory accepts a warning_cls_on_decorator_exception config. When set (non-None), decoration failures are caught and converted to warnings instead of raising exceptions. The original object is returned unmodified. This is used by import hooks that process entire packages — one undecorable function should not crash the entire import.

**Why**: Import hooks (beartype.claw) automatically decorate all functions in a package. Real-world packages have functions beartype can't handle (C extensions, exotic signatures). Fail-fast would make import hooks practically useless — one bad function kills the entire import. Warning degradation allows the import to continue, type-checking what it can and warning about what it can't.

```python
# beartype — beartype/_decor/decorcore.py:75-130,201-270
def _beartype_object_nonfatal(obj, conf, **kwargs):
    try:
        return _beartype_object_fatal(obj, conf=conf, **kwargs)
    except Exception:
        warning_message = f'{prefix} not decoratable by @beartype, as:
    {format_exc()}'
        issue_warning(cls=warning_category, message=warning_message)
    return obj  # return unmodified
```

---

## Pipeline Composition (7 patterns)

### Processor chain: (logger, method_name, event_dict) → event_dict
*5 occurrences across 4 projects: attrs, celery, structlog, toolz*

Each processor takes a log entry dict and returns a (possibly modified) dict. Chain is a linear list of callables. Terminal processors return str/bytes.

```python
# celery — celery/utils/dispatch/signal.py:258-290
def send(self, sender, **named):
    """Send signal from sender to all connected receivers."""
    responses = []
    if not self.receivers or \
            self.sender_receivers_cache.get(sender) is NO_RECEIVERS:
        return responses
    for receiver in self._live_receivers(sender):
        try:
            response = receiver(signal=self, sender=sender, **named)
        except Exception as exc:
            logger.exception('Signal handler %r raised: %r', receiver, exc)
            response
```

### Iterator-first design: everything lazy, materialize on demand
*5 occurrences across 3 projects: more-itertools, polars, toolz*

All sequence functions return generators/iterators, never lists. Functions like mapcat, concat, interleave, unique, accumulate, sliding_window, partition, partition_all, pluck, and interpose use yield or return iterator-producing constructs (itertools.islice, itertools.chain.from_iterable). The caller materializes with list(), tuple(), or iterates directly. Even groupby returns a dict of lists only because the grouping operation requires materialization.

**Why**: Lazy evaluation enables working with infinite sequences and large datasets without memory pressure. Functions compose without intermediate materialization — pipe(data, map(f), filter(g), unique) processes each element through the full chain before the next element is read. This is the functional programming contract: functions transform streams, they don't collect results.

```python
# more-itertools — more_itertools/more.py:3549-3600
class time_limited:
    def __init__(self, limit_seconds, iterable):
        if limit_seconds < 0:
            raise ValueError('limit_seconds must be positive')
        self.limit_seconds = limit_seconds
        self._iterator = iter(iterable)
        self._start_time = monotonic()
        self.timed_out = False

    def __next__(self):
        if self.limit_seconds == 0:
            self.timed_out = True
            raise StopIteration
        item = next(self._iterator)
        if monotonic()
```

### Pipeline as named step chain
*3 occurrences across 3 projects: celery, polars, scikit-learn*

Pipeline holds [(name, estimator)] pairs. Data flows through fit_transform of each step. Steps addressable via name__param syntax.

```python
# celery — celery/canvas.py:758-785
def __or__(self, other):
    """Chaining operator.
    Example:
        >>> add.s(2, 2) | add.s(4) | add.s(8)
    Returns:
        chain: Constructs a :class:`~celery.canvas.chain` of the given signatures.
    """
    if isinstance(other, _chain):
        return _chain(seq_concat_seq((self,), other.unchain_tasks()), app=self._app)
    elif isinstance(other, group):
        other = maybe_unroll_group(other)
        return _chain(self, other, app=self.app)
    elif isinstance(other, Signature):
  
```

### IO manager: two-method serialization boundary
*3 occurrences across 3 projects: celery, dagster, flask*

Entire IO contract is two methods: load_input(context) (read) and handle_output(context, obj) (write). IO manager never touches compute function.

```python
# flask — src/flask/sessions.py:97-120
class SessionInterface:
    """The basic interface you have to implement in order to replace the
    default session interface which uses werkzeug's securecookie
    implementation."""

    null_session_class = NullSession
    pickle_based = False

    def make_null_session(self, app: Flask) -> NullSession:
        return self.null_session_class()

    def is_null_session(self, obj: object) -> bool:
        return isinstance(obj, self.null_session_class)

    def open_session(self, app: Flask, r
```

### Code generation via string templating + eval
*3 occurrences across 2 projects: attrs, beartype*

Instead of dynamically building methods via closures or descriptors, generate Python source code as strings, compile and eval them at class-definition time. The generated code is registered with linecache for debugger support. This produces real function objects with correct __qualname__, __doc__, and stack traces, not lambdas or wrappers.

**Why**: Generated methods (like __init__, __repr__, __eq__) need to be fast — they're on every hot path. String-generated code compiles to real bytecode with direct attribute access (self.x = value), avoiding the overhead of getattr/setattr loops or generic dispatch. The linecache registration makes the generated code visible to debuggers like PDB, closing the gap between generated and hand-written code. [Merged from P204: Runtime type-checking requires per-callable custom validation logic. Code generation produces O(1) wrappers with zero interpretation overhead — the type-check is baked into the generated code as a single boolean expression, not dispatched at runtime. compile()+exec() is preferred over eval() because compile() allows setting a custom co_filename for debuggability.]

```python
# attrs — src/attr/_make.py:221-260, 2154-2270
def _linecache_and_compile(script, filename, globs, locals=None):
    locs = {} if locals is None else locals
    count = 1
    base_filename = filename
    while True:
        linecache_tuple = (len(script), None, script.splitlines(True), filename)
        old_val = linecache.cache.setdefault(filename, linecache_tuple)
        if old_val == linecache_tuple:
            break
        filename = f"{base_filename[:-1]}-{count}>"
        count += 1
    _compile_and_eval(script, globs, locs, filenam
```

### on_setattr hook pipe for post-construction attribute mutation
*3 occurrences across 2 projects: attrs, textual*

After construction, attribute assignment can trigger a pipeline of hooks (convert → validate) via setters.pipe(). Each hook receives (instance, attribute, new_value) and returns the (possibly transformed) value. NO_OP sentinel disables hooks per-attribute. The pipe is composable: a list of setters is auto-wrapped into pipe(*setters).

**Why**: Construction-time validation is common, but post-construction mutation (obj.x = new_value) usually bypasses validators. The on_setattr hook extends the validation/conversion pipeline to every attribute assignment, not just __init__. The pipe composition allows ordering (convert before validate), and NO_OP gives per-field escape hatches without disabling the class-wide policy.

```python
# attrs — src/attr/setters.py:1-79
def pipe(*setters):
    def wrapped_pipe(instance, attrib, new_value):
        rv = new_value
        for setter in setters:
            rv = setter(instance, attrib, rv)
        return rv
    return wrapped_pipe

def validate(instance, attrib, new_value):
    if _config._run_validators is False:
        return new_value
    v = attrib.validator
    if not v:
        return new_value
    v(instance, attrib, new_value)
    return new_value

def convert(instance, attrib, new_value):
    c = attrib
```

### Prepare/send two-phase request lifecycle
*3 occurrences across 3 projects: cryptography, requests, starlette*

Request → PreparedRequest separates the user-facing API from the wire format. Request is a user-friendly container with optional fields. PreparedRequest is the immutable-ish internal representation with fully resolved URL, encoded body, merged headers, and attached auth. The prepare() method is a multi-step pipeline: prepare_method → prepare_url → prepare_headers → prepare_cookies → prepare_body → prepare_auth → prepare_hooks, each operating on the PreparedRequest in sequence.

**Why**: Users think in terms of 'GET this URL with these params and this auth', but the wire needs a fully resolved URL string, encoded body bytes, and merged headers. Separating the two phases means: (1) Session can merge its own settings (default headers, cookies, auth) with per-request overrides during preparation; (2) PreparedRequest can be serialized/pickled and sent later; (3) The prepare pipeline makes the transformation steps explicit and individually testable. Auth must be last because it may depend on the fully prepared request (e.g. signing the body).

```python
# starlette — starlette/routing.py:48-67
def request_response(
    func: Callable[[Request], Awaitable[Response] | Response],
) -> ASGIApp:
    f: Callable[[Request], Awaitable[Response]] = (
        func if is_async_callable(func) else functools.partial(run_in_threadpool, func)
    )

    async def app(scope: Scope, receive: Receive, send: Send) -> None:
        request = Request(scope, receive, send)

        async def app(scope: Scope, receive: Receive, send: Send) -> None:
            response = await f(request)
            await r
```

---

## Sync Async (2 patterns)

### Duplication over abstraction for sync/async
*4 occurrences across 4 projects: celery, httpx, textual, tornado*

Maintain parallel sync and async APIs as separate classes. ~400 lines of near-duplicate code for readability and debuggability.

```python
# textual — src/textual/message_pump.py:558-630
class MessagePump(metaclass=_MessagePumpMeta):
    async def _process_messages_loop(self) -> None:
        while not self._closed:
            message = await self._get_message()
            await self._dispatch_message(message)

    async def call_next(self, callback, *args) -> None:
        self._next_callbacks.append(events.Callback(callback=partial(callback, *args)))

    async def call_later(self, callback, *args) -> None:
        self._next_callbacks.append(events.Callback(callback=partial
```

### ensure_sync: sync/async transparent bridge
*4 occurrences across 3 projects: anyio, flask, starlette*

The app.ensure_sync(func) method returns func as-is if it's a plain def, or wraps it with async_to_sync if it's async def. Every call site that invokes user-provided callbacks (view functions, before_request, after_request, teardown) routes through ensure_sync. Override this single method to change how async code is run.

**Why**: Flask supports both sync and async view functions transparently. Instead of duplicating the entire request pipeline for sync/async (like httpx does for Client/AsyncClient), Flask wraps async functions at the call site. The overhead is one iscoroutinefunction() check per call. Overriding ensure_sync allows alternative async runtimes (e.g., using gevent instead of asyncio).

```python
# flask — src/flask/app.py:966-985
def ensure_sync(self, func: t.Callable[..., t.Any]) -> t.Callable[..., t.Any]:
    if iscoroutinefunction(func):
        return self.async_to_sync(func)
    return func

# Every call site:
# self.ensure_sync(before_func)()
# self.ensure_sync(self.view_functions[rule.endpoint])(**view_args)
# self.ensure_sync(handler)(e)
```

---
