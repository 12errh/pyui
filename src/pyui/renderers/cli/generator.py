"""
CLI renderer — Rich TUI backend.

Converts an IRTree into Rich renderables displayed in the terminal.
Interactive inputs use prompt_toolkit when available, falling back to
Python's built-in ``input()``.

Public API::

    from pyui.renderers.cli import run_cli_app, render_to_rich

    run_cli_app(MyApp)
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from rich import box
from rich.columns import Columns
from rich.console import Console, Group
from rich.panel import Panel
from rich.progress import BarColumn, Progress, TaskProgressColumn, TextColumn
from rich.rule import Rule
from rich.spinner import Spinner as RichSpinner
from rich.table import Table as RichTable
from rich.text import Text as RichText

from pyui.compiler.ir import IRNode, IRPage, IRTree, build_ir_tree, get_handler
from pyui.utils.logging import get_logger

if TYPE_CHECKING:
    from rich.console import RenderableType

    from pyui.app import App

log = get_logger(__name__)

console = Console()

# ── Colour palette (mirrors the web design tokens) ───────────────────────────

_VARIANT_STYLE: dict[str | None, str] = {
    "primary": "bold white on grey11",
    "secondary": "grey70 on grey93",
    "ghost": "grey50",
    "danger": "bold white on red3",
    "success": "bold white on green4",
    "warning": "bold black on yellow3",
    "info": "bold white on blue3",
    None: "bold white on grey11",
}

_ALERT_BORDER: dict[str, str] = {
    "info": "blue",
    "success": "green",
    "warning": "yellow",
    "danger": "red",
}

_HEADING_STYLES: dict[int, str] = {
    1: "bold white",
    2: "bold grey93",
    3: "bold grey70",
    4: "grey70",
    5: "grey50",
    6: "grey50",
}

_HEADING_SIZES: dict[int, str] = {
    1: "  ",  # extra indent for visual weight
    2: " ",
    3: "",
    4: "",
    5: "",
    6: "",
}


# ── Component renderers ───────────────────────────────────────────────────────


def _render_button(node: IRNode) -> RenderableType:
    label = str(node.props.get("label", ""))
    variant = node.style_variant
    style = _VARIANT_STYLE.get(variant, _VARIANT_STYLE[None])
    disabled = bool(node.props.get("disabled", False))

    if disabled:
        style = "grey50"

    text = RichText(f" {label} ", style=style)
    return Panel(text, expand=False, padding=(0, 1), box=box.ROUNDED)


def _render_text(node: IRNode) -> RenderableType:
    content = str(node.props.get("content", ""))
    variant = node.style_variant

    style_map: dict[str | None, str] = {
        "muted": "grey50",
        "code": "bold green on grey11",
        "lead": "bold",
        "small": "dim",
        None: "",
    }
    style = style_map.get(variant, "")
    return RichText(content, style=style)


def _render_heading(node: IRNode) -> RenderableType:
    text = str(node.props.get("text", ""))
    level = int(node.props.get("level", 1))
    subtitle = node.props.get("subtitle")

    style = _HEADING_STYLES.get(level, "bold")
    prefix = _HEADING_SIZES.get(level, "")
    rule_char = "━" if level == 1 else "─"

    parts: list[RenderableType] = [Rule(f"{prefix}{text}", style=style, characters=rule_char)]
    if subtitle:
        parts.append(RichText(str(subtitle), style="grey50"))

    return Group(*parts)


def _render_grid(node: IRNode) -> RenderableType:
    cols = int(node.props.get("cols", 1))
    children = [render_node(c) for c in node.children]

    if not children:
        return RichText("")

    if cols == 1:
        return Group(*children)

    # Split children into rows of `cols` items
    rows: list[RenderableType] = []
    for i in range(0, len(children), cols):
        chunk = children[i : i + cols]
        rows.append(Columns(chunk, equal=True, expand=True))

    return Group(*rows)


def _render_flex(node: IRNode) -> RenderableType:
    direction = node.props.get("direction", "row")
    children = [render_node(c) for c in node.children]

    if not children:
        return RichText("")

    if direction == "row":
        return Columns(children, expand=False)
    return Group(*children)


def _render_stack(node: IRNode) -> RenderableType:
    children = [render_node(c) for c in node.children]
    return Group(*children) if children else RichText("")


def _render_container(node: IRNode) -> RenderableType:
    children = [render_node(c) for c in node.children]
    inner = Group(*children) if children else RichText("")
    return Panel(inner, box=box.SIMPLE, padding=(0, 2))


def _render_divider(node: IRNode) -> RenderableType:
    label = node.props.get("label")
    direction = node.props.get("direction", "horizontal")
    if direction == "vertical":
        return RichText(" │ ", style="grey50")
    return Rule(str(label) if label else "", style="grey30")


def _render_spacer(_node: IRNode) -> RenderableType:
    return RichText("")


def _render_badge(node: IRNode) -> RenderableType:
    text = str(node.props.get("text", ""))
    variant = node.style_variant
    style = _VARIANT_STYLE.get(variant, "bold grey70 on grey93")
    return RichText(f" {text} ", style=style)


def _render_tag(node: IRNode) -> RenderableType:
    text = str(node.props.get("text", ""))
    return RichText(f"[{text}]", style="grey50")


def _render_avatar(node: IRNode) -> RenderableType:
    name = node.props.get("name", "")
    initials = "".join(p[0] for p in str(name).split()[:2]).upper() if name else "?"
    return Panel(
        RichText(initials, style="bold white", justify="center"),
        width=5,
        height=3,
        box=box.ROUNDED,
        style="on grey30",
    )


def _render_icon(node: IRNode) -> RenderableType:
    name = str(node.props.get("name", "•"))
    return RichText(f"[{name}]", style="grey50")


def _render_image(node: IRNode) -> RenderableType:
    src = str(node.props.get("src", ""))
    alt = str(node.props.get("alt", "image"))
    return Panel(
        RichText(f"🖼  {alt}", style="grey50"),
        subtitle=src[:40] + "…" if len(src) > 40 else src,
        box=box.SIMPLE,
        style="grey30",
    )


def _render_markdown(node: IRNode) -> RenderableType:
    content = str(node.props.get("content", ""))
    try:
        from rich.markdown import Markdown

        return Markdown(content)
    except Exception:
        return RichText(content)


def _render_video(node: IRNode) -> RenderableType:
    src = str(node.props.get("src", ""))
    return Panel(RichText(f"▶  Video: {src}", style="grey50"), box=box.SIMPLE)


def _render_input(node: IRNode) -> RenderableType:
    label_text = node.props.get("label")
    placeholder = str(node.props.get("placeholder", ""))
    value = str(node.props.get("value", ""))

    display = value if value else f"({placeholder})" if placeholder else "(empty)"
    label_prefix = f"{label_text}: " if label_text else ""
    return RichText(f"{label_prefix}{display}", style="grey70")


def _render_textarea(node: IRNode) -> RenderableType:
    label_text = node.props.get("label")
    value = str(node.props.get("value", ""))
    rows = int(node.props.get("rows", 4))

    lines = value.split("\n")[:rows]
    content = "\n".join(lines) if lines else "(empty)"
    title = str(label_text) if label_text else "Textarea"
    return Panel(RichText(content, style="grey70"), title=title, box=box.SIMPLE)


def _render_select(node: IRNode) -> RenderableType:
    options = node.props.get("options") or []
    selected = node.props.get("value")
    label_text = node.props.get("label")

    display_options: list[str] = []
    for opt in options:
        if isinstance(opt, (list, tuple)) and len(opt) >= 2:
            val, lbl = str(opt[0]), str(opt[1])
        else:
            val = lbl = str(opt)
        marker = "▶ " if val == selected else "  "
        display_options.append(f"{marker}{lbl}")

    label_prefix = f"{label_text}\n" if label_text else ""
    return RichText(label_prefix + "\n".join(display_options), style="grey70")


def _render_checkbox(node: IRNode) -> RenderableType:
    checked = bool(node.props.get("checked", False))
    label_text = str(node.props.get("label", ""))
    mark = "☑" if checked else "☐"
    return RichText(f"{mark}  {label_text}", style="grey70")


def _render_toggle(node: IRNode) -> RenderableType:
    checked = bool(node.props.get("checked", False))
    label_text = str(node.props.get("label", ""))
    mark = "● ON " if checked else "○ OFF"
    return RichText(f"[{mark}]  {label_text}", style="grey70")


def _render_slider(node: IRNode) -> RenderableType:
    value = float(node.props.get("value", 0))
    min_val = float(node.props.get("min", 0))
    max_val = float(node.props.get("max", 100))
    label_text = node.props.get("label")

    pct = (value - min_val) / (max_val - min_val) if max_val != min_val else 0
    filled = int(pct * 20)
    bar = "█" * filled + "░" * (20 - filled)
    label_prefix = f"{label_text}: " if label_text else ""
    return RichText(f"{label_prefix}[{bar}] {value:.0f}", style="grey70")


def _render_form(node: IRNode) -> RenderableType:
    title = node.props.get("title")
    children = [render_node(c) for c in node.children]
    inner = Group(*children) if children else RichText("")
    return Panel(inner, title=str(title) if title else "Form", box=box.ROUNDED)


def _render_alert(node: IRNode) -> RenderableType:
    title = str(node.props.get("title", ""))
    description = node.props.get("description")
    variant = node.style_variant or "info"
    border_color = _ALERT_BORDER.get(variant, "blue")

    content_parts = [RichText(title, style="bold")]
    if description:
        content_parts.append(RichText(str(description), style="grey70"))

    return Panel(
        Group(*content_parts),
        border_style=border_color,
        box=box.ROUNDED,
        padding=(0, 1),
    )


def _render_toast(node: IRNode) -> RenderableType:
    message = str(node.props.get("message", ""))
    variant = node.style_variant or "info"
    border_color = _ALERT_BORDER.get(variant, "blue")
    return Panel(RichText(message), border_style=border_color, box=box.SIMPLE, expand=False)


def _render_modal(node: IRNode) -> RenderableType:
    title = node.props.get("title", "Modal")
    children = [render_node(c) for c in node.children]
    inner = Group(*children) if children else RichText("")
    return Panel(inner, title=str(title), box=box.DOUBLE, padding=(1, 2))


def _render_drawer(node: IRNode) -> RenderableType:
    title = node.props.get("title", "Drawer")
    children = [render_node(c) for c in node.children]
    inner = Group(*children) if children else RichText("")
    return Panel(inner, title=str(title), box=box.SIMPLE, padding=(0, 1))


def _render_tooltip(node: IRNode) -> RenderableType:
    text = str(node.props.get("text", ""))
    children = [render_node(c) for c in node.children]
    inner = Group(*children) if children else RichText("")
    return Group(inner, RichText(f"  ℹ  {text}", style="dim grey50"))


def _render_progress(node: IRNode) -> RenderableType:
    value = float(node.props.get("value", 0))
    label_text = node.props.get("label")

    progress = Progress(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        expand=True,
    )
    task_label = str(label_text) if label_text else "Progress"
    task = progress.add_task(task_label, total=100)
    progress.update(task, completed=value)
    return progress


def _render_spinner(_node: IRNode) -> RenderableType:
    return RichSpinner("dots", text="Loading…", style="grey50")


def _render_skeleton(_node: IRNode) -> RenderableType:
    return RichText("░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░", style="grey30")


def _render_table(node: IRNode) -> RenderableType:
    headers = node.props.get("headers", [])
    rows = node.props.get("rows", [])
    striped = bool(node.props.get("striped", False))

    table = RichTable(box=box.SIMPLE_HEAD, show_header=True, header_style="bold grey93")
    for col in headers:
        table.add_column(str(col))

    for i, row in enumerate(rows):
        style = "on grey11" if striped and i % 2 == 0 else ""
        table.add_row(*[str(v) for v in row], style=style)

    return table


def _render_stat(node: IRNode) -> RenderableType:
    label = str(node.props.get("label", ""))
    value = str(node.props.get("value", ""))
    trend = node.props.get("trend")
    trend_up = bool(node.props.get("trend_up", True))

    trend_str = ""
    if trend:
        arrow = "▲" if trend_up else "▼"
        color = "green" if trend_up else "red"
        trend_str = f"\n[{color}]{arrow} {trend}[/{color}]"

    content = RichText.from_markup(
        f"[grey50]{label}[/grey50]\n[bold white]{value}[/bold white]{trend_str}"
    )
    return Panel(content, box=box.SIMPLE, padding=(0, 2))


def _render_chart(node: IRNode) -> RenderableType:
    chart_type = str(node.props.get("chart_type", "line"))
    labels = node.props.get("labels", [])
    datasets = node.props.get("datasets", [])

    # ASCII bar chart for the first dataset
    if datasets and labels:
        ds = datasets[0]
        data = ds.get("data", [])
        ds_label = ds.get("label", "")
        max_val = max((float(v) for v in data if v is not None), default=1) or 1

        table = RichTable(box=box.SIMPLE, show_header=False, padding=(0, 1))
        table.add_column("Label", style="grey70", width=12)
        table.add_column("Bar", ratio=1)
        table.add_column("Value", style="grey50", width=8, justify="right")

        for lbl, val in zip(labels, data, strict=False):
            if val is None:
                continue
            pct = float(val) / max_val
            bar = "█" * int(pct * 30)
            table.add_row(str(lbl), f"[cyan]{bar}[/cyan]", str(val))

        return Panel(table, title=f"{chart_type.title()} Chart — {ds_label}", box=box.ROUNDED)

    return Panel(
        RichText(f"[{chart_type} chart — no data]", style="grey50"),
        box=box.SIMPLE,
    )


def _render_nav(node: IRNode) -> RenderableType:
    items = node.props.get("items", [])
    parts: list[str] = []
    for item in items:
        if isinstance(item, (list, tuple)) and len(item) >= 2:
            parts.append(str(item[0]))
        else:
            parts.append(str(item))

    return Panel(
        RichText("  ".join(parts), style="bold white"),
        style="on grey11",
        box=box.SIMPLE,
        padding=(0, 2),
    )


def _render_tabs(node: IRNode) -> RenderableType:
    tabs_data = node.props.get("tabs", [])
    active = node.props.get("active_tab")

    if not tabs_data:
        return RichText("")

    # Show tab headers
    headers = []
    for tab in tabs_data:
        label = str(tab.get("label", "Tab"))
        if label == active:
            headers.append(f"[bold white on grey30] {label} [/bold white on grey30]")
        else:
            headers.append(f"[grey50] {label} [/grey50]")

    header_line = RichText.from_markup("  ".join(headers))

    # Show first tab content (or active tab)
    active_tab = tabs_data[0]
    for tab in tabs_data:
        if tab.get("label") == active:
            active_tab = tab
            break

    children = active_tab.get("children", [])
    child_renderables = [render_node(c) for c in children if isinstance(c, IRNode)]
    content = Group(*child_renderables) if child_renderables else RichText("")

    return Group(header_line, Rule(style="grey30"), content)


def _render_breadcrumb(node: IRNode) -> RenderableType:
    items = node.props.get("items", [])
    parts: list[str] = []
    for item in items:
        if isinstance(item, (list, tuple)) and len(item) >= 2:
            parts.append(str(item[0]))
        else:
            parts.append(str(item))
    return RichText(" / ".join(parts), style="grey50")


def _render_pagination(node: IRNode) -> RenderableType:
    current = int(node.props.get("current", 1))
    total = int(node.props.get("total", 1))
    return RichText(f"← Page {current} of {total} →", style="grey50")


def _render_menu(node: IRNode) -> RenderableType:
    items = node.props.get("items", [])
    lines: list[str] = []
    for item in items:
        if isinstance(item, (list, tuple)) and len(item) >= 2:
            lines.append(f"  {item[0]}")
        else:
            lines.append(f"  {item}")
    return Panel(
        RichText("\n".join(lines), style="grey70"),
        box=box.SIMPLE,
        padding=(0, 1),
    )


def _render_list_component(node: IRNode) -> RenderableType:
    children = [render_node(c) for c in node.children]
    return Group(*children) if children else RichText("")


def _render_sidebar_layout(node: IRNode) -> RenderableType:
    sidebar_children = node.props.get("sidebar_children", [])
    main_children = node.props.get("main_children", [])

    sidebar_parts = [render_node(c) for c in sidebar_children if isinstance(c, IRNode)]
    main_parts = [render_node(c) for c in main_children if isinstance(c, IRNode)]

    sidebar_panel = Panel(
        Group(*sidebar_parts) if sidebar_parts else RichText(""),
        title="Sidebar",
        box=box.SIMPLE,
        width=30,
    )
    main_panel = Panel(
        Group(*main_parts) if main_parts else RichText(""),
        box=box.SIMPLE,
    )
    return Columns([sidebar_panel, main_panel], expand=True)


def _render_raw_html(node: IRNode) -> RenderableType:
    content = str(node.props.get("html", ""))
    return Panel(
        RichText(content[:200] + ("…" if len(content) > 200 else ""), style="grey50"),
        title="[Raw HTML]",
        box=box.SIMPLE,
    )


# ── Dispatch table ────────────────────────────────────────────────────────────

_RENDERERS: dict[str, Any] = {
    "button": _render_button,
    "text": _render_text,
    "heading": _render_heading,
    "grid": _render_grid,
    "flex": _render_flex,
    "stack": _render_stack,
    "container": _render_container,
    "divider": _render_divider,
    "spacer": _render_spacer,
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
    "toggle": _render_toggle,
    "slider": _render_slider,
    "form": _render_form,
    "alert": _render_alert,
    "toast": _render_toast,
    "modal": _render_modal,
    "drawer": _render_drawer,
    "tooltip": _render_tooltip,
    "progress": _render_progress,
    "spinner": _render_spinner,
    "skeleton": _render_skeleton,
    "table": _render_table,
    "stat": _render_stat,
    "chart": _render_chart,
    "nav": _render_nav,
    "tabs": _render_tabs,
    "breadcrumb": _render_breadcrumb,
    "pagination": _render_pagination,
    "menu": _render_menu,
    "list": _render_list_component,
    "sidebar_layout": _render_sidebar_layout,
    "raw_html": _render_raw_html,
}


def render_node(node: IRNode) -> RenderableType:
    """
    Convert a single :class:`~pyui.compiler.ir.IRNode` into a Rich renderable.

    Parameters
    ----------
    node : IRNode

    Returns
    -------
    RenderableType
    """
    renderer = _RENDERERS.get(node.type)
    if renderer is None:
        return RichText(f"[unknown: {node.type}]", style="red")
    result: RenderableType = renderer(node)
    return result


def render_to_rich(ir_page: IRPage) -> RenderableType:
    """
    Convert an :class:`~pyui.compiler.ir.IRPage` into a Rich renderable.

    Parameters
    ----------
    ir_page : IRPage

    Returns
    -------
    RenderableType
    """
    parts: list[RenderableType] = []
    for child in ir_page.children:
        parts.append(render_node(child))

    inner = Group(*parts) if parts else RichText("(empty page)")
    return Panel(
        inner,
        title=f"[bold]{ir_page.title}[/bold]" if ir_page.title else "",
        box=box.ROUNDED,
        padding=(1, 2),
    )


# ── Interactive CLI runner ────────────────────────────────────────────────────


class CliRenderer:
    """
    Renders an :class:`~pyui.compiler.ir.IRTree` in the terminal.

    Displays each page in sequence. Button clicks are handled via
    numbered prompts.

    Parameters
    ----------
    app_class : type[App]
        The user's App subclass.
    """

    def __init__(self, app_class: type[App]) -> None:
        self.app_class = app_class
        self._ir_tree: IRTree = build_ir_tree(app_class)

    def _collect_buttons(self, nodes: list[IRNode]) -> list[tuple[str, str]]:
        """Recursively collect (label, handler_id) for all buttons."""
        buttons: list[tuple[str, str]] = []
        for node in nodes:
            if node.type == "button" and "click" in node.events:
                label = str(node.props.get("label", "Button"))
                buttons.append((label, node.events["click"]))
            buttons.extend(self._collect_buttons(node.children))
        return buttons

    def run(self) -> None:
        """Render the app in the terminal with a simple interactive loop."""
        pages = self._ir_tree.pages
        if not pages:
            console.print("[red]No pages defined.[/red]")
            return

        app_name = self._ir_tree.app_meta.get("name", "PyUI App")
        console.print(
            Panel.fit(
                f"[bold cyan]{app_name}[/bold cyan]",
                box=box.DOUBLE,
                border_style="cyan",
            )
        )

        # Show all pages (for multi-page apps, show them sequentially)
        for page in pages:
            renderable = render_to_rich(page)
            console.print(renderable)
            console.print()

            # Collect interactive buttons on this page
            buttons = self._collect_buttons(page.children)
            if buttons:
                console.print("[dim]Available actions:[/dim]")
                for i, (label, _) in enumerate(buttons, 1):
                    console.print(f"  [cyan]{i}[/cyan]. {label}")
                console.print("  [dim]0. Continue / Skip[/dim]")

                try:
                    choice_str = input("\nEnter action number (0 to skip): ").strip()
                    choice = int(choice_str) if choice_str.isdigit() else 0
                except (EOFError, KeyboardInterrupt):
                    choice = 0

                if 1 <= choice <= len(buttons):
                    _, handler_id = buttons[choice - 1]
                    handler = get_handler(handler_id)
                    if handler:
                        try:
                            handler()
                            console.print("[green]✓ Action executed.[/green]")
                            # Re-render after state change
                            self._ir_tree = build_ir_tree(self.app_class)
                            updated_page = next(
                                (p for p in self._ir_tree.pages if p.route == page.route),
                                page,
                            )
                            console.print(render_to_rich(updated_page))
                        except Exception as exc:
                            console.print(f"[red]Error: {exc}[/red]")


def run_cli_app(app_class: type[App]) -> None:
    """
    Compile *app_class* and render it in the terminal.

    Parameters
    ----------
    app_class : type[App]
        The App subclass to render.
    """
    renderer = CliRenderer(app_class)
    renderer.run()
