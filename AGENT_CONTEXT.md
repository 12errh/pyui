# PyUI — Complete Agent Context

> This file is the single source of truth for any AI agent working on this codebase.
> Read this before touching anything. It covers architecture, conventions, current state, and what comes next.

---

## What Is PyUI

PyUI is an open-source Python UI framework. The core idea: write your entire UI in pure Python, and the framework compiles it to whatever target you need — currently web (HTML + Tailwind CSS + Alpine.js), with desktop (Qt/tkinter) and terminal (Rich TUI) planned.

- **Version:** 1.0.0
- **Python:** 3.10+
- **License:** MIT
- **Repo:** https://github.com/12errh/pyui
- **Status:** v1.0.0 — All phases complete

---

## Project Structure

```
pyui/
├── src/pyui/                    # Main package (installed as pyui-framework)
│   ├── __init__.py              # Public API — all user-facing exports live here
│   ├── app.py                   # App base class + AppMeta metaclass
│   ├── page.py                  # Page class (routable screen)
│   ├── exceptions.py            # PyUIError, CompilerError, ComponentError, ThemeError, PluginError
│   │
│   ├── components/              # All 42+ UI components
│   │   ├── base.py              # BaseComponent — root of all components
│   │   ├── layout/              # Flex, Grid, Stack, Container, Divider, Spacer, Sidebar, Split, List
│   │   ├── display/             # Text, Heading, Badge, Tag, Avatar, Icon, Image, Markdown, RawHTML
│   │   ├── input/               # Button, Input, Textarea, Select, Checkbox, Radio, Toggle, Slider, DatePicker, FilePicker, Form
│   │   ├── feedback/            # Alert, Toast, Modal, Drawer, Tooltip, Progress, Spinner, Skeleton
│   │   ├── navigation/          # Nav, Tabs, Breadcrumb, Pagination, Menu
│   │   ├── data/                # Table, Stat, Chart
│   │   └── media/               # Video
│   │
│   ├── compiler/
│   │   ├── ir.py                # IR builder — converts component tree → IRTree
│   │   └── discovery.py         # discover_app() — imports user .py file, finds App subclass
│   │
│   ├── renderers/
│   │   └── web/
│   │       ├── generator.py     # WebGenerator — IRTree → full HTML pages
│   │       └── tailwind.py      # Tailwind CSS class mappings for every component
│   │
│   ├── server/
│   │   └── dev_server.py        # aiohttp dev server, event POST handler, WebSocket stub
│   │
│   ├── state/
│   │   ├── reactive.py          # ReactiveVar + reactive() factory
│   │   ├── computed.py          # ComputedVar + computed() factory
│   │   └── store.py             # Global Store singleton
│   │
│   ├── theme/
│   │   └── tokens.py            # DEFAULT_TOKENS + 6 built-in themes (light, dark, ocean, sunset, forest, rose)
│   │
│   ├── cli/
│   │   ├── main.py              # Click CLI entry point (pyui command)
│   │   ├── storybook.py         # pyui storybook — component gallery server
│   │   └── commands/            # Placeholder for future subcommand modules
│   │
│   └── utils/
│       └── logging.py           # structlog-based logging setup
│
├── tests/
│   ├── conftest.py              # autouse fixture: resets global store between tests
│   ├── counter_reactive.py      # Minimal reactive counter demo
│   ├── portfolio.py             # Full cinematic portfolio demo (run with: python tests/portfolio.py)
│   ├── assets/                  # Images used by portfolio demo
│   ├── test_compiler/           # Unit tests for IR builder and discovery
│   └── test_renderers/          # Unit tests for web generator
│
├── app.py                       # Root demo app (pyui run app.py)
├── pyproject.toml               # Build config, deps, tool settings
├── CHANGELOG.md                 # Version history
└── CONTRIBUTING.md              # Contribution guide
```

---

## Compilation Pipeline

This is the most important thing to understand. Everything flows through this pipeline:

```
User Python file
      │
      ▼
compiler/discovery.py
  discover_app("app.py")
  → imports the module, finds the App subclass
      │
      ▼
compiler/ir.py
  build_ir_tree(AppClass)
  → walks App._pages, calls build_ir_page() for each Page
  → build_ir_page() calls page.compose() if it exists, then build_ir_node() for each child
  → build_ir_node() resolves props, detects ReactiveVars/lambdas, registers event handlers
  → returns IRTree (target-agnostic)
      │
      ▼
renderers/web/generator.py
  WebGenerator(ir_tree).render_ir_page(ir_page)
  → dispatches each IRNode to a _render_* function
  → _render_* functions call tailwind.py for CSS classes
  → returns complete HTML string
      │
      ▼
server/dev_server.py
  serves HTML over aiohttp
  handles POST /pyui-api/event/{handler_id} for button clicks etc.
  handles WebSocket /pyui-api/ws (hot-reload stub, Phase 6)
```

---

## Core Data Structures

### IRNode (compiler/ir.py)
```python
@dataclass
class IRNode:
    type: str                          # "button", "flex", "text", etc.
    props: dict[str, Any]              # resolved, serialisable props
    children: list[IRNode]
    events: dict[str, str]             # event_name → handler_id
    reactive_bindings: list[str]       # names of reactive vars this node depends on
    reactive_props: dict[str, list[str]]  # prop_name → [dep_var_names]
    style_variant: str | None          # "primary", "ghost", etc.
    theme_tokens: dict[str, str]
    node_id: str                       # unique DOM id (pyui-{uuid})
```

### IRPage
```python
@dataclass
class IRPage:
    route: str
    title: str
    layout: str          # "default" | "full-width" | "sidebar" | "auth"
    children: list[IRNode]
    meta: dict[str, str]
```

### IRTree
```python
@dataclass
class IRTree:
    app_meta: dict[str, Any]           # name, version, description, favicon
    pages: list[IRPage]
    theme: str | dict[str, str]
    reactive_vars: dict[str, Any]      # key → current value snapshot
    event_handlers: dict[str, Callable]
    persistent_vars: list[str]         # vars with persist=True → localStorage
```

---

## Component System

### BaseComponent (components/base.py)

Every component inherits from `BaseComponent`. Key internals:

- `_CONTEXT_STACK: list[Any]` — global stack. When you do `with Flex():`, the Flex is pushed onto this stack. Any component instantiated inside the `with` block auto-registers itself as a child via `parent.add(self)` in `__init__`.
- `component_type: str` — must be set on every subclass (e.g. `"button"`, `"flex"`). This is what the IR dispatcher uses.
- `props: dict[str, Any]` — all component-specific data lives here.
- `_style_variant`, `_size`, `_classes`, `_hidden`, `_disabled` — standard style state.
- Event handlers: `_on_click`, `_on_change`, `_on_hover`, `_on_mount`, `_on_unmount`.

### Chainable API (all methods return `self`)
```python
Button("Save")
    .style("primary")       # sets _style_variant
    .size("lg")             # sets _size
    .padding(4)             # sets _padding
    .className("my-class")  # appends to _classes
    .disabled(False)        # sets _disabled
    .onClick(handler)       # sets _on_click
```

### Declarative Composition (context manager pattern)
```python
class MyPage(Page):
    def compose(self):
        with Flex(direction="col", gap=6):
            Heading("Title")           # auto-added to Flex
            with Grid(cols=2):
                Text("A")              # auto-added to Grid
                Text("B")
```

### Adding a New Component — Checklist
1. Create file in the right `components/` subdirectory
2. Inherit from `BaseComponent`
3. Set `component_type = "your_type"` (snake_case)
4. Set `self.props` in `__init__`
5. Export from the subdirectory's `__init__.py`
6. Export from `src/pyui/__init__.py` (both import and `__all__`)
7. Add `"your_type": _render_your_type` to the dispatch dict in `renderers/web/generator.py`
8. Add `_render_your_type(node: IRNode) -> str` function in `generator.py`
9. Add Tailwind class helper in `renderers/web/tailwind.py` if needed

---

## State & Reactivity

### ReactiveVar (state/reactive.py)
```python
count = reactive(0)           # ReactiveVar[int]
name  = reactive("", persist=True)  # syncs to localStorage

count.get()                   # read value (also tracks dependency if inside computed)
count.set(5)                  # write value, notifies subscribers
count.subscribe(fn)           # returns unsubscribe callable
```

`persist=True` → the var name is added to `IRTree.persistent_vars` → the web renderer emits JS that saves/loads from `localStorage` under key `pyui_state_{name}`.

### ComputedVar (state/computed.py)
```python
doubled = computed(lambda: count.get() * 2)
doubled.get()   # auto-updates when count changes
doubled.set(x)  # raises AttributeError — read-only
```

Dependency tracking uses `_REACTIVE_CONTEXT` (a thread-local stack of sets). When `computed()` runs its fn, any `ReactiveVar.get()` call pushes itself into the current set. The ComputedVar subscribes to all of them.

### Store (state/store.py)
```python
from pyui import store

username = store.define("username", "Guest")   # creates ReactiveVar, raises if key exists
store.get("username").set("Alice")
store.snapshot()   # → {"username": "Alice"}
store.reset()      # clears all — used in tests
```

### How Reactivity Works in the Browser
1. `build_ir_tree()` snapshots all `ReactiveVar` values → `IRTree.reactive_vars`
2. `WebGenerator` serialises this as `window.__pyuiState = {...}` in the page HTML
3. Alpine.js store: `Alpine.store('pyui', { state: __pyuiState, nodes: __pyuiNodes })`
4. Reactive `Text` nodes use `x-text="$store.pyui.nodes['{node_id}']?.content"`
5. Input components with reactive `value` get `x-model="$store.pyui.state.{var_name}"`
6. On any event (button click, input change), browser POSTs to `/pyui-api/event/{handler_id}`
7. Dev server calls the Python handler, re-runs `build_ir_tree()`, collects updated node props
8. Returns `{"state": {...}, "nodes": {...}, "reload": false}` as JSON
9. Browser updates `Alpine.store('pyui')` → Alpine reactivity propagates to DOM

### REACTIVE_VAR_REGISTRY
`register_reactive_name(var, name)` is called during `build_ir_tree()` for every `ReactiveVar` found on the App class. This lets `build_ir_node()` look up the string name of a var (needed to generate correct Alpine `x-text`/`x-model` bindings).

---

## App & Page Classes

### App (app.py)
```python
class MyApp(App):
    name = "My App"
    theme = "dark"           # or a dict of token overrides
    fonts = ["Inter"]
    count = reactive(0)      # ReactiveVars on App are global state

    home = HomePage()        # Page instances auto-discovered by AppMeta
```

`AppMeta` metaclass scans class attributes for `Page` instances and populates `cls._pages`. Every Page must have a `route`.

### Page (page.py)
```python
class HomePage(Page):
    title = "Home"
    route = "/"
    layout = "default"       # "default" | "full-width" | "sidebar" | "auth"

    def compose(self):       # declarative style — preferred
        with Flex(direction="col"):
            Heading("Hello")
```

Or imperative style:
```python
home = Page(title="Home", route="/")
home.add(Heading("Hello"), Button("Click"))
```

`Page.layout` maps to `PAGE_LAYOUT_CLASSES` in `tailwind.py`:
- `"default"` → `container mx-auto px-4 py-8 max-w-7xl`
- `"full-width"` → `w-full` (no padding — use for full-bleed designs)
- `"sidebar"` → `flex gap-6 px-4 py-8 max-w-7xl mx-auto`
- `"auth"` → `min-h-screen flex items-center justify-center bg-gray-50 px-4`

---

## Web Renderer Details

### generator.py
- `_PAGE_TEMPLATE` — the full HTML shell. Includes: Tailwind CDN + custom config (animations, keyframes, brand color), tailwindcss-animate plugin, Alpine.js, Inter font (weights 300–900), Lucide icons, Marked.js, Chart.js.
- `_render_node(node)` — main dispatch function. After calling the specific renderer, it also:
  - Injects `x-model` + `@input` for reactive input components
  - Injects `x-show` / `x-bind:disabled` for reactive `hidden`/`disabled` props
  - Appends custom `className()` classes
- `render_component(component)` — public helper, builds IR node and renders to HTML fragment
- `render_page(page, theme)` — public helper, builds IR page and renders to full HTML
- `WebGenerator(ir_tree).write_to_disk(output_dir)` — for `pyui build`

### tailwind.py
Pure functions mapping component props → Tailwind class strings. No side effects. Pattern:
```python
def button_classes(variant, size, disabled) -> str: ...
def flex_classes(direction, align, justify, gap, wrap) -> str: ...
```

### Custom CSS in the Page Template
The template includes these utility classes (added in Phase 3 / portfolio work):
- `.animate-on-scroll` + `.is-visible` — IntersectionObserver-driven scroll animations
- `.stagger-1` through `.stagger-6` — transition-delay utilities
- `.tilt-card` — 3D hover tilt effect
- `.gradient-text` — animated gradient text
- `.marquee-container` / `.marquee-content` — infinite scroll marquee
- `.magnetic-btn` — smooth transform transition for magnetic button effect
- `.theme-transition` — smooth color transitions on theme change

### RawHTML Component
`RawHTML(html_string)` — escape hatch for injecting arbitrary HTML/CSS/JS. Also available as `Text("").inject_html(html_string)`. The renderer outputs the string unescaped. **XSS risk — only use with trusted content.**

---

## CLI

Entry point: `pyui` → `src/pyui/cli/main.py:main` (Click group)

| Command | Status | Notes |
|---|---|---|
| `pyui new <name>` | ✅ Working | Scaffold with blank/dashboard/landing/admin/auth templates |
| `pyui run [app.py]` | ✅ Working | web (dev server + hot reload), desktop (tkinter), cli (Rich) |
| `pyui build [app.py]` | ✅ Working | web → HTML/CSS/JS; desktop/cli → run.py launcher |
| `pyui storybook` | ✅ Working | Component gallery on port 9000 |
| `pyui doctor` | ✅ Working | Python, deps, ports, PyPI version check |
| `pyui lint [app.py]` | ✅ Working | Missing alt, empty pages, duplicate routes, bad variants |
| `pyui search <query>` | ✅ Working | Searches PyPI for pyui-* packages |
| `pyui publish` | 🚧 Stub | Phase 5 — not yet implemented |
| `pyui info` | ✅ Working | Version info panel |

`pyui run` options: `--port`, `--host`, `--no-browser`, `--target` (web/desktop/cli)

---

## Theme System

Themes are flat token dicts. `DEFAULT_TOKENS` defines the base. Built-in themes override specific keys:

```python
BUILT_IN_THEMES = {
    "light": {},           # uses DEFAULT_TOKENS as-is
    "dark": DARK_OVERRIDES,
    "ocean": OCEAN_OVERRIDES,
    "sunset": SUNSET_OVERRIDES,
    "forest": FOREST_OVERRIDES,
    "rose": ROSE_OVERRIDES,
}
```

`_build_tokens(theme)` in `generator.py` merges DEFAULT_TOKENS + overrides → `_tokens_to_css_vars()` renders them as CSS `--pyui-*` variables in `:root`.

Custom theme: `App.theme = {"color.primary": "#FF0000", ...}` — any key from DEFAULT_TOKENS can be overridden.

---

## Dev Server Internals

- **Routes:** `POST /pyui-api/event/{handler_id}`, `GET /pyui-api/ws`, `GET /{path:.*}`
- **Event flow:** browser click → POST → `get_handler(id)` → call Python fn → re-run `build_ir_tree()` → collect node updates → return JSON
- **Special handler `update_state`:** used by `x-model` inputs to directly set ReactiveVar values without a Python handler
- **Hot reload:** WebSocket endpoint exists but only sends `{"type": "connected"}`. Full hot-reload is Phase 6.
- **SPA fallback:** any unmatched route falls back to `/`

---

## Testing

```bash
pytest                          # all tests
pytest tests/test_compiler/     # compiler unit tests
pytest tests/test_renderers/    # renderer unit tests
pytest -k "not e2e"             # skip playwright tests
pytest --cov=pyui               # with coverage
```

- `conftest.py` has an `autouse` fixture that resets the global `store` between every test
- E2E tests require Playwright and are marked `@pytest.mark.e2e`
- `asyncio_mode = "auto"` in pyproject.toml — async tests work without decorators

---

## Code Style & Tooling

```bash
ruff check src/ tests/          # lint
ruff format src/ tests/         # format
mypy src/                       # type check (strict mode)
pre-commit run --all-files      # run all hooks
```

- Line length: 100
- Target: Python 3.10
- Ruff rules: E, F, I, UP, B, SIM (E501 ignored)
- MyPy: strict, ignore_missing_imports = true
- Pre-commit: ruff, mypy, trailing whitespace, end-of-file fixer

---

## Running the Demos

```bash
# Basic demo app
python app.py
# or
pyui run app.py
# → http://localhost:8000

# Cinematic portfolio demo (full-bleed, dark, animations)
python tests/portfolio.py
# → http://localhost:9010

# Reactive counter
python tests/counter_reactive.py

# Component gallery
pyui storybook
# → http://localhost:9000
```

---

## Phase Roadmap

| Phase | Name | Status |
|---|---|---|
| 0 | Project setup & foundations | ✅ Complete |
| 1 | Core compiler (web target) | ✅ Complete |
| 2 | Full component library (42+ components) + storybook | ✅ Complete |
| 3 | State & reactivity (ReactiveVar, computed, store, persistence, x-model) | ✅ Complete |
| 4 | Desktop (tkinter) & CLI (Rich) renderers | ✅ Complete |
| 5 | Theme engine & plugin system | ✅ Complete |
| 6 | Hot reload, linter, scaffold, doctor, dev tools panel | ✅ Complete |
| 7 | Production hardening, error codes, security, example apps | ✅ Complete |
| 8 | Public launch — v1.0.0 | ✅ Complete |

---

## Phase 4 — What Needs to Be Built

Phase 4 adds two new render targets. The IR pipeline already exists — we just need new renderers.

### Desktop Renderer (tkinter or PyQt6)
- New file: `src/pyui/renderers/desktop/generator.py`
- Consumes `IRTree` → creates native widgets
- `pyui run --target desktop` should open a native window
- tkinter is the default (zero extra deps), PyQt6 is optional (`pip install pyui-framework[qt]`)
- Map component types to tkinter widgets: `button→tk.Button`, `text→tk.Label`, `flex→tk.Frame`, etc.
- Reactivity: subscribe to `ReactiveVar` changes and call widget `.config()` to update

### CLI / TUI Renderer (Rich)
- New file: `src/pyui/renderers/cli/generator.py`
- Consumes `IRTree` → Rich renderables / Layout
- `pyui run --target cli` should render in the terminal
- Use `rich.layout.Layout` for Flex/Grid, `rich.panel.Panel` for containers, `rich.table.Table` for Table, etc.
- Interactivity via `prompt_toolkit` (already in spirit of the project)

### CLI Changes Needed
- `src/pyui/cli/main.py` `cmd_run`: remove the "only web" guard, add desktop/cli dispatch
- `src/pyui/compiler/__init__.py`: add `compile_app()` routing for new targets

### Key Files to Create for Phase 4
```
src/pyui/renderers/desktop/__init__.py
src/pyui/renderers/desktop/generator.py    # tkinter renderer
src/pyui/renderers/cli/__init__.py
src/pyui/renderers/cli/generator.py        # Rich TUI renderer
```

---

## Known Gaps & Things to Watch Out For

- `pyui publish` is a stub — marketplace publishing not implemented yet (Phase 5 remainder)
- VS Code extension — Phase 6 stretch goal, not built
- `pyui build --target all` — routes to web only; desktop/cli each need separate build calls
- Hot reload re-imports the module on every file change — if the app has side effects on import, they will re-run
- `Text.inject_html()` and `RawHTML` bypass XSS protection — document clearly
- `REACTIVE_VAR_REGISTRY` is a module-level dict — not thread-safe for multi-user servers (fine for dev server)
- `_handler_registry` in `ir.py` is also module-level — same caveat
- `discover_app()` mutates `sys.path` — fine for CLI use, not for library use
- Multiple App subclasses in one file: only the first is used (warns but doesn't error)
- `Page.compose()` clears `page.children` before each call to prevent duplication on hot-reload

---

## Dependencies

### Runtime
| Package | Purpose |
|---|---|
| `click>=8.1` | CLI framework |
| `jinja2>=3.1` | Template engine (used in build output) |
| `aiohttp>=3.9` | Async HTTP dev server |
| `watchdog>=3.0` | File watching (hot reload, Phase 6) |
| `rich>=13.0` | Terminal output, CLI renderer |
| `structlog>=24.0` | Structured logging |
| `typing-extensions>=4.9` | Backports for Python 3.10 |

### Optional
| Extra | Package | Purpose |
|---|---|---|
| `[qt]` | `PyQt6` | Desktop renderer (Phase 4) |
| `[images]` | `Pillow` | Image processing |
| `[e2e]` | `playwright`, `pytest-playwright` | E2E browser tests |

### Dev
`pytest`, `pytest-cov`, `pytest-asyncio`, `ruff`, `mypy`, `pre-commit`, `hatch`

---

## Git Workflow

- Main branch: `main`
- PR target: `dev` (when it exists)
- Branch naming: `feat/description`, `fix/description`
- Pre-commit hooks required before committing
- Commit style: `feat:`, `fix:`, `chore:`, `docs:` prefixes
