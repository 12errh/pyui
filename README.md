# PyUI

> **Write Python. Render anywhere.**  
> Web browser · Desktop window · Terminal UI — from a single Python codebase.

[![PyPI](https://img.shields.io/pypi/v/pyui-framework)](https://pypi.org/project/pyui-framework)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

PyUI is a modern, reactive UI framework that lets you build production-ready interfaces using pure Python. It compiles your code into an Intermediate Representation (IR) that can be rendered to HTML/Tailwind, native desktop widgets (Qt), or rich terminal output.

## Features

- **42+ Essential Components**: Full set of inputs, navigation, feedback, and data visualization tools.
- **Declarative Style**: Clean, context-managed UI composition using the `with` statement.
- **Pure Python Reactivity**: State management that feels like standard Python, powered by a sophisticated reactive engine.
- **Production-Ready Visuals**: Seamless integration with Tailwind CSS and Lucide Icons.
- **Storybook CLI**: Instant component gallery for development and testing.

## Quick Start

```bash
pip install pyui-framework
pyui new my-app
cd my-app
pyui storybook       # → Explore the component gallery
```

## Example

```python
from pyui import App, Page, Heading, Text, Flex, Button, reactive

class MyApp(App):
    count = reactive(0)

class HomePage(Page):
    title = "Home"
    route = "/"

    def compose(self):
        with Flex(direction="col", gap=6).padding(10):
            Heading("Welcome to PyUI", subtitle="Built with pure Python")
            Text(lambda: f"Current count: {MyApp.count.get()}")
            
            with Flex(gap=4):
                Button("Increment").style("primary").onClick(
                    lambda: MyApp.count.set(MyApp.count.get() + 1)
                )
                Button("Reset").style("ghost").onClick(
                    lambda: MyApp.count.set(0)
                )

class StoryApp(App):
    index = HomePage()
```

## Status

✅ **Phase 0 & 1** (Foundations & Layout) - Complete  
✅ **Phase 2** (Full Component Library) - Complete  
🚧 **Phase 3** (Client-Side Reactivity) - In Progress  

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT — see [LICENSE](LICENSE).
