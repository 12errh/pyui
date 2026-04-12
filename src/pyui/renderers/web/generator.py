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

  <!-- Icons: Lucide -->
  <script src="https://unpkg.com/lucide@latest"></script>

  <!-- Markdown: Marked -->
  <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>

  <!-- Charts: Chart.js -->
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

  <style>
    *, *::before, *::after {{ box-sizing: border-box; }}
    body {{ font-family: 'Inter', system-ui, -apple-system, sans-serif; }}
    {css_vars}
    {extra_css}
  </style>
  {favicon_tag}
</head>
<body class="bg-gray-50 text-gray-900 min-h-screen antialiased"
      x-data='{alpine_data}'
      x-init="lucide.createIcons();">

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
        "flex": _render_flex,
        "stack": _render_stack,
        "container": _render_container,
        "divider": _render_divider,
        "spacer": _render_spacer,
        "sidebar_layout": _render_sidebar,
        "split": _render_split,
        "badge": _render_badge,
        "tag": _render_tag,
        "avatar": _render_avatar,
        "icon": _render_icon,
        "image": _render_image,
        "markdown": _render_markdown,
        "video": _render_video,
        "input": _render_input,
        "textarea": _render_textarea,
        "select": _render_select,
        "checkbox": _render_checkbox,
        "radio_group": _render_radio_group,
        "toggle": _render_toggle,
        "slider": _render_slider,
        "datepicker": _render_datepicker,
        "filepicker": _render_filepicker,
        "form": _render_form,
        "alert": _render_alert,
        "toast": _render_toast,
        "modal": _render_modal,
        "drawer": _render_drawer,
        "tooltip": _render_tooltip,
        "progress": _render_progress,
        "spinner": _render_spinner,
        "skeleton": _render_skeleton,
        "nav": _render_nav,
        "tabs": _render_tabs,
        "breadcrumb": _render_breadcrumb,
        "pagination": _render_pagination,
        "menu": _render_menu,
        "table": _render_table,
        "stat": _render_stat,
        "chart": _render_chart,
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


def _render_flex(node: IRNode) -> str:
    direction = node.props.get("direction", "row")
    align = node.props.get("align", "center")
    justify = node.props.get("justify", "start")
    gap = node.props.get("gap", 4)
    wrap = node.props.get("wrap", False)
    classes = tw.flex_classes(direction, align, justify, gap, wrap)

    inner = "\n".join(f"  {_render_node(child)}" for child in node.children)
    return f'<div id="{node.node_id}" class="{classes}">\n{inner}\n</div>'


def _render_stack(node: IRNode) -> str:
    direction = node.props.get("direction", "vertical")
    spacing = node.props.get("spacing", 4)
    classes = tw.stack_classes(direction, spacing)

    inner = "\n".join(f"  {_render_node(child)}" for child in node.children)
    return f'<div id="{node.node_id}" class="{classes}">\n{inner}\n</div>'


def _render_container(node: IRNode) -> str:
    size = node.props.get("size", "xl")
    centered = node.props.get("centered", True)
    classes = tw.container_classes(size, centered)

    inner = "\n".join(f"  {_render_node(child)}" for child in node.children)
    return f'<div id="{node.node_id}" class="{classes}">\n{inner}\n</div>'


def _render_divider(node: IRNode) -> str:
    direction = node.props.get("direction", "horizontal")
    label = node.props.get("label")
    classes = tw.divider_classes(direction, label is not None)

    if direction == "horizontal" and label:
        return (
            f'<div id="{node.node_id}" class="{classes}">\n'
            f'  <div class="flex-grow border-t border-gray-200"></div>\n'
            f'  <span class="flex-shrink mx-4 text-gray-400 text-sm font-medium">{html_module.escape(label)}</span>\n'
            f'  <div class="flex-grow border-t border-gray-200"></div>\n'
            "</div>"
        )

    if direction == "vertical":
        return f'<div id="{node.node_id}" class="{classes}" role="separator"></div>'

    return f'<hr id="{node.node_id}" class="{classes}" role="separator">'


def _render_spacer(node: IRNode) -> str:
    size = node.props.get("size")
    classes = tw.spacer_classes(size)
    return f'<div id="{node.node_id}" class="{classes}"></div>'


def _render_sidebar(node: IRNode) -> str:
    side = node.props.get("side", "left")
    width = node.props.get("width", "64")
    sidebar_children = node.props.get("sidebar_children", [])
    main_children = node.props.get("main_children", [])

    sidebar_html = "\n".join(f"    {_render_node(c)}" for c in sidebar_children)
    main_html = "\n".join(f"    {_render_node(c)}" for c in main_children)

    sidebar_cls = f"w-{width} flex-none h-full border-r border-gray-200 bg-white"
    if side == "right":
        sidebar_cls = f"w-{width} flex-none h-full border-l border-gray-200 bg-white"

    parts = [
        f'<div id="{node.node_id}" class="flex h-screen w-full overflow-hidden">',
    ]

    if side == "left":
        parts.append(f'  <aside class="{sidebar_cls}">\n{sidebar_html}\n  </aside>')
        parts.append(f'  <main class="flex-grow overflow-y-auto">\n{main_html}\n  </main>')
    else:
        parts.append(f'  <main class="flex-grow overflow-y-auto">\n{main_html}\n  </main>')
        parts.append(f'  <aside class="{sidebar_cls}">\n{sidebar_html}\n  </aside>')

    parts.append("</div>")
    return "\n".join(parts)


def _render_split(node: IRNode) -> str:
    direction = node.props.get("direction", "horizontal")
    ratio = node.props.get("ratio", 0.5)
    first_pane = node.props.get("first_pane", [])
    second_pane = node.props.get("second_pane", [])

    first_html = "\n".join(f"    {_render_node(c)}" for c in first_pane)
    second_html = "\n".join(f"    {_render_node(c)}" for c in second_pane)

    if direction == "horizontal":
        return (
            f'<div id="{node.node_id}" class="flex w-full h-full">\n'
            f'  <div style="width: {ratio * 100}%" class="overflow-auto">\n{first_html}\n  </div>\n'
            f'  <div style="width: {(1 - ratio) * 100}%" class="overflow-auto">\n{second_html}\n  </div>\n'
            "</div>"
        )
    else:
        return (
            f'<div id="{node.node_id}" class="flex flex-col w-full h-full">\n'
            f'  <div style="height: {ratio * 100}%" class="overflow-auto">\n{first_html}\n  </div>\n'
            f'  <div style="height: {(1 - ratio) * 100}%" class="overflow-auto">\n{second_html}\n  </div>\n'
            "</div>"
        )


def _render_badge(node: IRNode) -> str:
    text = html_module.escape(str(node.props.get("text", "")))
    classes = tw.badge_classes(variant=node.style_variant)
    return f'<span id="{node.node_id}" class="{classes}">{text}</span>'


def _render_tag(node: IRNode) -> str:
    text = html_module.escape(str(node.props.get("text", "")))
    closable = node.props.get("closable", False)
    classes = tw.tag_classes(variant=node.style_variant)

    close_btn = ""
    if closable:
        close_btn = (
            '<button type="button" class="flex-shrink-0 ml-0.5 h-4 w-4 rounded-full inline-flex items-center justify-center text-current hover:bg-black/10 focus:outline-none">'
            '<i data-lucide="x" class="h-3 w-3"></i>'
            "</button>"
        )

    return f'<span id="{node.node_id}" class="{classes}">{text}{close_btn}</span>'


def _render_avatar(node: IRNode) -> str:
    src = node.props.get("src")
    name = node.props.get("name")
    size = node.props.get("size", "md")
    classes = tw.avatar_classes(size=size)

    if src:
        safe_src = html_module.escape(str(src))
        inner = f'<img class="h-full w-full object-cover" src="{safe_src}" alt="{html_module.escape(name or "")}">'
    elif name:
        # Generate initials
        initials = "".join(p[0] for p in str(name).split()[:2]).upper()
        inner = f"<span>{html_module.escape(initials)}</span>"
    else:
        inner = '<i data-lucide="user" class="text-gray-400"></i>'

    return f'<div id="{node.node_id}" class="{classes}">{inner}</div>'


def _render_icon(node: IRNode) -> str:
    name = node.props.get("name", "help-circle")
    size = node.props.get("icon_size", 24)
    color = node.props.get("color")
    classes = tw.icon_classes(color=color)

    # Note: style width/height for raw pixels override, data-lucide for the CDN script
    return f'<i id="{node.node_id}" data-lucide="{name}" class="{classes}" style="width: {size}px; height: {size}px;"></i>'


def _render_image(node: IRNode) -> str:
    src = html_module.escape(str(node.props.get("src", "")))
    alt = html_module.escape(str(node.props.get("alt", "")))
    fit = node.props.get("fit")
    classes = tw.image_classes(fit=fit)

    return f'<img id="{node.node_id}" src="{src}" alt="{alt}" class="{classes}" loading="lazy">'


def _render_markdown(node: IRNode) -> str:
    content = node.props.get("content", "")
    classes = tw.markdown_classes()

    # We use x-init to render markdown on the client for now (saves server dependency)
    # The content is JSON-encoded to be safe inside the x-data string
    safe_content = json.dumps(content)
    return (
        f'<div id="{node.node_id}" class="{classes}" '
        f"x-data='{{ content: {safe_content} }}' "
        f'x-html="marked.parse(content)">'
        f"</div>"
    )


def _render_video(node: IRNode) -> str:
    src = html_module.escape(str(node.props.get("src", "")))
    poster = (
        html_module.escape(str(node.props.get("poster", ""))) if node.props.get("poster") else ""
    )
    controls = "controls" if node.props.get("controls", True) else ""
    autoplay = "autoplay muted" if node.props.get("autoplay", False) else ""
    loop = "loop" if node.props.get("loop", False) else ""
    classes = tw.video_classes()

    poster_attr = f' poster="{poster}"' if poster else ""

    return (
        f'<video id="{node.node_id}" class="{classes}" {controls} {autoplay} {loop}{poster_attr}>'
        f'  <source src="{src}" type="video/mp4">'
        f"  Your browser does not support the video tag."
        f"</video>"
    )


def _render_label(node_id: str, text: str | None) -> str:
    if not text:
        return ""
    return f'<label for="{node_id}" class="block text-sm font-medium text-gray-700 mb-1">{html_module.escape(text)}</label>'


def _render_input(node: IRNode) -> str:
    val = html_module.escape(str(node.props.get("value", "")))
    placeholder = html_module.escape(str(node.props.get("placeholder", "")))
    t = node.props.get("type", "text")
    label_text = node.props.get("label")
    classes = tw.input_classes()

    label_html = _render_label(node.node_id, label_text)
    return (
        f"<div>\n"
        f"  {label_html}\n"
        f'  <input id="{node.node_id}" type="{t}" value="{val}" placeholder="{placeholder}" class="{classes}">\n'
        f"</div>"
    )


def _render_textarea(node: IRNode) -> str:
    val = html_module.escape(str(node.props.get("value", "")))
    placeholder = html_module.escape(str(node.props.get("placeholder", "")))
    rows = node.props.get("rows", 4)
    label_text = node.props.get("label")
    classes = tw.textarea_classes()

    label_html = _render_label(node.node_id, label_text)
    return (
        f"<div>\n"
        f"  {label_html}\n"
        f'  <textarea id="{node.node_id}" rows="{rows}" placeholder="{placeholder}" class="{classes}">{val}</textarea>\n'
        f"</div>"
    )


def _render_select(node: IRNode) -> str:
    options = node.props.get("options", [])
    selected_val = node.props.get("value")
    label_text = node.props.get("label")
    classes = tw.select_classes()

    label_html = _render_label(node.node_id, label_text)
    opts_html = []
    for val, label in options:
        sel = " selected" if val == selected_val else ""
        opts_html.append(
            f'    <option value="{html_module.escape(val)}"{sel}>{html_module.escape(label)}</option>'
        )

    inner = "\n".join(opts_html)
    return (
        f"<div>\n"
        f"  {label_html}\n"
        f'  <select id="{node.node_id}" class="{classes}">\n{inner}\n  </select>\n'
        f"</div>"
    )


def _render_checkbox(node: IRNode) -> str:
    checked = " checked" if node.props.get("checked") else ""
    label_text = node.props.get("label")
    classes = tw.checkbox_classes()

    inner = f'<input id="{node.node_id}" type="checkbox" class="{classes}"{checked}>'
    if label_text:
        return (
            f'<div class="flex items-center">\n'
            f"  {inner}\n"
            f'  <label for="{node.node_id}" class="ml-2 block text-sm text-gray-900">{html_module.escape(label_text)}</label>\n'
            f"</div>"
        )
    return inner


def _render_radio_group(node: IRNode) -> str:
    options = node.props.get("options", [])
    selected_val = node.props.get("value")
    label_text = node.props.get("label")
    group_name = node.node_id

    label_html = _render_label(node.node_id, label_text)
    radios = []
    for val, label in options:
        checked = " checked" if val == selected_val else ""
        opt_id = f"{group_name}-{val}"
        radios.append(
            f'  <div class="flex items-center">\n'
            f'    <input id="{opt_id}" name="{group_name}" type="radio" value="{html_module.escape(val)}" class="h-4 w-4 border-gray-300 text-violet-600 focus:ring-violet-500"{checked}>\n'
            f'    <label for="{opt_id}" class="ml-3 block text-sm font-medium text-gray-700">{html_module.escape(label)}</label>\n'
            f"  </div>"
        )

    inner = "\n".join(radios)
    return f'<div>\n  {label_html}\n  <div class="space-y-4">\n{inner}\n  </div>\n</div>'


def _render_toggle(node: IRNode) -> str:
    checked = node.props.get("checked", False)
    label_text = node.props.get("label")
    classes = tw.toggle_classes(checked)
    knob_classes = tw.toggle_knob_classes(checked)

    # Simplified toggle using a button + hidden input/Alpine state in future
    inner = (
        f'<button type="button" class="{classes}" role="switch" aria-checked="{str(checked).lower()}">\n'
        f'  <span class="{knob_classes}"></span>\n'
        f"</button>"
    )
    if label_text:
        return (
            f'<div class="flex items-center gap-3">\n'
            f"  {inner}\n"
            f'  <span class="text-sm font-medium text-gray-900">{html_module.escape(label_text)}</span>\n'
            f"</div>"
        )
    return inner


def _render_slider(node: IRNode) -> str:
    val = node.props.get("value", 0)
    min_val = node.props.get("min", 0)
    max_val = node.props.get("max", 100)
    step = node.props.get("step", 1)
    label_text = node.props.get("label")
    classes = tw.slider_classes()

    label_html = _render_label(node.node_id, label_text)
    return (
        f"<div>\n"
        f"  {label_html}\n"
        f'  <input id="{node.node_id}" type="range" min="{min_val}" max="{max_val}" step="{step}" value="{val}" class="{classes}">\n'
        f"</div>"
    )


def _render_datepicker(node: IRNode) -> str:
    val = html_module.escape(str(node.props.get("value", "")))
    label_text = node.props.get("label")
    classes = tw.datepicker_classes()

    label_html = _render_label(node.node_id, label_text)
    return (
        f"<div>\n"
        f"  {label_html}\n"
        f'  <input id="{node.node_id}" type="date" value="{val}" class="{classes}">\n'
        f"</div>"
    )


def _render_filepicker(node: IRNode) -> str:
    multiple = " multiple" if node.props.get("multiple") else ""
    accept = (
        f' accept="{html_module.escape(node.props["accept"])}"' if node.props.get("accept") else ""
    )
    label_text = node.props.get("label")
    classes = tw.filepicker_classes()

    label_html = _render_label(node.node_id, label_text)
    return (
        f"<div>\n"
        f"  {label_html}\n"
        f'  <input id="{node.node_id}" type="file" class="{classes}"{multiple}{accept}>\n'
        f"</div>"
    )


def _render_form(node: IRNode) -> str:
    title = node.props.get("title")
    classes = tw.form_classes()

    # Event handler
    submit_handler = node.events.get("change")  # We used _on_change for onSubmit stub
    submit_attr = (
        f" onsubmit=\"event.preventDefault(); __pyuiEvent('{submit_handler}')\""
        if submit_handler
        else ' onsubmit="event.preventDefault();"'
    )

    header = (
        f'<h3 class="text-lg font-medium text-gray-900 mb-4">{html_module.escape(title)}</h3>'
        if title
        else ""
    )
    inner = "\n".join(f"  {_render_node(child)}" for child in node.children)

    return f'<form id="{node.node_id}" class="{classes}"{submit_attr}>\n{header}\n{inner}\n</form>'


def _render_alert(node: IRNode) -> str:
    title = html_module.escape(str(node.props.get("title", "")))
    description = (
        html_module.escape(str(node.props.get("description", "")))
        if node.props.get("description")
        else ""
    )
    classes = tw.alert_classes(variant=node.style_variant)
    show_icon = node.props.get("show_icon", True)

    icon_html = ""
    if show_icon:
        icon_name = {
            "success": "check-circle",
            "danger": "alert-circle",
            "warning": "alert-triangle",
            "info": "info",
        }.get(node.style_variant or "info", "info")
        icon_html = f'<div class="flex-shrink-0 mr-3"><i data-lucide="{icon_name}" class="h-5 w-5"></i></div>'

    desc_html = f'<div class="mt-1 text-sm opacity-90">{description}</div>' if description else ""

    return (
        f'<div id="{node.node_id}" class="{classes}" role="alert">\n'
        f"  {icon_html}\n"
        f'  <div>\n    <h3 class="text-sm font-bold">{title}</h3>\n    {desc_html}\n  </div>\n'
        f"</div>"
    )


def _render_toast(node: IRNode) -> str:
    message = html_module.escape(str(node.props.get("message", "")))
    # duration = node.props.get("duration", 3000)
    classes = tw.toast_classes(variant=node.style_variant)

    return (
        f'<div id="{node.node_id}" x-data="{{ show: true }}" x-show="show" x-init="setTimeout(() => show = false, {node.props.get("duration", 3000)})" '
        f'class="{classes}">\n'
        f'  <div class="ms-3 text-sm font-normal">{message}</div>\n'
        f'  <button @click="show = false" class="ms-auto -mx-1.5 -my-1.5 bg-white text-gray-400 hover:text-gray-900 rounded-lg p-1.5 inline-flex items-center justify-center h-8 w-8">\n'
        f'    <i data-lucide="x" class="h-4 w-4"></i>\n'
        f"  </button>\n"
        f"</div>"
    )


def _render_modal(node: IRNode) -> str:
    title = node.props.get("title")
    is_open = node.props.get("open", False)
    footer_children = node.props.get("footer_children", [])

    overlay_cls = tw.modal_overlay_classes()
    panel_cls = tw.modal_panel_classes()

    inner = "\n".join(f"        {_render_node(child)}" for child in node.children)
    footer_html = ""
    if footer_children:
        footer_inner = "\n".join(f"          {_render_node(c)}" for c in footer_children)
        footer_html = f'      <div class="bg-gray-50 px-4 py-3 sm:flex sm:flex-row-reverse sm:px-6 gap-3">\n{footer_inner}\n      </div>'

    header_html = ""
    if title:
        header_html = (
            f'      <div class="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4 border-b border-gray-100">\n'
            f'        <h3 class="text-lg font-semibold leading-6 text-gray-900">{html_module.escape(title)}</h3>\n'
            f"      </div>"
        )

    return (
        f'<div id="{node.node_id}" x-data="{{ open: {str(is_open).lower()} }}" x-show="open" class="relative z-40">\n'
        f'  <div class="{overlay_cls}" x-show="open" x-transition.opacity @click="open = false"></div>\n'
        f'  <div class="fixed inset-0 z-50 flex items-center justify-center p-4">\n'
        f'    <div class="{panel_cls}" x-show="open" x-transition @click.away="open = false">\n'
        f"{header_html}\n"
        f'      <div class="bg-white px-4 pt-5 pb-4 sm:p-6">\n{inner}\n      </div>\n'
        f"{footer_html}\n"
        f"    </div>\n"
        f"  </div>\n"
        f"</div>"
    )


def _render_drawer(node: IRNode) -> str:
    title = node.props.get("title")
    is_open = node.props.get("open", False)
    side = node.props.get("side", "right")

    overlay_cls = tw.drawer_overlay_classes()
    panel_cls = tw.drawer_panel_classes(side)

    # Alpine transition logic
    translate_cls = "translate-x-full" if side == "right" else "-translate-x-full"

    inner = "\n".join(f"      {_render_node(child)}" for child in node.children)
    header = (
        f'<h2 class="text-lg font-medium text-gray-900">{html_module.escape(title)}</h2>'
        if title
        else ""
    )

    return (
        f'<div id="{node.node_id}" x-data="{{ open: {str(is_open).lower()} }}" x-show="open" class="relative z-40">\n'
        f'  <div class="{overlay_cls}" @click="open = false" x-show="open" x-transition.opacity></div>\n'
        f'  <div class="{panel_cls}">\n'
        f'    <div class="w-screen max-w-md bg-white shadow-xl flex flex-col h-full" '
        f'         x-show="open" x-transition:enter="transform transition ease-in-out duration-300" '
        f'         x-transition:enter-start="{translate_cls}" x-transition:enter-end="translate-x-0">\n'
        f'      <div class="px-4 py-6 sm:px-6 border-b flex items-center justify-between">\n'
        f"        {header}\n"
        f'        <button @click="open = false" class="text-gray-400 hover:text-gray-500"><i data-lucide="x"></i></button>\n'
        f"      </div>\n"
        f'      <div class="relative flex-1 px-4 py-6 sm:px-6 overflow-y-auto">\n{inner}\n      </div>\n'
        f"    </div>\n"
        f"  </div>\n"
        f"</div>"
    )


def _render_tooltip(node: IRNode) -> str:
    text = html_module.escape(str(node.props.get("text", "")))
    classes = tw.tooltip_classes()

    # Needs a parent element to hover on. For IR purposes, tooltips wrap their children.
    inner = "\n".join(_render_node(c) for c in node.children)

    return (
        f'<div class="relative inline-block group" id="{node.node_id}">\n'
        f"  {inner}\n"
        f'  <div class="{classes} group-hover:visible group-hover:opacity-100 bottom-full left-1/2 -translate-x-1/2 mb-2 whitespace-nowrap">\n'
        f"    {text}\n"
        f'    <div class="tooltip-arrow" data-popper-arrow></div>\n'
        f"  </div>\n"
        f"</div>"
    )


def _render_progress(node: IRNode) -> str:
    val = node.props.get("value", 0)
    max_val = node.props.get("max", 100)
    circular = node.props.get("circular", False)
    pct = (val / max_val) * 100

    if circular:
        # Simple SVG circle progress
        return (
            f'<div id="{node.node_id}" class="relative h-12 w-12">\n'
            f'  <svg class="h-full w-full" viewBox="0 0 36 36">\n'
            f'    <path class="text-gray-200" stroke-width="3" stroke="currentColor" fill="none" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" />\n'
            f'    <path class="text-violet-600" stroke-width="3" stroke-dasharray="{pct}, 100" stroke-linecap="round" stroke="currentColor" fill="none" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" />\n'
            f"  </svg>\n"
            f"</div>"
        )

    base_cls = tw.progress_base_classes()
    bar_cls = tw.progress_bar_classes()
    return (
        f'<div id="{node.node_id}" class="{base_cls}">\n'
        f'  <div class="{bar_cls}" style="width: {pct}%"></div>\n'
        f"</div>"
    )


def _render_spinner(node: IRNode) -> str:
    size = node.props.get("spinner_size", "md")
    classes = tw.spinner_classes(size)

    return (
        f'<svg id="{node.node_id}" class="{classes}" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">\n'
        f'  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>\n'
        f'  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>\n'
        f"</svg>"
    )


def _render_skeleton(node: IRNode) -> str:
    variant = node.props.get("variant", "text")
    classes = tw.skeleton_classes(variant)

    if variant == "circle":
        return f'<div id="{node.node_id}" class="{classes} h-12 w-12"></div>'
    if variant == "rect":
        return f'<div id="{node.node_id}" class="{classes} h-32 w-full"></div>'
    return f'<div id="{node.node_id}" class="{classes}"></div>'


def _render_nav(node: IRNode) -> str:
    items = node.props.get("items", [])
    classes = tw.nav_classes()

    links = []
    for label, route in items:
        # Simplified 'active' detection for now
        cls = tw.nav_item_classes(active=False)
        links.append(f'  <a href="{route}" class="{cls}">{html_module.escape(label)}</a>')

    inner = "\n".join(links)
    return f'<nav id="{node.node_id}" class="{classes}">\n{inner}\n</nav>'


def _render_tabs(node: IRNode) -> str:
    tabs = node.props.get("tabs", [])
    active_tab = node.props.get("active_tab") or (tabs[0]["label"] if tabs else "")

    list_cls = tw.tabs_list_classes()

    tab_buttons = []
    tab_contents = []

    for _i, tab in enumerate(tabs):
        label = tab["label"]
        active_expr = f"selected === '{label}'"
        tw.tab_item_classes(active=False)  # We'll use Alpine :class
        active_cls = tw.tab_item_classes(active=True)
        inactive_cls = tw.tab_item_classes(active=False)

        tab_buttons.append(
            f"    <button @click=\"selected = '{label}'\" "
            f"            :class=\"{active_expr} ? '{active_cls}' : '{inactive_cls}'\">\n"
            f"      {html_module.escape(label)}\n"
            f"    </button>"
        )

        # Build children HTML for the panel
        children_html = "\n".join(f"      {_render_node(child)}" for child in tab["children"])
        tab_contents.append(
            f"    <div x-show=\"selected === '{label}'\" x-transition>\n{children_html}\n    </div>"
        )

    inner_btns = "\n".join(tab_buttons)
    inner_panels = "\n".join(tab_contents)

    return (
        f'<div id="{node.node_id}" x-data="{{ selected: \'{active_tab}\' }}">\n'
        f'  <div class="{list_cls}">\n{inner_btns}\n  </div>\n'
        f'  <div class="mt-2">\n{inner_panels}\n  </div>\n'
        f"</div>"
    )


def _render_breadcrumb(node: IRNode) -> str:
    items = node.props.get("items", [])
    classes = tw.breadcrumb_classes()

    links = []
    for i, (label, route) in enumerate(items):
        is_last = i == len(items) - 1
        if i > 0:
            links.append('  <span class="text-gray-400">/</span>')

        if is_last:
            links.append(
                f'  <span class="font-medium text-gray-900">{html_module.escape(label)}</span>'
            )
        else:
            links.append(
                f'  <a href="{route}" class="hover:text-violet-600 transition-colors">{html_module.escape(label)}</a>'
            )

    inner = "\n".join(links)
    return f'<nav id="{node.node_id}" class="{classes}" aria-label="Breadcrumb">\n{inner}\n</nav>'


def _render_pagination(node: IRNode) -> str:
    current = node.props.get("current", 1)
    total = node.props.get("total", 1)
    classes = tw.pagination_classes()

    items = []
    # Prev
    prev_disabled = current <= 1
    items.append(
        f'  <a href="#" class="{tw.pagination_item_classes(False, prev_disabled)}"><i data-lucide="chevron-left" class="h-4 w-4"></i></a>'
    )

    # Numbers
    for i in range(1, total + 1):
        active = i == current
        items.append(f'  <a href="#" class="{tw.pagination_item_classes(active)}">{i}</a>')

    # Next
    next_disabled = current >= total
    items.append(
        f'  <a href="#" class="{tw.pagination_item_classes(False, next_disabled)}"><i data-lucide="chevron-right" class="h-4 w-4"></i></a>'
    )

    inner = "\n".join(items)
    return f'<nav id="{node.node_id}" class="{classes}">\n{inner}\n</nav>'


def _render_menu(node: IRNode) -> str:
    items = node.props.get("items", [])
    classes = tw.menu_classes()

    links = []
    for label, route in items:
        item_cls = tw.menu_item_classes()
        links.append(f'  <a href="{route}" class="{item_cls}">{html_module.escape(label)}</a>')

    inner = "\n".join(links)
    return f'<div id="{node.node_id}" class="{classes}">\n{inner}\n</div>'


def _render_table(node: IRNode) -> str:
    headers = node.props.get("headers", [])
    rows = node.props.get("rows", [])
    striped = node.props.get("striped", False)

    base_cls = tw.table_base_classes()
    header_cls = tw.table_header_classes()
    row_cls = tw.table_row_classes(striped=striped)

    header_html = "".join(f'<th class="{header_cls}">{html_module.escape(h)}</th>' for h in headers)

    body_rows = []
    for row in rows:
        cells = "".join(
            f'<td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{html_module.escape(str(c))}</td>'
            for c in row
        )
        body_rows.append(f'      <tr class="{row_cls}">{cells}</tr>')

    inner_rows = "\n".join(body_rows)
    return (
        f'<div class="overflow-hidden border border-gray-200 rounded-lg" id="{node.node_id}">\n'
        f'  <table class="{base_cls}">\n'
        f'    <thead class="bg-gray-50">\n      <tr>{header_html}</tr>\n    </thead>\n'
        f'    <tbody class="bg-white divide-y divide-gray-200">\n{inner_rows}\n    </tbody>\n'
        f"  </table>\n"
        f"</div>"
    )


def _render_stat(node: IRNode) -> str:
    label = html_module.escape(str(node.props.get("label", "")))
    value = html_module.escape(str(node.props.get("value", "")))
    trend = node.props.get("trend")
    trend_up = node.props.get("trend_up", True)

    card_cls = tw.stat_card_classes()
    val_cls = tw.stat_value_classes()

    trend_html = ""
    if trend:
        color_cls = "text-emerald-600 bg-emerald-50" if trend_up else "text-red-600 bg-red-50"
        trend_icon = "arrow-up-right" if trend_up else "arrow-down-right"
        trend_html = (
            f'<div class="flex items-center rounded-md px-2 py-0.5 text-xs font-medium {color_cls}">\n'
            f'  <i data-lucide="{trend_icon}" class="mr-1 h-3 w-3"></i>\n'
            f"  {html_module.escape(trend)}\n"
            f"</div>"
        )

    return (
        f'<div id="{node.node_id}" class="{card_cls}">\n'
        f'  <p class="text-sm font-medium text-gray-500 truncate">{label}</p>\n'
        f'  <div class="{val_cls}">\n'
        f'    <p class="text-2xl font-bold tracking-tight text-gray-900">{value}</p>\n'
        f"    {trend_html}\n"
        f"  </div>\n"
        f"</div>"
    )


def _render_chart(node: IRNode) -> str:
    chart_type = node.props.get("chart_type", "line")
    labels = node.props.get("labels", [])
    datasets = node.props.get("datasets", [])

    container_cls = tw.chart_container_classes()

    # Configuration for Chart.js
    config = {
        "type": chart_type,
        "data": {"labels": labels, "datasets": datasets},
        "options": {
            "responsive": True,
            "maintainAspectRatio": False,
            "plugins": {"legend": {"position": "bottom"}},
        },
    }

    safe_config = json.dumps(config)

    return (
        f'<div id="{node.node_id}" class="{container_cls}" '
        f'     x-data="{{ chartConfig: {html_module.escape(safe_config)} }}" '
        f'     x-init="new Chart($refs.canvas, chartConfig)">\n'
        f'  <canvas x-ref="canvas"></canvas>\n'
        f"</div>"
    )


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
