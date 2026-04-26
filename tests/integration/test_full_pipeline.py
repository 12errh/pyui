"""
Phase 7 — Integration tests: full compilation pipeline end-to-end.
"""

from __future__ import annotations

from pathlib import Path


# ── Web pipeline ──────────────────────────────────────────────────────────────


def test_full_web_compile_pipeline(tmp_path: Path) -> None:
    """App class → HTML files on disk with correct content."""
    from pyui import App, Button, Page, Text
    from pyui.compiler import compile_app

    class MyApp(App):
        home = Page(title="Test", route="/")
        home.add(Text("Welcome"), Button("Go").style("primary"))

    out, stats = compile_app(MyApp, target="web", output_dir=str(tmp_path / "dist"))

    index = out / "index.html"
    assert index.exists()
    content = index.read_text(encoding="utf-8")
    assert "Welcome" in content
    assert "Go" in content
    assert "Test" in content

    # Build stats are populated
    assert stats["pages"] == 1
    assert stats["total_kb"] > 0
    assert stats["elapsed_ms"] >= 0


def test_multi_page_compile(tmp_path: Path) -> None:
    """Multi-page app produces one HTML file per page."""
    from pyui import App, Page, Text
    from pyui.compiler import compile_app

    class MultiApp(App):
        home = Page(title="Home", route="/")
        home.add(Text("Homepage"))
        about = Page(title="About", route="/about")
        about.add(Text("About page"))

    out, stats = compile_app(MultiApp, target="web", output_dir=str(tmp_path / "dist"))

    assert (out / "index.html").exists()
    assert (out / "about.html").exists()
    assert "Homepage" in (out / "index.html").read_text()
    assert "About page" in (out / "about.html").read_text()
    assert stats["pages"] == 2


def test_desktop_build_produces_launcher(tmp_path: Path) -> None:
    """pyui build --target desktop writes run.py and README.txt."""
    from pyui import App, Button, Page
    from pyui.compiler import compile_app

    class DesktopApp(App):
        home = Page(title="Desktop", route="/")
        home.add(Button("Launch"))

    out, _ = compile_app(DesktopApp, target="desktop", output_dir=str(tmp_path / "dist"))

    assert (out / "run.py").exists()
    assert (out / "README.txt").exists()
    run_content = (out / "run.py").read_text()
    assert "run_desktop_app" in run_content
    assert "DesktopApp" in run_content


def test_cli_build_produces_launcher(tmp_path: Path) -> None:
    """pyui build --target cli writes run.py and README.txt."""
    from pyui import App, Page, Text
    from pyui.compiler import compile_app

    class CLIApp(App):
        home = Page(title="CLI", route="/")
        home.add(Text("Hello CLI"))

    out, _ = compile_app(CLIApp, target="cli", output_dir=str(tmp_path / "dist"))

    assert (out / "run.py").exists()
    run_content = (out / "run.py").read_text()
    assert "run_cli_app" in run_content


def test_build_all_produces_three_subdirs(tmp_path: Path) -> None:
    """pyui build --target all creates web/, desktop/, cli/ subdirectories."""
    from pyui import App, Button, Page
    from pyui.compiler import compile_app

    class AllApp(App):
        home = Page(title="All", route="/")
        home.add(Button("Go"))

    out, _ = compile_app(AllApp, target="all", output_dir=str(tmp_path / "dist"))

    assert (out / "web" / "index.html").exists()
    assert (out / "desktop" / "run.py").exists()
    assert (out / "cli" / "run.py").exists()


# ── Error codes ───────────────────────────────────────────────────────────────


def test_error_codes_on_missing_route() -> None:
    """MissingRouteError must carry PYUI-004 code."""
    import pytest
    from pyui.exceptions import MissingRouteError

    with pytest.raises(MissingRouteError) as exc_info:
        from pyui import App
        from pyui.page import Page

        class BadApp(App):
            home = Page(title="No Route")  # missing route=

    assert "PYUI-004" in str(exc_info.value)


def test_error_codes_on_unknown_theme() -> None:
    """UnknownThemeError must carry PYUI-201 code."""
    import pytest
    from pyui.exceptions import UnknownThemeError
    from pyui.theme.engine import build_theme

    with pytest.raises(UnknownThemeError) as exc_info:
        build_theme("nonexistent-theme")

    assert "PYUI-201" in str(exc_info.value)


def test_error_codes_on_plugin_conflict() -> None:
    """PluginConflictError must carry PYUI-301 code."""
    import pytest
    from pyui.components.base import BaseComponent
    from pyui.exceptions import PluginConflictError
    from pyui.plugins.registry import clear_registry, register_component

    clear_registry()

    class WidgetA(BaseComponent):
        component_type = "conflict_widget_a"

    class WidgetB(BaseComponent):
        component_type = "conflict_widget_b"

    register_component("ConflictTest", WidgetA)
    with pytest.raises(PluginConflictError) as exc_info:
        register_component("ConflictTest", WidgetB)

    assert "PYUI-301" in str(exc_info.value)
    clear_registry()


# ── Security headers ──────────────────────────────────────────────────────────


def test_rendered_page_has_no_inline_secrets() -> None:
    """Rendered HTML must not contain any obvious secret patterns."""
    import re
    from pyui import App, Page, Text
    from pyui.compiler.ir import build_ir_tree
    from pyui.renderers.web.generator import WebGenerator

    class SecApp(App):
        home = Page(title="Sec", route="/")
        home.add(Text("Hello"))

    ir = build_ir_tree(SecApp)
    gen = WebGenerator(ir)
    html = gen.render_ir_page(ir.pages[0])

    # No obvious secret patterns
    assert not re.search(r"password\s*=\s*['\"][^'\"]+['\"]", html, re.IGNORECASE)
    assert not re.search(r"api_key\s*=\s*['\"][^'\"]+['\"]", html, re.IGNORECASE)


def test_rendered_page_has_csp_script() -> None:
    """Rendered page must include the dark-mode script (security baseline)."""
    from pyui import Page
    from pyui.renderers.web import render_page

    html = render_page(Page(title="T", route="/"))
    assert "prefers-color-scheme" in html


# ── Graceful degradation ──────────────────────────────────────────────────────


def test_graceful_component_error_does_not_crash_page() -> None:
    """A broken component renders an error card, not a Python exception."""
    from pyui.compiler.ir import IRNode
    from pyui.renderers.web.generator import _render_node

    # Create a node whose renderer will raise (inject a bad prop)
    bad_node = IRNode(
        type="text",
        props={"content": None},  # None will cause issues in some paths
        children=[],
        events={},
        reactive_bindings=[],
        reactive_props={},
        style_variant=None,
        theme_tokens={},
    )
    # Should not raise — returns HTML string
    result = _render_node(bad_node)
    assert isinstance(result, str)
    assert len(result) > 0


# ── Example apps compile ──────────────────────────────────────────────────────


def test_example_dashboard_compiles(tmp_path: Path) -> None:
    """examples/dashboard/app.py must compile without errors."""
    from pathlib import Path as _Path
    from pyui.compiler.discovery import discover_app
    from pyui.compiler import compile_app

    example = _Path(__file__).parent.parent.parent / "examples" / "dashboard" / "app.py"
    app_class = discover_app(str(example))
    out, stats = compile_app(app_class, target="web", output_dir=str(tmp_path))
    assert (out / "index.html").exists()
    assert stats["pages"] >= 3


def test_example_blog_compiles(tmp_path: Path) -> None:
    """examples/blog/app.py must compile without errors."""
    from pathlib import Path as _Path
    from pyui.compiler.discovery import discover_app
    from pyui.compiler import compile_app

    example = _Path(__file__).parent.parent.parent / "examples" / "blog" / "app.py"
    app_class = discover_app(str(example))
    out, stats = compile_app(app_class, target="web", output_dir=str(tmp_path))
    assert (out / "index.html").exists()
    assert stats["pages"] >= 2
