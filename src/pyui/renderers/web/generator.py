"""
Web renderer — HTML/CSS/JS code generator.

Converts an IRTree (or individual IRNodes/IRPages) into complete, styled
HTML pages powered by Tailwind CSS (CDN) and Alpine.js.

Public helpers (for testing and programmatic use):
    render_component(component)          → HTML fragment string
    render_page(page, theme)             → full HTML string
    WebGenerator(ir_tree).write_to_disk(output_dir)
"""

from __future__ import annotations

import html as html_module
import json
from pathlib import Path
from typing import TYPE_CHECKING, Any

from pyui.compiler.ir import IRNode, IRPage, IRTree, build_ir_node, build_ir_page
from pyui.renderers.web import tailwind as tw
from pyui.theme.tokens import BUILT_IN_THEMES, DEFAULT_TOKENS

if TYPE_CHECKING:
    from pyui.components.base import BaseComponent
    from pyui.page import Page


# ── Page HTML template ────────────────────────────────────────────────────────

_PAGE_TEMPLATE = """\
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title}</title>
  <meta name="description" content="{description}" />

  <!-- Tailwind CSS -->
  <script src="https://cdn.tailwindcss.com"></script>

  <!-- Alpine.js -->
  <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.14.1/dist/cdn.min.js"></script>

  <!-- Google Fonts: Inter -->
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap"
        rel="stylesheet" />

  <style>
    *, *::before, *::after {{ box-sizing: border-box; }}
    body {{ font-family: 'Inter', system-ui, -apple-system, sans-serif; }}
    {css_vars}
    {extra_css}
  </style>
  {favicon_tag}
</head>
<body class="bg-gray-50 text-gray-900 min-h-screen antialiased"
      x-data='{alpine_data}'>

  <!-- PyUI App -->
  <div id="pyui-app" class="{layout_class}">
{content}
  </div>

  <!-- PyUI Runtime -->
  <script>
    window.__pyuiState = {state_json};

    async function __pyuiEvent(handlerId, data) {{
      try {{
        const resp = await fetch('/pyui-api/event/' + handlerId, {{
          method: 'POST',
          headers: {{ 'Content-Type': 'application/json' }},
          body: JSON.stringify({{ handler_id: handlerId, data: data || {{}} }}),
        }});
        const result = await resp.json();
        if (result.state) {{
          Object.assign(window.__pyuiState, result.state);
          // Refresh reactive x-data proxy
          if (window.__pyuiAlpine) {{
            Object.assign(window.__pyuiAlpine, result.state);
          }}
        }}
        if (result.reload) {{
          window.location.reload();
        }}
      }} catch (e) {{
        console.error('[PyUI] Event error:', e);
      }}
    }}
  </script>
</body>
</html>
"""

# ── CSS variable generation ───────────────────────────────────────────────────


def _build_tokens(theme: str | dict[str, str]) -> dict[str, str]:
    """Merge DEFAULT_TOKENS with theme overrides → flat token dict."""
    tokens = dict(DEFAULT_TOKENS)
    overrides = BUILT_IN_THEMES.get(theme, {}) if isinstance(theme, str) else theme
    tokens.update(overrides)
    return tokens


def _tokens_to_css_vars(tokens: dict[str, str]) -> str:
    """Render tokens as a CSS :root block with --pyui-* variables."""
    lines = [":root {"]
    for key, value in tokens.items():
        css_name = "--pyui-" + key.replace(".", "-")
        lines.append(f"  {css_name}: {value};")
    lines.append("}")
    return "\n".join(lines)


# ── Component renderers ───────────────────────────────────────────────────────


def _render_node(node: IRNode) -> str:
    """Dispatch an IRNode to the correct component renderer."""
    dispatch = {
        "button": _render_button,
        "text": _render_text,
        "heading": _render_heading,
        "grid": _render_grid,
        "page": _render_page_node,  # page-root wrapper (unused normally)
    }
    renderer = dispatch.get(node.type)
    if renderer is None:
        # Unknown component — render as a debug placeholder
        return (
            f'<div class="border-2 border-dashed border-red-300 p-4 rounded text-red-500 text-sm">'
            f"Unknown component: <code>{html_module.escape(node.type)}</code>"
            f"</div>"
        )
    return renderer(node)


def _children_html(node: IRNode) -> str:
    return "\n".join(_render_node(child) for child in node.children)


def _render_button(node: IRNode) -> str:
    label = html_module.escape(str(node.props.get("label", "")))
    loading = node.props.get("loading", False)
    t = node.props.get("type", "button")
    disabled_val = node.props.get("disabled", False)

    classes = tw.button_classes(
        variant=node.style_variant,
        size=node.props.get("_size"),
        disabled=bool(disabled_val),
    )

    # Event handler attr
    click_handler = node.events.get("click")
    click_attr = f" onclick=\"__pyuiEvent('{click_handler}')\"" if click_handler else ""
    disabled_attr = " disabled" if disabled_val else ""

    # Loading spinner
    spinner = (
        '<svg class="animate-spin -ml-1 mr-2 h-4 w-4" xmlns="http://www.w3.org/2000/svg" '
        'fill="none" viewBox="0 0 24 24">'
        '<circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>'
        '<path class="opacity-75" fill="currentColor" '
        'd="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 '
        '1.135 5.824 3 7.938l3-2.647z"></path></svg>'
        if loading
        else ""
    )

    return (
        f'<button id="{node.node_id}" type="{t}" class="{classes}"'
        f"{click_attr}{disabled_attr}>"
        f"{spinner}{label}"
        f"</button>"
    )


def _render_text(node: IRNode) -> str:
    content = node.props.get("content", "")
    element = node.props.get("element", "span")
    truncate = node.props.get("truncate", False)
    node.props.get("is_reactive", False)

    # content is already resolved (callable was called during build_ir_node)
    safe = html_module.escape(str(content))
    classes = tw.text_classes(
        variant=node.style_variant,
        size=node.props.get("_size"),
        truncate=bool(truncate),
    )

    # For now, we rely on page reloads for reactivity in Phase 1.
    return f'<{element} id="{node.node_id}" class="{classes}">{safe}</{element}>'


def _render_heading(node: IRNode) -> str:
    text = html_module.escape(str(node.props.get("text", "")))
    level = node.props.get("level", 1)
    subtitle = node.props.get("subtitle")
    classes = tw.heading_classes(level=level, variant=node.style_variant)

    parts = [f'<h{level} id="{node.node_id}" class="{classes}">{text}</h{level}>']
    if subtitle:
        safe_sub = html_module.escape(str(subtitle))
        parts.append(f'<p class="mt-2 text-lg text-gray-500">{safe_sub}</p>')
    return "\n".join(parts)


def _render_grid(node: IRNode) -> str:
    cols = node.props.get("cols", 1)
    gap = node.props.get("gap", 4)
    classes = tw.grid_classes(cols=cols, gap=gap)

    inner = "\n".join(f"  {_render_node(child)}" for child in node.children)
    return f'<div id="{node.node_id}" class="{classes}">\n{inner}\n</div>'


def _render_page_node(node: IRNode) -> str:
    """Fallback: render a page-root node by rendering its children."""
    return _children_html(node)


# ── Full-page HTML builder ────────────────────────────────────────────────────


class WebGenerator:
    """
    Convert an :class:`~pyui.compiler.ir.IRTree` into HTML files.

    Parameters
    ----------
    ir_tree : IRTree
    """

    def __init__(self, ir_tree: IRTree) -> None:
        self.ir_tree = ir_tree
        self._tokens = _build_tokens(ir_tree.theme)

    def render_ir_page(self, ir_page: IRPage) -> str:
        """Render an :class:`~pyui.compiler.ir.IRPage` to a full HTML string."""
        content_parts = [f"    {_render_node(n)}" for n in ir_page.children]
        content = "\n".join(content_parts)

        layout_class = tw.PAGE_LAYOUT_CLASSES.get(ir_page.layout, tw.PAGE_LAYOUT_CLASSES["default"])
        css_vars = _tokens_to_css_vars(self._tokens)

        # Alpine x-data: dump reactive state as JSON
        state: dict[str, Any] = dict(self.ir_tree.reactive_vars)
        alpine_data = json.dumps(state, default=str)
        state_json = json.dumps(state, default=str)

        favicon_tag = ""
        favicon = self.ir_tree.app_meta.get("favicon")
        if favicon:
            favicon_tag = f'<link rel="icon" href="{html_module.escape(favicon)}" />'

        return _PAGE_TEMPLATE.format(
            title=html_module.escape(
                ir_page.title or self.ir_tree.app_meta.get("name", "PyUI App")
            ),
            description=html_module.escape(self.ir_tree.app_meta.get("description", "")),
            css_vars=css_vars,
            extra_css="",
            favicon_tag=favicon_tag,
            alpine_data=alpine_data,
            layout_class=layout_class,
            content=content,
            state_json=state_json,
        )

    def write_to_disk(self, output_dir: Path) -> None:
        """
        Write all pages to *output_dir* as HTML files.

        The root page (``route="/"`) is written as ``index.html``.
        Other pages are written as ``<route-slug>/index.html``.
        """
        output_dir.mkdir(parents=True, exist_ok=True)

        for ir_page in self.ir_tree.pages:
            html = self.render_ir_page(ir_page)

            if ir_page.route in ("/", ""):
                out_file = output_dir / "index.html"
            else:
                slug = ir_page.route.lstrip("/").replace("/", "_")
                out_file = output_dir / f"{slug}.html"

            out_file.write_text(html, encoding="utf-8")


# ── Convenience helpers (used in tests and by the dev server) ─────────────────


def render_component(component: BaseComponent) -> str:
    """
    Render a single component to an HTML fragment string.

    This is a convenience wrapper for tests and REPL exploration.
    Does **not** include a full HTML page shell.

    Parameters
    ----------
    component : BaseComponent

    Returns
    -------
    str
        HTML fragment.
    """
    node = build_ir_node(component)
    return _render_node(node)


def render_page(
    page: Page,
    theme: str | dict[str, str] = "light",
    app_meta: dict[str, Any] | None = None,
) -> str:
    """
    Render a :class:`~pyui.page.Page` to a full HTML string.

    Parameters
    ----------
    page : Page
    theme : str | dict
        Theme name or custom token dict.
    app_meta : dict | None
        Optional app metadata (name, description, favicon).

    Returns
    -------
    str
        Complete HTML document.
    """
    ir_page = build_ir_page(page)
    stub_tree = IRTree(
        app_meta=app_meta or {"name": "PyUI App", "description": "", "favicon": None},
        pages=[ir_page],
        theme=theme,
        reactive_vars={},
        event_handlers={},
    )
    return WebGenerator(stub_tree).render_ir_page(ir_page)
