---
inclusion: always
---

# Zolt — AI Agent Context

Zolt is a production-ready Python UI framework. Install: `pip install zolt`. CLI: `zolt`.

## Core concept

Write your entire UI in pure Python. One codebase compiles to three targets:
- **Web** — HTML + Tailwind CSS + Alpine.js (dev server with hot reload)
- **Desktop** — native tkinter window
- **CLI** — Rich TUI in the terminal

## Package structure

```
src/pyui/          ← import name is still `pyui` (from pyui import App)
├── app.py         ← App base class + AppMeta metaclass
├── page.py        ← Page class
├── exceptions.py  ← PyUIError hierarchy with PYUI-NNN error codes
├── linter.py      ← lint_app()
├── scaffold.py    ← create_project() for zolt new
├── components/    ← 42+ components (layout, display, input, feedback, nav, data, media)
├── compiler/      ← IR pipeline: build_ir_node → build_ir_page → build_ir_tree
├── renderers/     ← web/, desktop/, cli/
├── server/        ← aiohttp dev server with hot reload + WebSocket
├── state/         ← reactive.py, computed.py, store.py
├── theme/         ← engine.py (build_theme, tokens_to_css_vars, tokens_to_figma)
├── plugins/       ← PyUIPlugin base, registry, loader
├── hotreload/     ← FileWatcher, diff_ir
└── cli/           ← main.py (zolt command), storybook.py
```

## Minimal app

```python
from pyui import App, Button, Flex, Heading, Page, Text, reactive

_count = reactive(0)

class HomePage(Page):
    title = "Home"
    route = "/"

    def compose(self):
        with Flex(direction="col", align="center", gap=6):
            Heading("Hello from Zolt", level=1)
            Text(lambda: f"Count: {_count.get()}").style("muted")
            Button("+").style("primary").onClick(lambda: _count.set(_count.get() + 1))

class MyApp(App):
    name = "My App"
    count = _count
    home = HomePage()
```

Run: `zolt run app.py`

## CRITICAL: Page registration rule

Pages MUST be declared as class attributes inside the App class body.
`AppMeta` metaclass scans at class definition time — post-assignment does NOT work.

```python
# ✅ CORRECT
class MyApp(App):
    home = HomePage()   # registered at class creation

# ❌ WRONG — causes 404
class MyApp(App):
    home = None
MyApp.home = HomePage()  # too late, AppMeta already ran
```

## Reactive state pattern

Always define reactive vars at module level, then reference them in the App class:

```python
_count = reactive(0)          # module level

class MyApp(App):
    count = _count             # reference in App for IR registration
    home = CounterPage()
```

## Component API

All components use fluent chaining. Every method returns `self`:

```python
Button("Save").style("primary").size("lg").disabled(False).onClick(handler)
Text("Hello").style("muted").paragraph()
Grid(cols=3, gap=6).add(Card(...), Card(...), Card(...))
```

Style variants: `primary`, `secondary`, `ghost`, `danger`, `success`, `gradient`, `link`
Sizes: `xs`, `sm`, `md`, `lg`, `xl`

## Declarative composition (preferred)

```python
class MyPage(Page):
    def compose(self):
        with Flex(direction="col", gap=6):
            Heading("Title")          # auto-added to Flex
            with Grid(cols=2):
                Text("A")             # auto-added to Grid
                Text("B")
```

## Adding a new component — checklist

1. Create file in `src/pyui/components/<category>/`
2. Inherit from `BaseComponent`, set `component_type = "my_type"`
3. Export from category `__init__.py`
4. Export from `src/pyui/__init__.py` (import + `__all__`)
5. Add `"my_type": _render_my_type` to dispatch dict in `renderers/web/generator.py`
6. Add `_render_my_type(node: IRNode) -> str` in `generator.py`
7. Add widget builder in `renderers/desktop/tkinter_renderer.py`
8. Add renderer in `renderers/cli/generator.py`

## Theme system

```python
class MyApp(App):
    theme = "dark"   # light · dark · ocean · sunset · forest · rose

# Custom tokens
class MyApp(App):
    theme = {"color.primary": "#FF6B6B", "color.background": "#FFF5F5"}
```

Built-in themes: `light`, `dark`, `ocean`, `sunset`, `forest`, `rose`

Runtime swap: `POST /pyui-api/theme/{name}` → returns CSS vars

## Plugin system

```python
from pyui.plugins import PyUIPlugin, register_component

class MyPlugin(PyUIPlugin):
    name = "zolt-charts"
    version = "1.0.0"

    def on_load(self, app):
        register_component("LineChart", LineChartComponent)

class MyApp(App):
    plugins = [MyPlugin()]
```

Lifecycle hooks: `on_load`, `on_compile_start`, `on_compile_end`, `on_build`, `on_dev_start`

## Error codes

All exceptions carry `PYUI-NNN` codes:
- `PYUI-002` AppNotFoundError — no App subclass in file
- `PYUI-003` ModuleImportError — file can't be imported
- `PYUI-004` MissingRouteError — Page missing `route=`
- `PYUI-201` UnknownThemeError — unknown theme name
- `PYUI-301` PluginConflictError — duplicate component registration

## CLI commands

```bash
zolt new <name>              # scaffold project (--template blank|dashboard|landing|admin|auth)
zolt run [app.py]            # dev server with hot reload (--target web|desktop|cli)
zolt build [app.py]          # production build (--target web|desktop|cli|all)
zolt storybook               # component gallery on port 9000
zolt doctor                  # environment health check
zolt lint [app.py]           # validate component trees
zolt search <query>          # search PyPI for zolt-* packages
zolt publish                 # publish component package (requires pyui.json)
zolt info                    # version info
```

## Dev server endpoints

- `GET /{path}` — serve HTML page
- `POST /pyui-api/event/{handler_id}` — invoke Python event handler
- `POST /pyui-api/theme/{name}` — hot-swap theme
- `GET /pyui-api/ws` — WebSocket for hot reload
- `GET /pyui-api/devtools/state` — reactive state snapshot

## Key files

| File | Purpose |
|---|---|
| `src/pyui/__init__.py` | Public API, `__version__ = "1.1.0"` |
| `src/pyui/compiler/ir.py` | `build_ir_tree(AppClass)` → IRTree |
| `src/pyui/renderers/web/generator.py` | IRTree → HTML/CSS/JS |
| `src/pyui/server/dev_server.py` | aiohttp server, hot reload, security middleware |
| `src/pyui/theme/engine.py` | `build_theme()`, `tokens_to_css_vars()`, `tokens_to_figma()` |
| `src/pyui/hotreload/watcher.py` | `FileWatcher` — watchdog-based file watcher |
| `src/pyui/hotreload/diff.py` | `diff_ir()` — minimal IR patch generation |
| `src/pyui/linter.py` | `lint_app()` — component tree validation |
| `src/pyui/scaffold.py` | `create_project()` — zolt new templates |

## Testing

```bash
pytest                          # all 243 tests
pytest tests/test_compiler/     # compiler unit tests
pytest tests/test_renderers/    # renderer tests
pytest tests/integration/       # end-to-end pipeline tests
```

## Known constraints

- Import name is `pyui` (not `zolt`) — `from pyui import App` — this is intentional
- `AppMeta` runs at class definition time — pages must be in the class body
- `REACTIVE_VAR_REGISTRY` is module-level — not thread-safe for multi-user servers
- Hot reload re-imports the module on every file change
- `RawHTML` / `Text.inject_html()` bypass XSS protection — only use with trusted content
