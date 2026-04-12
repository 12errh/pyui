"""
Demo app for Phase 1 — used to test `pyui run --web` manually.

Run with: pyui run app.py
"""

from pyui import App, Button, Grid, Heading, Page, Text, reactive


class DemoApp(App):
    name = "PyUI Demo"
    description = "Phase 1 demo — Button, Text, Heading, Grid"
    theme = "light"

    # Reactive counter (persists as a class attribute between requests)
    count = reactive(0)

    # ── Home page ─────────────────────────────────────────────────────────────
    home = Page(title="PyUI Demo", route="/")
    home.add(
        Heading("Hello from PyUI!", level=1).style("gradient"),
        Heading("The Python UI Framework", level=2),
        Text("Write Python. Render anywhere — Web, Desktop, and CLI.").paragraph(),
        Text(lambda: f"Button clicked {DemoApp.count.get()} times").paragraph().style("muted"),
        Grid(cols=3, gap=4).add(
            Button("Primary")
            .style("primary")
            .onClick(lambda: DemoApp.count.set(DemoApp.count.get() + 1)),
            Button("Ghost").style("ghost"),
            Button("Danger").style("danger"),
        ),
        Heading("Component Grid", level=2),
        Grid(cols=2, gap=6).add(
            Text("Fast — Compiles to native code").paragraph(),
            Text("Beautiful — Gorgeous by default").paragraph(),
            Text("Simple — Pure Python").paragraph(),
            Text("Reactive — State updates instantly").paragraph(),
        ),
    )

    # ── About page ────────────────────────────────────────────────────────────
    about = Page(title="About — PyUI Demo", route="/about")
    about.add(
        Heading("About PyUI", level=1),
        Text(
            "PyUI is an open-source Python framework for building production-grade UIs."
        ).paragraph(),
        Button("Back to Home").style("ghost"),
    )
