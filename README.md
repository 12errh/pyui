# PyUI

> **Write Python. Render anywhere.**  
> Web · Desktop · Terminal — from a single Python codebase.

[![PyPI](https://img.shields.io/pypi/v/pyui-framework)](https://pypi.org/project/pyui-framework)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Tests](https://github.com/12errh/pyui/actions/workflows/test.yml/badge.svg)](https://github.com/12errh/pyui/actions)

PyUI is a production-ready Python UI framework. Write your entire UI in pure Python — no HTML, no CSS, no JavaScript. One codebase compiles to a web app, a native desktop window, and a terminal UI.

---

## Install

```bash
pip install pyui-framework
```

Requires Python 3.10+.

---

## Quick start

```bash
pyui new my-app
cd my-app
pyui run          # → http://localhost:8000
```

Or scaffold a dashboard:

```bash
pyui new my-dash --template dashboard
cd my-dash
pyui run
```

---

## Hello World

```python
from pyui import App, Button, Flex, Heading, Page, Text, reactive

class HomePage(Page):
    title = "Home"
    route = "/"

    def compose(self):
        with Flex(direction="col", align="center", gap=6):
            Heading("Hello from PyUI", level=1)
            Text("Built with pure Python.").style("muted")
            Button("Get Started").style("primary").size("lg")

class MyApp(App):
    name = "My App"
    home = HomePage()
```

Run it:

```bash
pyui run app.py                    # web browser
pyui run app.py --target desktop   # native window
pyui run app.py --target cli       # terminal
```

---

## Reactive state

```python
from pyui import App, Button, Flex, Page, Text, reactive

_count = reactive(0)

class CounterPage(Page):
    title = "Counter"
    route = "/"

    def compose(self):
        with Flex(direction="col", align="center", gap=4):
            Text(lambda: f"Count: {_count.get()}").style("lead")
            with Flex(gap=3):
                Button("−").style("ghost").onClick(lambda: _count.set(_count.get() - 1))
                Button("+").style("primary").onClick(lambda: _count.set(_count.get() + 1))

class CounterApp(App):
    count = _count
    home = CounterPage()
```

---

## 42+ built-in components

| Category | Components |
|---|---|
| Layout | `Flex`, `Grid`, `Stack`, `Container`, `Sidebar`, `Split`, `Divider`, `Spacer`, `List` |
| Display | `Text`, `Heading`, `Badge`, `Tag`, `Avatar`, `Icon`, `Image`, `Markdown`, `Video` |
| Input | `Button`, `Input`, `Textarea`, `Select`, `Checkbox`, `Radio`, `Toggle`, `Slider`, `DatePicker`, `FilePicker`, `Form` |
| Feedback | `Alert`, `Toast`, `Modal`, `Drawer`, `Tooltip`, `Progress`, `Spinner`, `Skeleton` |
| Navigation | `Nav`, `Tabs`, `Breadcrumb`, `Pagination`, `Menu` |
| Data | `Table`, `Stat`, `Chart` |

---

## 6 built-in themes

```python
class MyApp(App):
    theme = "dark"   # light · dark · ocean · sunset · forest · rose
```

Custom theme:

```python
class MyApp(App):
    theme = {"color.primary": "#FF6B6B", "color.background": "#FFF5F5"}
```

---

## CLI reference

| Command | Description |
|---|---|
| `pyui new <name>` | Scaffold a new project (`--template blank\|dashboard\|landing\|admin\|auth`) |
| `pyui run [app.py]` | Start dev server with hot reload (`--target web\|desktop\|cli`) |
| `pyui build [app.py]` | Production build (`--target web\|desktop\|cli\|all`) |
| `pyui storybook` | Open component gallery |
| `pyui doctor` | Check environment health |
| `pyui lint [app.py]` | Lint component definitions |
| `pyui search <query>` | Search PyPI for `pyui-*` packages |
| `pyui publish` | Publish a component package to PyPI |
| `pyui info` | Show version info |

---

## Plugin system

```python
from pyui.plugins import PyUIPlugin, register_component

class ChartsPlugin(PyUIPlugin):
    name = "pyui-charts"
    version = "1.0.0"

    def on_load(self, app):
        register_component("LineChart", LineChartComponent)

class MyApp(App):
    plugins = [ChartsPlugin()]
```

---

## Example apps

Five full example apps are in [`examples/`](examples/):

| App | Description |
|---|---|
| [`dashboard/`](examples/dashboard/app.py) | Analytics dashboard with stats, chart, table |
| [`todo/`](examples/todo/app.py) | Reactive todo list |
| [`blog/`](examples/blog/app.py) | Content site with routing |
| [`ml-demo/`](examples/ml-demo/app.py) | ML inference UI |
| [`admin/`](examples/admin/app.py) | CRUD admin panel |

Run any example:

```bash
pyui run examples/dashboard/app.py
```

---

## What's included

- ✅ Web renderer (HTML + Tailwind CSS + Alpine.js)
- ✅ Desktop renderer (tkinter, optional sv-ttk)
- ✅ CLI renderer (Rich TUI)
- ✅ Reactive state (`reactive`, `computed`, `store`)
- ✅ Theme engine (6 built-in themes + custom tokens + Figma export)
- ✅ Plugin system with lifecycle hooks
- ✅ Hot reload (file save → browser update)
- ✅ Dev tools panel (state inspector, event log)
- ✅ Error overlay with structured error codes (`PYUI-NNN`)
- ✅ `pyui lint` — component tree validation
- ✅ `pyui doctor` — environment health check
- ✅ `pyui publish` — marketplace publishing via PyPI

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Issues labelled [`good-first-issue`](https://github.com/12errh/pyui/issues?q=label%3Agood-first-issue) are a great place to start.

## License

MIT — see [LICENSE](LICENSE).
