"""
Phase 4 — CLI renderer (Rich) tests.
"""

from __future__ import annotations


# ── render_node ───────────────────────────────────────────────────────────────


def test_render_button_returns_renderable() -> None:
    """render_node on a button IRNode must return a non-None Rich renderable."""
    from pyui import Button
    from pyui.compiler.ir import build_ir_node
    from pyui.renderers.cli.generator import render_node

    node = build_ir_node(Button("Click me").style("primary"))
    result = render_node(node)
    assert result is not None


def test_render_text_returns_renderable() -> None:
    """render_node on a text IRNode must return a Rich Text object."""
    from rich.text import Text as RichText

    from pyui import Text
    from pyui.compiler.ir import build_ir_node
    from pyui.renderers.cli.generator import render_node

    node = build_ir_node(Text("Hello CLI"))
    result = render_node(node)
    assert result is not None
    assert isinstance(result, RichText)


def test_render_text_content_preserved() -> None:
    """The rendered text must contain the original content string."""
    from rich.text import Text as RichText

    from pyui import Text
    from pyui.compiler.ir import build_ir_node
    from pyui.renderers.cli.generator import render_node

    node = build_ir_node(Text("Hello World"))
    result = render_node(node)
    assert isinstance(result, RichText)
    assert "Hello World" in result.plain


def test_render_heading_returns_renderable() -> None:
    """render_node on a heading IRNode must return a non-None renderable."""
    from pyui import Heading
    from pyui.compiler.ir import build_ir_node
    from pyui.renderers.cli.generator import render_node

    node = build_ir_node(Heading("Section Title", level=2))
    result = render_node(node)
    assert result is not None


def test_render_grid_returns_renderable() -> None:
    """render_node on a grid IRNode must return a non-None renderable."""
    from pyui import Grid, Text
    from pyui.compiler.ir import build_ir_node
    from pyui.renderers.cli.generator import render_node

    node = build_ir_node(Grid(cols=2).add(Text("A"), Text("B")))
    result = render_node(node)
    assert result is not None


def test_render_alert_returns_panel() -> None:
    """render_node on an alert IRNode must return a Rich Panel."""
    from rich.panel import Panel

    from pyui import Alert
    from pyui.compiler.ir import build_ir_node
    from pyui.renderers.cli.generator import render_node

    node = build_ir_node(Alert("Error", "Something failed", variant="danger"))
    result = render_node(node)
    assert isinstance(result, Panel)


def test_render_table_returns_rich_table() -> None:
    """render_node on a table IRNode must return a Rich Table."""
    from rich.table import Table as RichTable

    from pyui import Table
    from pyui.compiler.ir import build_ir_node
    from pyui.renderers.cli.generator import render_node

    node = build_ir_node(
        Table(headers=["Name", "Score"], rows=[["Alice", "95"], ["Bob", "87"]])
    )
    result = render_node(node)
    assert isinstance(result, RichTable)


def test_render_stat_returns_panel() -> None:
    """render_node on a stat IRNode must return a Rich Panel."""
    from rich.panel import Panel

    from pyui import Stat
    from pyui.compiler.ir import build_ir_node
    from pyui.renderers.cli.generator import render_node

    node = build_ir_node(Stat(label="Users", value="1,234", trend="+5%", trend_up=True))
    result = render_node(node)
    assert isinstance(result, Panel)


def test_render_unknown_type_returns_text() -> None:
    """render_node on an unknown type must return a fallback Rich Text."""
    from rich.text import Text as RichText

    from pyui.compiler.ir import IRNode
    from pyui.renderers.cli.generator import render_node

    unknown = IRNode(
        type="totally_unknown",
        props={},
        children=[],
        events={},
        reactive_bindings=[],
        reactive_props={},
        style_variant=None,
        theme_tokens={},
    )
    result = render_node(unknown)
    assert isinstance(result, RichText)
    assert "totally_unknown" in result.plain


# ── render_to_rich ────────────────────────────────────────────────────────────


def test_render_to_rich_returns_panel() -> None:
    """render_to_rich must return a Rich Panel wrapping the page content."""
    from rich.panel import Panel

    from pyui import Button, Page, Text
    from pyui.compiler.ir import build_ir_page
    from pyui.renderers.cli.generator import render_to_rich

    page = Page(title="My Page", route="/")
    page.add(Text("Welcome"), Button("Go"))
    ir_page = build_ir_page(page)
    result = render_to_rich(ir_page)
    assert isinstance(result, Panel)


def test_render_to_rich_empty_page() -> None:
    """render_to_rich must handle an empty page without error."""
    from rich.panel import Panel

    from pyui import Page
    from pyui.compiler.ir import build_ir_page
    from pyui.renderers.cli.generator import render_to_rich

    page = Page(title="Empty", route="/empty")
    ir_page = build_ir_page(page)
    result = render_to_rich(ir_page)
    assert isinstance(result, Panel)


# ── CliRenderer ───────────────────────────────────────────────────────────────


def test_cli_renderer_instantiates() -> None:
    """CliRenderer must instantiate without error given a valid App."""
    from pyui import App, Button, Page
    from pyui.renderers.cli.generator import CliRenderer

    class SampleApp(App):
        name = "CLI Test"
        home = Page(title="Home", route="/")
        home.add(Button("Go"))

    renderer = CliRenderer(SampleApp)
    assert renderer._ir_tree is not None
    assert len(renderer._ir_tree.pages) == 1


def test_cli_renderer_collect_buttons() -> None:
    """_collect_buttons must find all buttons with click handlers."""
    from pyui import App, Button, Page
    from pyui.compiler.ir import build_ir_page
    from pyui.renderers.cli.generator import CliRenderer

    class SampleApp(App):
        home = Page(title="Home", route="/")
        home.add(
            Button("Action 1").onClick(lambda: None),
            Button("Action 2").onClick(lambda: None),
            Button("No handler"),
        )

    renderer = CliRenderer(SampleApp)
    ir_page = build_ir_page(SampleApp.home)
    buttons = renderer._collect_buttons(ir_page.children)
    assert len(buttons) == 2
    labels = [b[0] for b in buttons]
    assert "Action 1" in labels
    assert "Action 2" in labels


# ── All component types covered ───────────────────────────────────────────────


def test_all_renderers_registered() -> None:
    """Every core component type must have a CLI renderer registered."""
    from pyui.renderers.cli.generator import _RENDERERS

    required = [
        "button", "text", "heading", "grid", "flex", "stack",
        "container", "divider", "spacer", "badge", "tag", "avatar",
        "icon", "image", "markdown", "video", "input", "textarea",
        "select", "checkbox", "toggle", "slider", "form",
        "alert", "toast", "modal", "drawer", "tooltip",
        "progress", "spinner", "skeleton",
        "table", "stat", "chart",
        "nav", "tabs", "breadcrumb", "pagination", "menu",
        "list", "sidebar_layout",
    ]
    for t in required:
        assert t in _RENDERERS, f"Missing CLI renderer for type: {t}"
