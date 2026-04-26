"""Desktop renderer - tkinter backend."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pyui.compiler.ir import IRNode, IRPage, IRTree, build_ir_tree, get_handler
from pyui.utils.logging import get_logger

if TYPE_CHECKING:
    from pyui.app import App

log = get_logger(__name__)

_FONT_FAMILY = "Segoe UI"
_FONT_NORMAL = (_FONT_FAMILY, 10)
_FONT_BOLD = (_FONT_FAMILY, 10, "bold")
_FONT_HEADING = {1: 22, 2: 18, 3: 15, 4: 13, 5: 11, 6: 10}
_BG = "#FFFFFF"
_FG = "#111827"
_FG_MUTED = "#6B7280"
_PRIMARY = "#111827"
_PRIMARY_FG = "#FFFFFF"
_DANGER = "#EF4444"
_SUCCESS = "#10B981"
_WARNING = "#F59E0B"
_INFO = "#3B82F6"
_SURFACE = "#F9FAFB"

_VARIANT_BG: dict[str | None, str] = {
    "primary": _PRIMARY,
    "secondary": "#F3F4F6",
    "ghost": _BG,
    "danger": _DANGER,
    "success": _SUCCESS,
    "warning": _WARNING,
    "info": _INFO,
    None: _PRIMARY,
}
_VARIANT_FG: dict[str | None, str] = {
    "primary": _PRIMARY_FG,
    "secondary": "#1F2937",
    "ghost": "#374151",
    "danger": _PRIMARY_FG,
    "success": _PRIMARY_FG,
    "warning": _PRIMARY_FG,
    "info": _PRIMARY_FG,
    None: _PRIMARY_FG,
}
_SIZE_FONT: dict[str | None, tuple[str, int]] = {
    "xs": (_FONT_FAMILY, 8),
    "sm": (_FONT_FAMILY, 9),
    "md": (_FONT_FAMILY, 10),
    "lg": (_FONT_FAMILY, 12),
    "xl": (_FONT_FAMILY, 14),
    None: (_FONT_FAMILY, 10),
}
_ALERT_COLORS: dict[str, str] = {
    "info": _INFO,
    "success": _SUCCESS,
    "warning": _WARNING,
    "danger": _DANGER,
}


def _try_apply_sv_ttk(root: Any) -> bool:
    try:
        import sv_ttk  # noqa: PLC0415

        sv_ttk.set_theme("light")
        return True
    except ImportError:
        return False


def _build_button(node: IRNode, parent: Any) -> Any:
    import tkinter as tk

    label = str(node.props.get("label", ""))
    variant = node.style_variant
    size = node.props.get("_size")
    disabled = bool(node.props.get("disabled", False))
    bg = _VARIANT_BG.get(variant, _PRIMARY)
    fg = _VARIANT_FG.get(variant, _PRIMARY_FG)
    font = _SIZE_FONT.get(size, _FONT_NORMAL)
    click_handler_id = node.events.get("click")

    def _on_click() -> None:
        if click_handler_id:
            handler = get_handler(click_handler_id)
            if handler:
                try:
                    handler()
                except Exception as exc:
                    log.error("Button handler error", error=str(exc))

    return tk.Button(
        parent,
        text=label,
        bg=bg,
        fg=fg,
        font=font,
        relief="flat",
        padx=12,
        pady=6,
        cursor="hand2",
        command=_on_click,
        state="disabled" if disabled else "normal",
        activebackground=bg,
        activeforeground=fg,
        bd=0,
    )


def _build_text(node: IRNode, parent: Any) -> Any:
    import tkinter as tk

    content = str(node.props.get("content", ""))
    variant = node.style_variant
    size = node.props.get("_size")
    fg = _FG_MUTED if variant == "muted" else _FG
    font = _SIZE_FONT.get(size, _FONT_NORMAL)
    if variant == "code":
        font = ("Courier New", 10)
    lbl = tk.Label(parent, text=content, fg=fg, bg=_BG, font=font, anchor="w", justify="left")
    if node.reactive_props.get("content"):
        from pyui.state.reactive import REACTIVE_VAR_REGISTRY

        for var, name in REACTIVE_VAR_REGISTRY.items():
            if name in node.reactive_bindings:
                def _make_updater(widget: tk.Label) -> Any:
                    def _update(v: Any) -> None:
                        widget.config(text=str(v))
                    return _update
                var.subscribe(_make_updater(lbl))
    return lbl


def _build_heading(node: IRNode, parent: Any) -> Any:
    import tkinter as tk

    text = str(node.props.get("text", ""))
    level = int(node.props.get("level", 1))
    size = _FONT_HEADING.get(level, 14)
    font = (_FONT_FAMILY, size, "bold")
    frame = tk.Frame(parent, bg=_BG)
    tk.Label(frame, text=text, fg=_FG, bg=_BG, font=font, anchor="w").pack(fill="x", side="top")
    subtitle = node.props.get("subtitle")
    if subtitle:
        tk.Label(frame, text=str(subtitle), fg=_FG_MUTED, bg=_BG, font=_FONT_NORMAL).pack(
            fill="x", side="top"
        )
    return frame


def _build_grid(node: IRNode, parent: Any) -> Any:
    import tkinter as tk

    cols = int(node.props.get("cols", 1))
    gap = int(node.props.get("gap", 4))
    pad = max(gap * 2, 2)
    frame = tk.Frame(parent, bg=_BG)
    for i, child in enumerate(node.children):
        row, col = divmod(i, cols)
        cell = tk.Frame(frame, bg=_BG)
        cell.grid(row=row, column=col, padx=pad, pady=pad, sticky="nsew")
        frame.columnconfigure(col, weight=1)
        widget = build_widget(child, cell)
        if widget:
            widget.pack(fill="both", expand=True)
    return frame


def _build_flex(node: IRNode, parent: Any) -> Any:
    import tkinter as tk

    direction = node.props.get("direction", "row")
    gap = int(node.props.get("gap", 4))
    pad = max(gap * 2, 2)
    frame = tk.Frame(parent, bg=_BG)
    side = "left" if direction == "row" else "top"
    fill = "y" if direction == "row" else "x"
    for child in node.children:
        widget = build_widget(child, frame)
        if widget:
            widget.pack(side=side, fill=fill, padx=pad, pady=pad)
    return frame


def _build_stack(node: IRNode, parent: Any) -> Any:
    import tkinter as tk

    direction = node.props.get("direction", "vertical")
    spacing = int(node.props.get("spacing", 4))
    pad = max(spacing * 2, 2)
    frame = tk.Frame(parent, bg=_BG)
    side = "top" if direction == "vertical" else "left"
    fill = "x" if direction == "vertical" else "y"
    for child in node.children:
        widget = build_widget(child, frame)
        if widget:
            widget.pack(side=side, fill=fill, padx=pad, pady=pad)
    return frame


def _build_container(node: IRNode, parent: Any) -> Any:
    import tkinter as tk

    frame = tk.Frame(parent, bg=_BG, padx=16, pady=8)
    for child in node.children:
        widget = build_widget(child, frame)
        if widget:
            widget.pack(fill="x", pady=2)
    return frame


def _build_divider(node: IRNode, parent: Any) -> Any:
    from tkinter import ttk
    from typing import Literal

    direction = node.props.get("direction", "horizontal")
    orient: Literal["horizontal", "vertical"] = "vertical" if direction == "vertical" else "horizontal"
    return ttk.Separator(parent, orient=orient)


def _build_spacer(node: IRNode, parent: Any) -> Any:
    import tkinter as tk

    size = node.props.get("size")
    height = {"xs": 4, "sm": 8, "md": 16, "lg": 32, "xl": 48}.get(str(size) if size else "", 16)
    return tk.Frame(parent, bg=_BG, height=height)


def _build_input(node: IRNode, parent: Any) -> Any:
    import tkinter as tk
    from tkinter import ttk

    placeholder = str(node.props.get("placeholder", ""))
    value = str(node.props.get("value", ""))
    label_text = node.props.get("label")
    input_type = node.props.get("type", "text")
    frame = tk.Frame(parent, bg=_BG)
    if label_text:
        tk.Label(frame, text=str(label_text), fg=_FG, bg=_BG, font=_FONT_BOLD, anchor="w").pack(
            fill="x"
        )
    var = tk.StringVar(value=value)
    show = "*" if input_type == "password" else ""
    entry = ttk.Entry(frame, textvariable=var, show=show)
    entry.pack(fill="x", pady=(2, 0))
    if placeholder and not value:
        entry.insert(0, placeholder)
        entry.config(foreground=_FG_MUTED)

        def _on_focus_in(e: Any) -> None:
            if entry.get() == placeholder:
                entry.delete(0, "end")
                entry.config(foreground=_FG)

        def _on_focus_out(e: Any) -> None:
            if not entry.get():
                entry.insert(0, placeholder)
                entry.config(foreground=_FG_MUTED)

        entry.bind("<FocusIn>", _on_focus_in)
        entry.bind("<FocusOut>", _on_focus_out)
    change_handler_id = node.events.get("change")
    if change_handler_id:

        def _on_change(*_: Any) -> None:
            handler = get_handler(change_handler_id)
            if handler:
                try:
                    handler()
                except Exception as exc:
                    log.error("Input change handler error", error=str(exc))

        var.trace_add("write", _on_change)
    return frame


def _build_textarea(node: IRNode, parent: Any) -> Any:
    import tkinter as tk

    value = str(node.props.get("value", ""))
    rows = int(node.props.get("rows", 4))
    label_text = node.props.get("label")
    frame = tk.Frame(parent, bg=_BG)
    if label_text:
        tk.Label(frame, text=str(label_text), fg=_FG, bg=_BG, font=_FONT_BOLD, anchor="w").pack(
            fill="x"
        )
    text_widget = tk.Text(frame, height=rows, font=_FONT_NORMAL, relief="solid", bd=1)
    text_widget.insert("1.0", value)
    text_widget.pack(fill="x", pady=(2, 0))
    return frame


def _build_select(node: IRNode, parent: Any) -> Any:
    import tkinter as tk
    from tkinter import ttk

    options = node.props.get("options") or []
    selected = node.props.get("value", "")
    label_text = node.props.get("label")
    frame = tk.Frame(parent, bg=_BG)
    if label_text:
        tk.Label(frame, text=str(label_text), fg=_FG, bg=_BG, font=_FONT_BOLD, anchor="w").pack(
            fill="x"
        )
    display_values: list[str] = []
    for opt in options:
        if isinstance(opt, (list, tuple)) and len(opt) >= 2:
            display_values.append(str(opt[1]))
        else:
            display_values.append(str(opt))
    var = tk.StringVar(value=str(selected))
    ttk.Combobox(frame, textvariable=var, values=display_values, state="readonly").pack(
        fill="x", pady=(2, 0)
    )
    return frame


def _build_checkbox(node: IRNode, parent: Any) -> Any:
    import tkinter as tk
    from tkinter import ttk

    checked = bool(node.props.get("checked", False))
    label_text = node.props.get("label", "")
    var = tk.BooleanVar(value=checked)
    cb = ttk.Checkbutton(parent, text=str(label_text), variable=var)
    change_handler_id = node.events.get("change")
    if change_handler_id:

        def _on_change() -> None:
            handler = get_handler(change_handler_id)
            if handler:
                try:
                    handler()
                except Exception as exc:
                    log.error("Checkbox change handler error", error=str(exc))

        var.trace_add("write", lambda *_: _on_change())
    return cb


def _build_toggle(node: IRNode, parent: Any) -> Any:
    import tkinter as tk
    from tkinter import ttk

    checked = bool(node.props.get("checked", False))
    label_text = node.props.get("label", "")
    var = tk.BooleanVar(value=checked)
    return ttk.Checkbutton(parent, text=str(label_text), variable=var)


def _build_slider(node: IRNode, parent: Any) -> Any:
    import tkinter as tk
    from tkinter import ttk

    value = float(node.props.get("value", 0))
    min_val = float(node.props.get("min", 0))
    max_val = float(node.props.get("max", 100))
    label_text = node.props.get("label")
    frame = tk.Frame(parent, bg=_BG)
    if label_text:
        tk.Label(frame, text=str(label_text), fg=_FG, bg=_BG, font=_FONT_BOLD, anchor="w").pack(
            fill="x"
        )
    var = tk.DoubleVar(value=value)
    ttk.Scale(frame, from_=min_val, to=max_val, variable=var, orient="horizontal").pack(
        fill="x", pady=(2, 0)
    )
    return frame


def _build_badge(node: IRNode, parent: Any) -> Any:
    import tkinter as tk

    text = str(node.props.get("text", ""))
    variant = node.style_variant
    bg = _VARIANT_BG.get(variant, "#F3F4F6")
    fg = _VARIANT_FG.get(variant, _FG)
    return tk.Label(parent, text=text, bg=bg, fg=fg, font=(_FONT_FAMILY, 9, "bold"), padx=6, pady=2)


def _build_tag(node: IRNode, parent: Any) -> Any:
    import tkinter as tk

    text = str(node.props.get("text", ""))
    return tk.Label(parent, text=text, bg="#F3F4F6", fg=_FG, font=(_FONT_FAMILY, 9), padx=6, pady=2)


def _build_avatar(node: IRNode, parent: Any) -> Any:
    import tkinter as tk

    name = node.props.get("name", "")
    initials = "".join(p[0] for p in str(name).split()[:2]).upper() if name else "?"
    return tk.Label(
        parent,
        text=initials,
        bg="#E5E7EB",
        fg=_FG,
        font=(_FONT_FAMILY, 10, "bold"),
        width=3,
        height=1,
        relief="flat",
    )


def _build_alert(node: IRNode, parent: Any) -> Any:
    import tkinter as tk

    title = str(node.props.get("title", ""))
    description = node.props.get("description")
    variant = node.style_variant or "info"
    accent = _ALERT_COLORS.get(variant, _INFO)
    frame = tk.Frame(parent, bg=_SURFACE, bd=1, relief="solid", padx=12, pady=10)
    frame.config(highlightbackground=accent, highlightthickness=2)
    tk.Label(frame, text=title, fg=_FG, bg=_SURFACE, font=_FONT_BOLD, anchor="w").pack(fill="x")
    if description:
        tk.Label(
            frame, text=str(description), fg=_FG_MUTED, bg=_SURFACE, font=_FONT_NORMAL, anchor="w"
        ).pack(fill="x")
    return frame


def _build_progress(node: IRNode, parent: Any) -> Any:
    import tkinter as tk
    from tkinter import ttk

    value = float(node.props.get("value", 0))
    label_text = node.props.get("label")
    frame = tk.Frame(parent, bg=_BG)
    if label_text:
        tk.Label(frame, text=str(label_text), fg=_FG, bg=_BG, font=_FONT_NORMAL, anchor="w").pack(
            fill="x"
        )
    ttk.Progressbar(frame, value=value, maximum=100, mode="determinate").pack(fill="x", pady=(2, 0))
    return frame


def _build_spinner(node: IRNode, parent: Any) -> Any:
    from tkinter import ttk

    bar = ttk.Progressbar(parent, mode="indeterminate", length=80)
    bar.start(10)
    return bar


def _build_skeleton(node: IRNode, parent: Any) -> Any:
    import tkinter as tk

    return tk.Frame(parent, bg="#E5E7EB", height=20)


def _build_table(node: IRNode, parent: Any) -> Any:
    import tkinter as tk
    from tkinter import ttk

    headers = node.props.get("headers", [])
    rows = node.props.get("rows", [])
    frame = tk.Frame(parent, bg=_BG)
    tree = ttk.Treeview(frame, columns=headers, show="headings", height=min(len(rows) + 1, 10))
    for col in headers:
        tree.heading(col, text=str(col))
        tree.column(col, width=120, anchor="w")
    for row in rows:
        tree.insert("", "end", values=[str(v) for v in row])
    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    tree.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    return frame


def _build_stat(node: IRNode, parent: Any) -> Any:
    import tkinter as tk

    label = str(node.props.get("label", ""))
    value = str(node.props.get("value", ""))
    trend = node.props.get("trend")
    trend_up = bool(node.props.get("trend_up", True))
    frame = tk.Frame(parent, bg=_SURFACE, padx=16, pady=12, bd=1, relief="solid")
    tk.Label(frame, text=label, fg=_FG_MUTED, bg=_SURFACE, font=(_FONT_FAMILY, 9)).pack(anchor="w")
    tk.Label(frame, text=value, fg=_FG, bg=_SURFACE, font=(_FONT_FAMILY, 22, "bold")).pack(
        anchor="w"
    )
    if trend:
        trend_fg = _SUCCESS if trend_up else _DANGER
        tk.Label(frame, text=str(trend), fg=trend_fg, bg=_SURFACE, font=(_FONT_FAMILY, 9)).pack(
            anchor="w"
        )
    return frame


def _build_nav(node: IRNode, parent: Any) -> Any:
    import tkinter as tk

    items = node.props.get("items", [])
    frame = tk.Frame(parent, bg=_PRIMARY, padx=16, pady=8)
    for item in items:
        label = str(item[0]) if isinstance(item, (list, tuple)) and len(item) >= 2 else str(item)
        tk.Button(
            frame,
            text=label,
            bg=_PRIMARY,
            fg=_PRIMARY_FG,
            font=_FONT_NORMAL,
            relief="flat",
            padx=8,
            pady=4,
            cursor="hand2",
            bd=0,
            activebackground="#374151",
            activeforeground=_PRIMARY_FG,
        ).pack(side="left", padx=4)
    return frame


def _build_tabs(node: IRNode, parent: Any) -> Any:
    import tkinter as tk
    from tkinter import ttk

    tabs_data = node.props.get("tabs", [])
    notebook = ttk.Notebook(parent)
    for tab in tabs_data:
        label = str(tab.get("label", "Tab"))
        children = tab.get("children", [])
        tab_frame = tk.Frame(notebook, bg=_BG, padx=8, pady=8)
        notebook.add(tab_frame, text=label)
        for child in children:
            if isinstance(child, IRNode):
                widget = build_widget(child, tab_frame)
                if widget:
                    widget.pack(fill="x", pady=2)
    return notebook


def _build_form(node: IRNode, parent: Any) -> Any:
    import tkinter as tk

    title = node.props.get("title")
    frame = tk.Frame(parent, bg=_BG, padx=8, pady=8)
    if title:
        tk.Label(frame, text=str(title), fg=_FG, bg=_BG, font=_FONT_BOLD, anchor="w").pack(
            fill="x", pady=(0, 8)
        )
    for child in node.children:
        widget = build_widget(child, frame)
        if widget:
            widget.pack(fill="x", pady=3)
    return frame


def _build_generic_container(node: IRNode, parent: Any) -> Any:
    import tkinter as tk

    frame = tk.Frame(parent, bg=_BG)
    for child in node.children:
        widget = build_widget(child, frame)
        if widget:
            widget.pack(fill="x", pady=2)
    return frame


def _build_raw_html(node: IRNode, parent: Any) -> Any:
    """Render RawHTML as a plain text label (HTML stripped for desktop)."""
    import re
    import tkinter as tk

    html_content = str(node.props.get("html", ""))
    # Strip HTML tags for desktop display
    plain = re.sub(r"<[^>]+>", "", html_content).strip()
    if not plain:
        return tk.Frame(parent, bg=_BG, height=1)
    return tk.Label(
        parent,
        text=plain,
        fg=_FG_MUTED,
        bg=_BG,
        font=_FONT_NORMAL,
        anchor="w",
        justify="left",
        wraplength=600,
    )


_WIDGET_BUILDERS: dict[str, Any] = {
    "button": _build_button,
    "text": _build_text,
    "heading": _build_heading,
    "grid": _build_grid,
    "flex": _build_flex,
    "stack": _build_stack,
    "container": _build_container,
    "divider": _build_divider,
    "spacer": _build_spacer,
    "input": _build_input,
    "textarea": _build_textarea,
    "select": _build_select,
    "checkbox": _build_checkbox,
    "toggle": _build_toggle,
    "slider": _build_slider,
    "badge": _build_badge,
    "tag": _build_tag,
    "avatar": _build_avatar,
    "alert": _build_alert,
    "progress": _build_progress,
    "spinner": _build_spinner,
    "skeleton": _build_skeleton,
    "table": _build_table,
    "stat": _build_stat,
    "nav": _build_nav,
    "tabs": _build_tabs,
    "form": _build_form,
    "sidebar_layout": _build_generic_container,
    "split": _build_generic_container,
    "list": _build_generic_container,
    "raw_html": _build_raw_html,
}


def build_widget(node: IRNode, parent: Any) -> Any:
    """Convert an IRNode into a tkinter widget."""
    builder = _WIDGET_BUILDERS.get(node.type)
    if builder is None:
        import tkinter as tk

        # Use print instead of structlog to avoid PrintLogger.name AttributeError
        print(f"[PyUI Desktop] Unsupported component type: {node.type!r}")
        return tk.Label(parent, text=f"[{node.type}]", fg=_DANGER, bg=_BG, font=_FONT_NORMAL)
    return builder(node, parent)


def build_widget_tree(ir_page: IRPage, parent: Any) -> Any:
    """Build the full widget tree for an IRPage."""
    import tkinter as tk
    from tkinter import ttk

    root_frame = tk.Frame(parent, bg=_BG)
    root_frame.pack(fill="both", expand=True)
    canvas = tk.Canvas(root_frame, bg=_BG, highlightthickness=0)
    scrollbar = ttk.Scrollbar(root_frame, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)
    inner = tk.Frame(canvas, bg=_BG, padx=24, pady=16)
    canvas_window = canvas.create_window((0, 0), window=inner, anchor="nw")

    def _on_configure(event: Any) -> None:
        canvas.configure(scrollregion=canvas.bbox("all"))
        canvas.itemconfig(canvas_window, width=canvas.winfo_width())

    inner.bind("<Configure>", _on_configure)
    canvas.bind("<Configure>", lambda e: canvas.itemconfig(canvas_window, width=e.width))

    def _on_mousewheel(event: Any) -> None:
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    canvas.bind_all("<MouseWheel>", _on_mousewheel)
    for child_node in ir_page.children:
        widget = build_widget(child_node, inner)
        if widget:
            widget.pack(fill="x", pady=4)
    return root_frame


class TkinterRenderer:
    """Renders an IRTree as a native tkinter window."""

    def __init__(self, app_class: type[App]) -> None:
        self.app_class = app_class
        self._ir_tree: IRTree = build_ir_tree(app_class)

    def run(self) -> None:
        import tkinter as tk
        from tkinter import ttk

        root = tk.Tk()
        root.title(self._ir_tree.app_meta.get("name", "PyUI App"))
        root.geometry("1024x768")
        root.configure(bg=_BG)
        root.minsize(640, 480)
        _try_apply_sv_ttk(root)
        pages = self._ir_tree.pages
        if not pages:
            tk.Label(root, text="No pages defined.", fg=_FG_MUTED, bg=_BG).pack(pady=40)
            root.mainloop()
            return
        if len(pages) == 1:
            build_widget_tree(pages[0], root)
        else:
            notebook = ttk.Notebook(root)
            notebook.pack(fill="both", expand=True)
            for page in pages:
                tab_frame = tk.Frame(notebook, bg=_BG)
                notebook.add(tab_frame, text=page.title or page.route)
                build_widget_tree(page, tab_frame)
        root.mainloop()


def run_desktop_app(app_class: type[App]) -> None:
    """Compile app_class and open it as a native desktop window."""
    TkinterRenderer(app_class).run()
