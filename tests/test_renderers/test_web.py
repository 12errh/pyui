"""
Phase 1 — web renderer tests.

Tests from the PyUI spec Section 5, Phase 1, plus additional coverage.
"""

from __future__ import annotations

from pathlib import Path

# ── Spec tests ────────────────────────────────────────────────────────────────


def test_button_renders_html() -> None:
    """Button must render a <button> element containing its label."""
    from pyui import Button
    from pyui.renderers.web import render_component

    btn = Button("Submit").style("primary")
    html = render_component(btn)
    assert "Submit" in html
    assert "<button" in html


def test_heading_renders_correct_tag() -> None:
    """Heading(level=2) must render an <h2> element."""
    from pyui import Heading
    from pyui.renderers.web import render_component

    h = Heading("Hello", level=2)
    html = render_component(h)
    assert "<h2" in html
    assert "Hello" in html


def test_grid_renders_children() -> None:
    """Grid must render its children inside it."""
    from pyui import Grid, Text
    from pyui.renderers.web import render_component

    grid = Grid(cols=2).add(Text("A"), Text("B"))
    html = render_component(grid)
    assert "A" in html
    assert "B" in html


def test_page_title_in_html() -> None:
    """render_page() must include the page title in the HTML <title> tag."""
    from pyui import App, Page
    from pyui.renderers.web import render_page

    class TestApp(App):
        home = Page(title="My Page", route="/")

    html = render_page(TestApp.home)
    assert "My Page" in html


# ── Additional renderer tests ─────────────────────────────────────────────────


def test_button_primary_has_bg_class() -> None:
    """Primary Button must contain bg-violet Tailwind classes."""
    from pyui import Button
    from pyui.renderers.web import render_component

    html = render_component(Button("Go").style("primary"))
    assert "bg-violet" in html


def test_button_danger_variant() -> None:
    """Danger Button must contain red Tailwind classes."""
    from pyui import Button
    from pyui.renderers.web import render_component

    html = render_component(Button("Delete").style("danger"))
    assert "red" in html


def test_heading_h1_rendered() -> None:
    """Heading(level=1) renders <h1>."""
    from pyui import Heading
    from pyui.renderers.web import render_component

    html = render_component(Heading("Big Title", level=1))
    assert "<h1" in html
    assert "Big Title" in html


def test_text_renders_content() -> None:
    """Text component renders its content string."""
    from pyui import Text
    from pyui.renderers.web import render_component

    html = render_component(Text("Hello, World!"))
    assert "Hello, World!" in html


def test_text_reactive_content_resolved() -> None:
    """Text with a lambda must resolve the lambda at render time."""
    from pyui import Text
    from pyui.renderers.web import render_component

    html = render_component(Text(lambda: "dynamic content"))
    assert "dynamic content" in html


def test_grid_has_grid_class() -> None:
    """Grid renders a div with a CSS grid class."""
    from pyui import Grid
    from pyui.renderers.web import render_component

    html = render_component(Grid(cols=3))
    assert "grid" in html


def test_grid_cols_reflected_in_class() -> None:
    """Grid(cols=3) must produce a grid-cols-3 class on the wrapper div."""
    from pyui import Grid
    from pyui.renderers.web import render_component

    html = render_component(Grid(cols=3))
    assert "grid-cols-3" in html


def test_button_click_handler_in_output() -> None:
    """Button with onClick must emit onclick attribute referencing handler id."""
    from pyui import Button
    from pyui.renderers.web import render_component

    html = render_component(Button("Fire").onClick(lambda: None))
    assert "onclick" in html
    assert "__pyuiEvent" in html


def test_full_page_has_tailwind_cdn() -> None:
    """Full rendered page must include the Tailwind CDN script tag."""
    from pyui import Page
    from pyui.renderers.web import render_page

    p = Page(title="CDN Test", route="/")
    html = render_page(p)
    assert "cdn.tailwindcss.com" in html


def test_full_page_has_alpinejs() -> None:
    """Full rendered page must include the Alpine.js CDN script."""
    from pyui import Page
    from pyui.renderers.web import render_page

    p = Page(title="Alpine Test", route="/")
    html = render_page(p)
    assert "alpinejs" in html


def test_full_page_has_inter_font() -> None:
    """Full rendered page must load the Inter Google Font."""
    from pyui import Page
    from pyui.renderers.web import render_page

    p = Page(title="Font Test", route="/")
    html = render_page(p)
    assert "Inter" in html


# ── Integration — compile_app writes files ────────────────────────────────────


def test_full_web_compile_pipeline(tmp_path: Path) -> None:
    """compile_app() must write index.html containing all component text."""
    from pyui import App, Button, Page, Text
    from pyui.compiler import compile_app

    class MyApp(App):
        home = Page(title="Test", route="/")
        home.add(
            Text("Welcome"),
            Button("Go").style("primary"),
        )

    output_dir = tmp_path / "dist"
    compile_app(MyApp, target="web", output_dir=str(output_dir))

    index = output_dir / "index.html"
    assert index.exists()
    content = index.read_text(encoding="utf-8")
    assert "Welcome" in content
    assert "Go" in content
    assert "Test" in content


def test_compile_multi_page_app(tmp_path: Path) -> None:
    """compile_app() writes one file per page."""
    from pyui import App, Page, Text
    from pyui.compiler import compile_app

    class MultiApp(App):
        home = Page(title="Home", route="/")
        home.add(Text("Homepage"))
        about = Page(title="About", route="/about")
        about.add(Text("About page"))

    out = tmp_path / "dist"
    compile_app(MultiApp, target="web", output_dir=str(out))

    assert (out / "index.html").exists()
    assert (out / "about.html").exists()
    assert "Homepage" in (out / "index.html").read_text()
    assert "About page" in (out / "about.html").read_text()
