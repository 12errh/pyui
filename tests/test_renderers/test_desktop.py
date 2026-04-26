"""
Phase 4 — Desktop renderer (tkinter) tests.

Tests focus on the dispatch table, IR building, and renderer instantiation.
Widget construction tests use mocks to avoid requiring a display.
"""

from __future__ import annotations

from unittest.mock import MagicMock, patch


# ── Dispatch table ────────────────────────────────────────────────────────────


def test_widget_builders_cover_all_core_types() -> None:
    """Every core component type must have an entry in _WIDGET_BUILDERS."""
    from pyui.renderers.desktop.tkinter_renderer import _WIDGET_BUILDERS

    required = [
        "button", "text", "heading", "grid", "flex", "stack",
        "container", "divider", "spacer", "input", "textarea",
        "select", "checkbox", "toggle", "slider", "badge", "tag",
        "avatar", "alert", "progress", "spinner", "skeleton",
        "table", "stat", "nav", "tabs", "form",
    ]
    for t in required:
        assert t in _WIDGET_BUILDERS, f"Missing widget builder for type: {t}"


# ── TkinterRenderer (no display needed) ──────────────────────────────────────


def test_tkinter_renderer_instantiates() -> None:
    """TkinterRenderer must build an IRTree without touching the display."""
    from pyui import App, Button, Page
    from pyui.renderers.desktop.tkinter_renderer import TkinterRenderer

    class SampleApp(App):
        name = "Test"
        home = Page(title="Home", route="/")
        home.add(Button("Go"))

    renderer = TkinterRenderer(SampleApp)
    assert renderer._ir_tree is not None
    assert len(renderer._ir_tree.pages) == 1


def test_tkinter_renderer_multi_page() -> None:
    """TkinterRenderer must handle multi-page apps."""
    from pyui import App, Page, Text
    from pyui.renderers.desktop.tkinter_renderer import TkinterRenderer

    class MultiApp(App):
        home = Page(title="Home", route="/")
        home.add(Text("Welcome"))
        about = Page(title="About", route="/about")
        about.add(Text("About us"))

    renderer = TkinterRenderer(MultiApp)
    assert len(renderer._ir_tree.pages) == 2


# ── build_widget with mocked tkinter ─────────────────────────────────────────


def _mock_parent() -> MagicMock:
    parent = MagicMock()
    parent.tk = MagicMock()
    parent._w = "."
    return parent


def test_build_widget_button_with_mock() -> None:
    """build_widget for a button must call the button builder."""
    with patch("tkinter.Button") as mock_btn:
        mock_btn.return_value = MagicMock()
        from pyui import Button
        from pyui.compiler.ir import build_ir_node
        from pyui.renderers.desktop.tkinter_renderer import build_widget

        node = build_ir_node(Button("Save").style("primary"))
        parent = _mock_parent()
        widget = build_widget(node, parent)
        assert widget is not None


def test_build_widget_text_with_mock() -> None:
    """build_widget for a text node must call the text builder."""
    with patch("tkinter.Label") as mock_lbl:
        mock_lbl.return_value = MagicMock()
        from pyui import Text
        from pyui.compiler.ir import build_ir_node
        from pyui.renderers.desktop.tkinter_renderer import build_widget

        node = build_ir_node(Text("Hello"))
        parent = _mock_parent()
        widget = build_widget(node, parent)
        assert widget is not None


def test_build_widget_unknown_type_returns_label() -> None:
    """build_widget must return a fallback Label for unknown component types."""
    with patch("tkinter.Label") as mock_lbl:
        mock_lbl.return_value = MagicMock()
        from pyui.compiler.ir import IRNode
        from pyui.renderers.desktop.tkinter_renderer import build_widget

        unknown_node = IRNode(
            type="nonexistent_type",
            props={},
            children=[],
            events={},
            reactive_bindings=[],
            reactive_props={},
            style_variant=None,
            theme_tokens={},
        )
        parent = _mock_parent()
        widget = build_widget(unknown_node, parent)
        assert widget is not None


def test_build_widget_heading_with_mock() -> None:
    """build_widget for a heading must return a Frame."""
    with patch("tkinter.Frame") as mock_frame, patch("tkinter.Label"):
        mock_frame.return_value = MagicMock()
        from pyui import Heading
        from pyui.compiler.ir import build_ir_node
        from pyui.renderers.desktop.tkinter_renderer import build_widget

        node = build_ir_node(Heading("Title", level=2))
        parent = _mock_parent()
        widget = build_widget(node, parent)
        assert widget is not None


def test_build_widget_alert_with_mock() -> None:
    """build_widget for an alert must return a Frame."""
    with patch("tkinter.Frame") as mock_frame, patch("tkinter.Label"):
        mock_frame.return_value = MagicMock()
        from pyui import Alert
        from pyui.compiler.ir import build_ir_node
        from pyui.renderers.desktop.tkinter_renderer import build_widget

        node = build_ir_node(Alert("Warning", "Something went wrong", variant="danger"))
        parent = _mock_parent()
        widget = build_widget(node, parent)
        assert widget is not None


def test_build_widget_stat_with_mock() -> None:
    """build_widget for a stat must return a Frame."""
    with patch("tkinter.Frame") as mock_frame, patch("tkinter.Label"):
        mock_frame.return_value = MagicMock()
        from pyui import Stat
        from pyui.compiler.ir import build_ir_node
        from pyui.renderers.desktop.tkinter_renderer import build_widget

        node = build_ir_node(Stat(label="Revenue", value="$12,000", trend="+12%", trend_up=True))
        parent = _mock_parent()
        widget = build_widget(node, parent)
        assert widget is not None


def test_build_widget_table_with_mock() -> None:
    """build_widget for a table must return a Frame."""
    with patch("tkinter.Frame") as mock_frame, \
         patch("tkinter.ttk.Treeview"), patch("tkinter.ttk.Scrollbar"):
        mock_frame.return_value = MagicMock()
        from pyui import Table
        from pyui.compiler.ir import build_ir_node
        from pyui.renderers.desktop.tkinter_renderer import build_widget

        node = build_ir_node(Table(headers=["Name", "Age"], rows=[["Alice", "30"]]))
        parent = _mock_parent()
        widget = build_widget(node, parent)
        assert widget is not None
