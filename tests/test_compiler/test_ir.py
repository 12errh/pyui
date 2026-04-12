"""
Phase 1 — IR builder tests.

Tests from the PyUI spec Section 5, Phase 1.
"""

from __future__ import annotations


def test_button_produces_ir_node() -> None:
    """Button IRNode must have type='button', correct label, and style_variant."""
    from pyui import Button
    from pyui.compiler.ir import build_ir_node

    btn = Button("Click me").style("primary")
    node = build_ir_node(btn)
    assert node.type == "button"
    assert node.props["label"] == "Click me"
    assert node.style_variant == "primary"


def test_grid_children_in_ir() -> None:
    """Grid IRNode must have N children matching the components added."""
    from pyui import Button, Grid, Text
    from pyui.compiler.ir import build_ir_node

    grid = Grid(cols=3).add(Button("A"), Button("B"), Text("Hello"))
    node = build_ir_node(grid)
    assert len(node.children) == 3
    assert node.props["cols"] == 3


def test_event_handler_registered() -> None:
    """Button.onClick() must register the handler in IRNode.events['click']."""
    from pyui import Button
    from pyui.compiler.ir import build_ir_node

    def handler() -> None:
        return None

    btn = Button("Go").onClick(handler)
    node = build_ir_node(btn)
    assert "click" in node.events


def test_text_reactive_lambda_resolved() -> None:
    """Text with a lambda content must resolve to a string in props."""
    from pyui import Text
    from pyui.compiler.ir import build_ir_node

    t = Text(lambda: "resolved value")
    node = build_ir_node(t)
    # Callable resolved at compile time
    assert node.props["content"] == "resolved value"
    assert node.props["is_reactive"] is True
    assert "content" in node.reactive_bindings


def test_heading_ir_level() -> None:
    """Heading IRNode must carry the correct level prop."""
    from pyui import Heading
    from pyui.compiler.ir import build_ir_node

    h = Heading("Hello", level=3)
    node = build_ir_node(h)
    assert node.type == "heading"
    assert node.props["level"] == 3
    assert node.props["text"] == "Hello"


def test_nested_children_recursion() -> None:
    """build_ir_node must recurse into nested children."""
    from pyui import Button, Grid, Text
    from pyui.compiler.ir import build_ir_node

    grid = Grid(cols=2).add(
        Button("A"),
        Grid(cols=1).add(Text("nested")),
    )
    node = build_ir_node(grid)
    assert len(node.children) == 2
    inner_grid = node.children[1]
    assert inner_grid.type == "grid"
    assert len(inner_grid.children) == 1
    assert inner_grid.children[0].type == "text"


def test_build_ir_page() -> None:
    """build_ir_page must produce an IRPage with correct route and children."""
    from pyui import Button, Page, Text
    from pyui.compiler.ir import build_ir_page

    p = Page(title="My Page", route="/test")
    p.add(Button("Go"), Text("Hello"))
    ir_p = build_ir_page(p)
    assert ir_p.route == "/test"
    assert ir_p.title == "My Page"
    assert len(ir_p.children) == 2


def test_build_ir_tree() -> None:
    """build_ir_tree must produce an IRTree with all App pages."""
    from pyui import App, Button, Page
    from pyui.compiler.ir import build_ir_tree

    class SampleApp(App):
        name = "Sample"
        home = Page(title="Home", route="/")
        home.add(Button("Go"))

        about = Page(title="About", route="/about")

    tree = build_ir_tree(SampleApp)
    assert tree.app_meta["name"] == "Sample"
    routes = [p.route for p in tree.pages]
    assert "/" in routes
    assert "/about" in routes


def test_ir_node_has_unique_id() -> None:
    """Each IRNode should have a unique node_id."""
    from pyui import Button
    from pyui.compiler.ir import build_ir_node

    n1 = build_ir_node(Button("A"))
    n2 = build_ir_node(Button("B"))
    assert n1.node_id != n2.node_id


def test_multiple_event_handlers() -> None:
    """A component can register both onClick and onChange."""
    from pyui import Button
    from pyui.compiler.ir import build_ir_node

    btn = Button("X").onClick(lambda: None).onChange(lambda: None)
    node = build_ir_node(btn)
    assert "click" in node.events
    assert "change" in node.events
