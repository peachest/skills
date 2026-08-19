
## Data Modeling (10 patterns)

### __init__ as the parameter contract
*22 occurrences across 18 projects: Pillow, attrs, beartype, celery, click, cryptography, flask, hypothesis, loguru, more-itertools, polars, pytest, requests, scikit-learn, starlette, textual, toolz, tornado*

Constructor signature IS the parameter schema. Discovered via inspect.signature(). No *args/**kwargs. Fitted state uses _ suffix.

```python
# flask — src/flask/sansio/app.py:239-280
class App(Scaffold):
    default_config: dict[str, t.Any]
    response_class: type[Response]

    def __init__(
        self,
        import_name: str,
        static_url_path: str | None = None,
        static_folder: str | os.PathLike[str] | None = "static",
        host_matching: bool = False,
        subdomain_matching: bool = False,
        template_folder: str | os.PathLike[str] | None = "templates",
        instance_path: str | None = None,
        instance_relative_config: bool = False,

```

### __slots__ everywhere for value objects
*19 occurrences across 13 projects: anyio, attrs, beartype, celery, click, hypothesis, loguru, more-itertools, pluggy, pytest, textual, toolz, tornado*

Every class uses __slots__: prevents accidental attribute creation, reduces memory, signals fixed-shape data object.

```python
# tornado — tornado/ioloop.py:837-855
class _Timeout:
    """An IOLoop timeout, a UNIX timestamp and a callback"""

    # Reduce memory overhead when there are lots of pending callbacks
    __slots__ = ["deadline", "callback", "tdeadline"]

    def __init__(
        self, deadline: float, callback: Callable[[], None], io_loop: IOLoop
    ) -> None:
        if not isinstance(deadline, numbers.Real):
            raise TypeError("Unsupported deadline %r" % deadline)
        self.deadline = deadline
        self.callback = callback
    
```

### Sentinel object for distinguishing 'no value' from None
*15 occurrences across 12 projects: Pillow, anyio, attrs, beartype, click, hypothesis, jsonschema, more-itertools, polars, starlette, textual, tornado*

A dedicated sentinel enum member (NOTHING) used as the default for optional fields where None is a valid user-supplied value. The sentinel is falsy (bool(NOTHING) == False) and has a custom __repr__ returning 'NOTHING'. Type annotation uses Literal[NOTHING] via NothingType.

**Why**: When None is a legitimate value (e.g., a field that can be null), you can't use None as the 'no default provided' marker. A sentinel object distinguishes 'user didn't provide a value' from 'user explicitly passed None'. Making it an enum variant (not a bare object()) gives it a stable identity for pickling and a repr that's meaningful in error messages. [Merged from P267: When None is a semantically valid value (e.g. autoescape=None means disable escaping), a plain default=None is ambiguous — you can't tell if the user explicitly chose None or just didn't pass the argument. A sentinel object is identity-comparable (is _UNSET), has no false-positive collisions, and self-documents intent via its type annotation.]

```python
# tornado — tornado/template.py:220-295
class _UnsetMarker:
    pass

_UNSET = _UnsetMarker()

class Template:
    def __init__(self, template_string, name="<string>", loader=None,
                 compress_whitespace: Union[bool, _UnsetMarker] = _UNSET,
                 autoescape: Optional[Union[str, _UnsetMarker]] = _UNSET,
                 whitespace: Optional[str] = None):
        if not isinstance(autoescape, _UnsetMarker):
            self.autoescape = autoescape
        elif loader:
            self.autoescape = loader.autoesc
```

### @dataclass(frozen=True, slots=True) as validator container
*8 occurrences across 6 projects: anyio, attrs, hypothesis, pydantic, pytest, textual*

Value objects that carry no behavior beyond identity — frozen + slots signals fixed-shape data object.

```python
# hypothesis — hypothesis/src/hypothesis/internal/conjecture/data.py:627-655
@dataclass(slots=True, frozen=True)
class ConjectureResult:
    """Result class storing the parts of ConjectureData that we
    will care about after the original ConjectureData has outlived its
    usefulness."""

    status: Status
    interesting_origin: InterestingOrigin | None
    nodes: tuple[ChoiceNode, ...] = field(repr=False, compare=False)
    length: int
    notes: list[str]
    expected_exception: BaseException | None
    expected_traceback: str | None
    has_discards: bool
    targ
```

### evolve() for non-destructive immutable updates
*7 occurrences across 6 projects: attrs, cryptography, jsonschema, loguru, more-itertools, textual*

evolve(inst, **changes) creates a new instance of the same class with specified fields overridden. It reads the existing field values via getattr, fills in unchanged fields from the original instance, and constructs a new instance via cls(**changes). Works with both frozen and mutable classes.

**Why**: Frozen (immutable) classes can't be updated in place — but you still need to 'change' a field. evolve() provides a copy-with-changes operation that reads the compiled field metadata (__attrs_attrs__) to know which fields to copy and which to override. This is the functional update pattern: instead of obj.x = new_x, you write evolve(obj, x=new_x), getting a new instance.

```python
# textual — src/textual/reactive.py:286-310
def __get__(self, obj, obj_type):
    if obj is None:
        return self
    if not hasattr(obj, self.internal_name):
        self._initialize_reactive(obj, self.name)
    if hasattr(obj, self.compute_name):
        old_value = getattr(obj, internal_name)
        value = getattr(obj, self.compute_name)()
        setattr(obj, internal_name, value)
        self._check_watchers(obj, self.name, old_value)
        return value
    else:
        return getattr(obj, internal_name)

    def _set(self, 
```

### Ordered enum with navigation methods
*6 occurrences across 6 projects: Pillow, anyio, beartype, cryptography, pytest, textual*

Scope(Enum) uses @total_ordering with __lt__ based on declaration order index. Provides next_lower() and next_higher() for navigating the scope hierarchy. from_user() classmethod converts a string to enum with a friendly error message including context (where the conversion happened). The ordering (Function < Class < Module < Package < Session) is semantically meaningful: higher scopes outlive lower scopes.

**Why**: Fixture scopes form a hierarchy where containment matters: a session-scoped fixture must be set up before any module-scoped fixture, and torn down after all of them. An ordered enum with navigation methods lets the framework compare scopes (scope_a < scope_b), find adjacent scopes (for caching decisions), and convert user strings to enums with context-rich errors. @total_ordering provides all comparison operators from __lt__ + __eq__ for free.

```python
# pytest — src/_pytest/scope.py:18-60
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
        return _SCOPE_INDICES[se
```

### Sentinel string as module-level default marker
*6 occurrences across 5 projects: Pillow, beartype, more-itertools, starlette, toolz*

Module-level sentinel strings like no_default = '__no__default__' distinguish 'no value provided' from None (which is a valid default). Functions check `if default is no_default` to detect whether the caller passed a default at all, versus passing None as the intended default.

**Why**: Python's convention of using None as a default sentinel breaks when None is a valid value. The string sentinel is simple, picklable, and visible in tracebacks. Unlike object() sentinels (which require module-level singletons and are not picklable), string sentinels are self-describing and survive serialization. The pattern recurs across itertoolz.py and utils.py.

```python
# beartype — beartype/_data/func/datafuncarg.py:38-55
ARG_VALUE_UNPASSED = 0xBABECAFE
'''
Unpassed argument value (i.e., arbitrary magic constant serving as the
default value of an optional parameter accepted by a callable).

This constant is intentionally defined as an arbitrary integer literal
compatible with the PEP 586-compatible typing.Literal type hint factory.
```

### Metaclass-driven model construction
*4 occurrences across 3 projects: attrs, polars, pydantic*

Metaclass intercepts class creation to build validators/serializers at definition time, not instantiation time. __init__ becomes thin delegate.

**Why**: Storing compiled field metadata as a class-level constant means field introspection (fields(), has(), asdict()) is O(1) — it reads a pre-computed tuple, not __annotations__ or __init__ signature. The named-property tuple subclass allows both index access (fields(Cls)[0]) and name access (fields(Cls).x), matching how users naturally think about fields. The metadata is computed once at decoration time, not on every introspection call.

```python
# attrs — src/attr/_make.py:268-300, 719, 1900-1935
def _make_attr_tuple_class(cls_name, attr_names):
    attr_class_name = f"{cls_name}Attributes"
    body = {}
    for i, attr_name in enumerate(attr_names):
        def getter(self, i=i):
            return self[i]
        body[attr_name] = property(getter)
    return type(attr_class_name, (tuple,), body)

# In _ClassBuilder.__init__:
self._cls_dict["__attrs_attrs__"] = self._attrs

# fields() reads it:
def fields(cls):
    attrs = getattr(cls, "__attrs_attrs__", None)
    if attrs is None:
    
```

### ImmutableDict for framework defaults
*3 occurrences across 3 projects: flask, hypothesis, starlette*

Framework-wide default configurations and options use ImmutableDict (from werkzeug), a dict subclass that raises TypeError on mutation. Class-level defaults like default_config are ImmutableDict, signaling that these are read-only templates to be copied, not mutated in place.

**Why**: Class attributes are shared across all instances. If default_config were a regular dict, mutating it in one instance would affect all others. ImmutableDict prevents this at the language level — the only way to customize config is to copy and modify, which is the correct pattern. It also signals intent to readers: this value is a specification, not a working copy.

```python
# hypothesis — hypothesis/src/hypothesis/_settings.py:536-565
class settingsMeta(type):
    @property
    def default(cls) -> Optional["settings"]:
        v = default_variable.value
        if v is not None:
            return v
        ...

    def __setattr__(cls, name: str, value: object) -> None:
        if name == "default":
            raise AttributeError("Cannot assign to the property settings.default")
        elif not name.startswith("_"):
            raise AttributeError(
                f"Cannot assign hypothesis.settings.{name}={value!r} - th
```

### Immutable invocation spec with copy-on-modify
*3 occurrences across 3 projects: jsonschema, loguru, pytest*

CallSpec2 is a @dataclasses.dataclass(frozen=True) representing a planned parametrized test invocation. setmulti() creates a NEW CallSpec2 with updated fields instead of mutating self. Multiple parametrize() calls produce a cartesian product: each call's setmulti() is applied to every existing CallSpec2, creating new instances for each combination. The result is a list of immutable specs, each representing one test invocation.

**Why**: Parametrization is multiplicative: @parametrize('x', [1,2]) then @parametrize('y', [3,4]) produces 4 invocations. Copy-on-modify makes this clean: for each existing spec, create a new spec for each new parameter value. If specs were mutable, the cartesian product would require careful cloning to avoid aliasing bugs. Frozen dataclass prevents accidental mutation of specs after collection, which would break test isolation.

```python
# jsonschema — jsonschema/_types.py:72-95
@frozen(repr=False)
class TypeChecker:
    _type_checkers: HashTrieMap = field(default=HashTrieMap(), converter=_typed_map_converter)

    def redefine(self, type, fn) -> TypeChecker:
        return self.redefine_many({type: fn})

    def redefine_many(self, definitions=()) -> TypeChecker:
        type_checkers = self._type_checkers.update(definitions)
        return evolve(self, type_checkers=type_checkers)

    def remove(self, *types) -> TypeChecker:
        type_checkers = self._type_checker
```

---

## Serialization (2 patterns)

### __getstate__/__setstate__ for pickleable objects with non-pickleable internals
*15 occurrences across 9 projects: Pillow, beartype, hypothesis, loguru, more-itertools, polars, requests, starlette, tornado*

Session, PreparedRequest, Response, and HTTPAdapter all define __getstate__ and __setstate__ using a __attrs__ class attribute that lists the serializable field names. __getstate__ extracts only those fields; __setstate__ restores them, often re-initializing non-pickleable internals (like urllib3 PoolManager) from the stored config. This whitelisting approach controls exactly what survives pickling.

**Why**: HTTP clients contain non-pickleable objects (socket connections, urllib3 PoolManager, threading.local). But users need to pickle requests for multiprocessing, caching, or testing. The __attrs__ whitelist ensures only serializable state (config, headers, cookies, body bytes) survives, while __setstate__ reconstructs the non-serializable parts from stored config. HTTPAdapter's __setstate__ re-initializes the pool manager from stored _pool_connections/_pool_maxsize values. [Merged from P169: Tracebacks cannot be pickled — they contain frame references that don't survive serialization. When logs cross process boundaries (via multiprocessing queue with enqueue=True), the exception record must be serialized. Rather than failing, __reduce__ degrades gracefully: it preserves the exception type and tries to preserve the value, dropping what can't be pickled. The custom reduce protocol (returning a different reconstruction callable) allows the round-trip to use a cached pickle blob for efficiency.]

```python
# loguru — loguru/_handler.py:319-342
def __getstate__(self):
    state = self.__dict__.copy()
    state["_lock"] = None
    state["_lock_acquired"] = None
    state["_memoize_dynamic_format"] = None
    if self._enqueue:
        state["_sink"] = None
        state["_thread"] = None
        state["_owner_process"] = None
        state["_queue_lock"] = None
    return state

def __setstate__(self, state):
    self.__dict__.update(state)
    self._lock = create_handler_lock()
    self._lock_acquired = threading.local()
    if self._en
```

### model_dump() / model_dump_json() with mode selection
*3 occurrences across 3 projects: attrs, pydantic, pytest*

Separate Python-native dump (→ dict) from JSON dump (→ str). Support include/exclude, by_alias, exclude_unset. Serializer built at class definition time.

```python
# attrs — src/attr/_funcs.py:24-120
def asdict(inst, recurse=True, filter=None, dict_factory=dict,
          retain_collection_types=False, value_serializer=None):
    attrs = fields(inst.__class__)
    rv = dict_factory()
    for a in attrs:
        v = getattr(inst, a.name)
        if filter is not None and not filter(a, v):
            continue
        if value_serializer is not None:
            v = value_serializer(inst, a, v)
        if recurse is True:
            value_type = type(v)
            if value_type in _ATOMIC_TY
```

---

## Validation (2 patterns)

### Input validation via check_array / validate_params
*5 occurrences across 4 projects: attrs, cryptography, hypothesis, scikit-learn*

Two-tier validation: parameter validation (decorator-based, checks hyperparameters) and input validation (runtime, checks data shapes/types).

```python
# hypothesis — hypothesis/src/hypothesis/internal/validation.py:18-40
@check_function
def check_type(typ: type | tuple[type, ...], arg: object, name: str) -> None:
    if not isinstance(arg, typ):
        if isinstance(typ, tuple):
            assert len(typ) >= 2, "Use bare type instead of len-1 tuple"
            typ_string = "one of " + ", ".join(t.__name__ for t in typ)
        else:
            typ_string = typ.__name__
        raise InvalidArgument(
            f"Expected {typ_string} but got {name}={arg!r} (type={type(arg).__name__})"
        )
```

### Types as schemas — no separate schema object
*3 occurrences across 3 projects: attrs, beartype, msgspec*

Type annotation IS the schema. No separate Schema()/Model()/Field() definition step.

```python
# attrs — src/attr/_make.py:379-505
def _transform_attrs(cls, these, auto_attribs, kw_only, ...):
    anns = _get_annotations(cls)
    if auto_attribs is True:
        for attr_name, type in anns.items():
            if _is_class_var(type):
                continue
            annot_names.add(attr_name)
            a = cd.get(attr_name, NOTHING)
            if a.__class__ is not _CountingAttr:
                a = attrib(a)
            ca_list.append((attr_name, a))
```
