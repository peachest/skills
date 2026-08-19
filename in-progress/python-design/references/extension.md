
## Config Management (2 patterns)

### Config layering with per-field merge semantics
*7 occurrences across 6 projects: celery, dbt-core, flask, hypothesis, requests, tornado*

Config cascade: project → profile → model → runtime. Different fields need different merge strategies: replace-if-none, append, deep merge.

```python
# flask — src/flask/config.py:76-230
class Config(dict):
    def from_envvar(self, variable_name: str, silent: bool = False) -> bool: ...
    def from_prefixed_env(self, prefix: str = "FLASK", *, loads=json.loads) -> bool: ...
    def from_pyfile(self, filename: str, silent: bool = False) -> bool: ...
    def from_object(self, obj: object | str) -> None:
        if isinstance(obj, str):
            obj = import_string(obj)
        for key in dir(obj):
            if key.isupper():
                self[key] = getattr(obj, key)
    d
```

### Environment variable defaults with typed coercion
*3 occurrences across 3 projects: beartype, loguru, starlette*

All default configuration values are read from environment variables with type coercion. A single env() helper function handles str, bool, and int types with appropriate parsing and validation. Each config parameter has a sensible fallback default if the env var is not set.

**Why**: Environment variables enable configuration without code changes — useful for Docker, CI, and 12-factor apps. The typed coercion ensures bool env vars are actually booleans (not strings 'true'/'false'), preventing subtle bugs. Centralizing the env-reading logic in one function avoids scattered os.environ.get() calls with inconsistent parsing. The naming convention (LOGURU_PARAM) is discoverable.

```python
# loguru — loguru/_defaults.py:4-28
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
        raise ValueError("Invalid environment variable '%s' (expected a boolean): '%s'" % (key, val))
    if type_ is int:
        try:
            r
```

---

## Plugin Architecture (5 patterns)

### Hook spec / impl separation
*12 occurrences across 11 projects: Pillow, celery, click, flask, hypothesis, loguru, pluggy, pytest, requests, textual, tornado*

Two decorators define contract and implementation. @hookspec and @hookimpl stamp attributes, do NOT wrap function. Function remains directly callable.

```python
# flask — src/flask/sansio/blueprints.py:137-175
class Blueprint(Scaffold):
    _got_registered_once = False

    def __init__(self, name, import_name, ...):
        ...
        self.deferred_functions: list[DeferredSetupFunction] = []

    @setupmethod
    def record(self, func: DeferredSetupFunction) -> None:
        """Registers a function that is called when the blueprint is
        registered on the application."""
        self.deferred_functions.append(func)

    @setupmethod
    def record_once(self, func: DeferredSetupFunction) -> None
```

### Swappable execution strategy
*10 occurrences across 10 projects: Pillow, anyio, beartype, celery, cryptography, hypothesis, pluggy, pytest, textual, tornado*

Instead of decorators or class hierarchy, swap a function reference _inner_hookexec. Tracing/monitoring work by replacing one attribute. undo() restores.

```python
# tornado — tornado/util.py:204-330
class Configurable:
    __impl_class = None
    __impl_kwargs = None

    def __new__(cls, *args, **kwargs):
        base = cls.configurable_base()
        if cls is base:
            impl = cls.configured_class()
            if base.__impl_kwargs:
                init_kwargs.update(base.__impl_kwargs)
        else:
            impl = cls
        instance = super().__new__(impl)
        instance.initialize(*args, **init_kwargs)
        return instance

    @classmethod
    def configure(cls, imp
```

### Pluggable class attributes for framework extension points
*8 occurrences across 6 projects: click, flask, jsonschema, polars, starlette, textual*

The App class declares overridable class attributes (request_class, response_class, session_interface, json_provider_class, jinja_environment, url_map_class, url_rule_class, test_client_class) that serve as extension points. Subclassing Flask and overriding these attributes customizes behavior without rewriting methods. This is a declarative plugin system: set the class, get the behavior.

**Why**: Class attributes are the simplest possible extension point — no registry, no decorator, no hook. Just subclass and set an attribute. This is sufficient for most customization needs (custom Request class, custom JSON provider, custom session backend) and avoids the complexity of a full plugin system for the common case. The default class attributes also serve as documentation of what's pluggable.

```python
# textual — src/textual/widget.py:353-373
_PSEUDO_CLASSES: ClassVar[dict[str, Callable[[Widget], bool]]] = {
    "hover": lambda widget: widget.mouse_hover,
    "focus": lambda widget: widget.has_focus,
    "blur": lambda widget: not widget.has_focus,
    "can-focus": lambda widget: widget.allow_focus(),
    "disabled": lambda widget: widget.is_disabled,
    "enabled": lambda widget: not widget.is_disabled,
    "dark": lambda widget: widget.app.current_theme.dark,
    "light": lambda widget: not widget.app.current_theme.dark,
    "focus
```

### Signal: observer pattern with weak references and robust dispatch
*7 occurrences across 6 projects: Pillow, celery, hypothesis, matplotlib, polars, textual*

A Signal object maintains a list of receiver callables. `connect()` registers receivers with optional `dispatch_uid` for dedup, `weak` references for automatic cleanup, and `sender` filtering. `send()` calls all live receivers, catching exceptions per-receiver and returning `(receiver, response_or_exception)` pairs. Dead weak references are cleaned lazily. Supports `retry` mode that wraps receivers with `retry_over_time` for transient failures.

**Why**: A distributed task system emits events at many lifecycle points (task received, started, succeeded, failed, retried, revoked). Extensions need to hook into these events without modifying core code. The observer pattern decouples event emission from handling. Weak references prevent memory leaks when handlers are garbage collected. Per-receiver exception isolation prevents one broken handler from crashing the entire dispatch chain. [Merged from P307: GUI callbacks are a major source of memory leaks when bound methods hold references. Weakrefs allow the receiver to be GC'd. Exception isolation prevents one bad callback from crashing the entire event dispatch. The signal filter prevents typos from silently creating dead callbacks.]

```python
# celery — celery/utils/dispatch/signal.py:81-130
class Signal:
    def __init__(self, providing_args=None, use_caching=False, name=None):
        self.receivers = []
        self.providing_args = set(providing_args if providing_args is not None else [])
        self.lock = threading.Lock()
        self.use_caching = use_caching
        self.name = name
        self.sender_receivers_cache = weakref.WeakKeyDictionary() if use_caching else {}
        self._dead_receivers = False

    def connect(self, *args, **kwargs):
        def _handle_options
```

### Registry as dict subclass with __missing__ guard
*5 occurrences across 5 projects: Pillow, celery, click, polars, starlette*

A registry that inherits from `dict` and overrides `__missing__` to raise a custom NotRegistered error when an unregistered key is accessed. Registration accepts either a class (auto-instantiated) or an instance. The registry enforces that registered items have a `name` attribute used as the key.

**Why**: Using dict as the base class provides free serialization, iteration, and standard dict operations. The `__missing__` override turns silent KeyError into a meaningful domain error (NotRegistered) that users can catch. Auto-instantiation of classes simplifies registration: `registry.register(MyTaskClass)` instead of `registry.register(MyTaskClass())`.

```python
# celery — celery/app/registry.py:14-50
class TaskRegistry(dict):
    """Map of registered tasks."""
    NotRegistered = NotRegistered

    def __missing__(self, key):
        raise self.NotRegistered(key)

    def register(self, task):
        if task.name is None:
            raise InvalidTaskError(
                'Task class {!r} must specify .name attribute'.format(
                    type(task).__name__))
        task = inspect.isclass(task) and task() or task
        add_autoretry_behaviour(task)
        self[task.name] = task
```

---

## State Context (2 patterns)

### ContextVar + LocalProxy for implicit context access
*7 occurrences across 5 projects: anyio, flask, hypothesis, loguru, textual*

Per-request/per-app state is stored in ContextVar objects (not thread-locals). Module-level LocalProxy instances read from these ContextVars, providing implicit access to current_app, request, session, g without passing them as parameters. The proxy raises a descriptive error when accessed outside a context.

**Why**: View functions and helpers access request/app state without explicit parameter passing, keeping signatures clean. ContextVar (over thread-local) is async-safe — works correctly with asyncio, greenlets, and concurrent requests. The LocalProxy transparently delegates attribute access, so `request.json` works exactly as if request were a local variable.

```python
# textual — src/textual/_context.py:13-28
class NoActiveAppError(RuntimeError):
    """Runtime error raised if we try to retrieve the active app when there is none."""

active_app: ContextVar["App[Any]"] = ContextVar("active_app")
active_message_pump: ContextVar["MessagePump"] = ContextVar("active_message_pump")
prevent_message_types_stack: ContextVar[list[set[type[Message]]]] = ContextVar("prevent_message_types_stack")
visible_screen_stack: ContextVar[list[Screen[object]]] = ContextVar("visible_screen_stack")
message_hook: ContextVar[C
```

### Context manager as request/app lifecycle boundary
*5 occurrences across 5 projects: click, flask, loguru, polars, starlette*

AppContext and RequestContext implement __enter__/__exit__ to manage setup and teardown. push() binds the context to the current ContextVar, pop() runs teardown handlers and resets the token. The request lifecycle is: ctx.push() → dispatch → ctx.pop(error), wrapped in try/finally. Teardown functions always run, even on error.

**Why**: Context managers ensure cleanup (teardown handlers, DB disconnection) runs regardless of success or failure. The try/finally in wsgi_app guarantees ctx.pop() even on unhandled exceptions. This is the pipeline boundary between HTTP transport and application logic — everything inside is per-request scoped.

```python
# starlette — starlette/routing.py:581-610
async def lifespan(self, scope: Scope, receive: Receive, send: Send) -> None:
    started = False
    app: Any = scope.get("app")
    await receive()
    try:
        async with self.lifespan_context(app) as maybe_state:
            if maybe_state is not None:
                if "state" not in scope:
                    raise RuntimeError('The server does not support "state" in the lifespan scope.')
                scope["state"].update(maybe_state)
            await send({"type": "lifespan.star
```

---
