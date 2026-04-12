"""
Web renderer — Tailwind CSS class mappings.

Maps (component_type, variant, size) tuples to Tailwind class strings.
Each renderer function calls ``get_classes()`` to resolve the final
class list for a given IRNode.
"""

from __future__ import annotations

# ── Button ────────────────────────────────────────────────────────────────────

_BUTTON_BASE = (
    "inline-flex items-center justify-center gap-2 rounded-lg font-medium "
    "transition-all duration-150 focus:outline-none focus:ring-2 "
    "focus:ring-offset-2 select-none cursor-pointer"
)

_BUTTON_SIZES: dict[str | None, str] = {
    "xs": "px-2.5 py-1 text-xs",
    "sm": "px-3 py-1.5 text-sm",
    "md": "px-4 py-2 text-sm",
    "lg": "px-5 py-2.5 text-base",
    "xl": "px-6 py-3 text-base",
    None: "px-4 py-2 text-sm",  # default = md
}

_BUTTON_VARIANTS: dict[str | None, str] = {
    "primary": "bg-violet-600 text-white hover:bg-violet-700 focus:ring-violet-500 shadow-sm",
    "secondary": "bg-gray-100 text-gray-900 hover:bg-gray-200 focus:ring-gray-400",
    "ghost": "border border-gray-300 text-gray-700 bg-transparent hover:bg-gray-50 focus:ring-gray-400",
    "danger": "bg-red-600 text-white hover:bg-red-700 focus:ring-red-500 shadow-sm",
    "success": "bg-emerald-600 text-white hover:bg-emerald-700 focus:ring-emerald-500 shadow-sm",
    "link": "text-violet-600 hover:text-violet-700 hover:underline underline-offset-4 p-0 focus:ring-violet-400",
    None: "bg-violet-600 text-white hover:bg-violet-700 focus:ring-violet-500 shadow-sm",
}

_BUTTON_DISABLED = "opacity-50 cursor-not-allowed pointer-events-none"


def button_classes(variant: str | None, size: str | None, disabled: bool = False) -> str:
    classes = [
        _BUTTON_BASE,
        _BUTTON_SIZES.get(size, _BUTTON_SIZES[None]),
        _BUTTON_VARIANTS.get(variant, _BUTTON_VARIANTS[None]),
    ]
    if disabled:
        classes.append(_BUTTON_DISABLED)
    return " ".join(classes)


# ── Text ──────────────────────────────────────────────────────────────────────

_TEXT_VARIANTS: dict[str | None, str] = {
    "muted": "text-gray-500",
    "code": "font-mono text-sm bg-gray-100 px-1.5 py-0.5 rounded text-violet-700",
    "lead": "text-lg text-gray-600 leading-relaxed",
    "small": "text-xs text-gray-500",
    "error": "text-red-600",
    "success": "text-emerald-600",
    None: "text-gray-800",
}

_TEXT_SIZES: dict[str | None, str] = {
    "xs": "text-xs",
    "sm": "text-sm",
    "md": "text-base",
    "lg": "text-lg",
    "xl": "text-xl",
    None: "",
}


def text_classes(variant: str | None, size: str | None, truncate: bool = False) -> str:
    classes = [
        _TEXT_VARIANTS.get(variant, _TEXT_VARIANTS[None]),
        _TEXT_SIZES.get(size, ""),
    ]
    if truncate:
        classes.append("truncate")
    return " ".join(c for c in classes if c)


# ── Heading ───────────────────────────────────────────────────────────────────

_HEADING_LEVEL_CLASSES: dict[int, str] = {
    1: "text-4xl font-bold tracking-tight",
    2: "text-3xl font-bold tracking-tight",
    3: "text-2xl font-semibold",
    4: "text-xl font-semibold",
    5: "text-lg font-medium",
    6: "text-base font-medium",
}

_HEADING_VARIANTS: dict[str | None, str] = {
    "gradient": "bg-gradient-to-r from-violet-600 to-pink-500 bg-clip-text text-transparent",
    "muted": "text-gray-500",
    "display": "text-6xl font-extrabold tracking-tighter",
    None: "text-gray-900",
}


def heading_classes(level: int, variant: str | None) -> str:
    base = _HEADING_LEVEL_CLASSES.get(level, _HEADING_LEVEL_CLASSES[2])
    color = _HEADING_VARIANTS.get(variant, _HEADING_VARIANTS[None])
    return f"{base} {color}"


# ── Grid ──────────────────────────────────────────────────────────────────────

_GRID_COLS: dict[int | str, str] = {
    1: "grid-cols-1",
    2: "grid-cols-2",
    3: "grid-cols-3",
    4: "grid-cols-4",
    5: "grid-cols-5",
    6: "grid-cols-6",
    7: "grid-cols-7",
    8: "grid-cols-8",
    9: "grid-cols-9",
    10: "grid-cols-10",
    11: "grid-cols-11",
    12: "grid-cols-12",
}

_GRID_GAPS: dict[int, str] = {
    0: "gap-0",
    1: "gap-1",
    2: "gap-2",
    3: "gap-3",
    4: "gap-4",
    5: "gap-5",
    6: "gap-6",
    8: "gap-8",
    10: "gap-10",
    12: "gap-12",
}


def grid_classes(cols: int | str, gap: int) -> str:
    col_cls = _GRID_COLS.get(cols, f"grid-cols-{cols}")
    gap_cls = _GRID_GAPS.get(gap, f"gap-{gap}")
    return f"grid {col_cls} {gap_cls}"


# ── Flex ──────────────────────────────────────────────────────────────────────

_FLEX_DIRECTIONS = {
    "row": "flex-row",
    "col": "flex-col",
    "row-reverse": "flex-row-reverse",
    "col-reverse": "flex-col-reverse",
}
_FLEX_ALIGN = {
    "start": "items-start",
    "center": "items-center",
    "end": "items-end",
    "baseline": "items-baseline",
    "stretch": "items-stretch",
}
_FLEX_JUSTIFY = {
    "start": "justify-start",
    "center": "justify-center",
    "end": "justify-end",
    "between": "justify-between",
    "around": "justify-around",
    "evenly": "justify-evenly",
}


def flex_classes(direction: str, align: str, justify: str, gap: int, wrap: bool) -> str:
    dir_cls = _FLEX_DIRECTIONS.get(direction, "flex-row")
    align_cls = _FLEX_ALIGN.get(align, "items-center")
    just_cls = _FLEX_JUSTIFY.get(justify, "justify-start")
    gap_cls = _GRID_GAPS.get(gap, f"gap-{gap}")
    wrap_cls = "flex-wrap" if wrap else "flex-nowrap"
    return f"flex {dir_cls} {align_cls} {just_cls} {gap_cls} {wrap_cls}"


# ── Stack ─────────────────────────────────────────────────────────────────────


def stack_classes(direction: str, spacing: int) -> str:
    dir_cls = "flex-col" if direction == "vertical" else "flex-row"
    gap_cls = _GRID_GAPS.get(spacing, f"gap-{spacing}")
    return f"flex {dir_cls} {gap_cls}"


# ── Container ─────────────────────────────────────────────────────────────────

_CONTAINER_SIZES = {
    "sm": "max-w-screen-sm",
    "md": "max-w-screen-md",
    "lg": "max-w-screen-lg",
    "xl": "max-w-screen-xl",
    "2xl": "max-w-screen-2xl",
    "full": "max-w-full",
}


def container_classes(size: str, centered: bool) -> str:
    size_cls = _CONTAINER_SIZES.get(size, "max-w-screen-xl")
    mx_cls = "mx-auto" if centered else ""
    return f"w-full {size_cls} {mx_cls} px-4"


# ── Divider ───────────────────────────────────────────────────────────────────


def divider_classes(direction: str, has_label: bool) -> str:
    if direction == "vertical":
        return "inline-block flex-shrink-0 w-px h-full bg-gray-200 mx-4 self-stretch"

    if has_label:
        return "relative flex py-5 items-center w-full"

    return "w-full border-t border-gray-200 my-4"


# ── Spacer ────────────────────────────────────────────────────────────────────


def spacer_classes(size: int | None) -> str:
    if size is None:
        return "flex-grow"
    return f"flex-none h-{size} w-{size}"


# ── Badge ─────────────────────────────────────────────────────────────────────

_BADGE_BASE = "inline-flex items-center px-2 py-0.5 rounded text-xs font-medium"
_BADGE_VARIANTS = {
    "primary": "bg-violet-100 text-violet-700",
    "secondary": "bg-gray-100 text-gray-700",
    "success": "bg-emerald-100 text-emerald-700",
    "danger": "bg-red-100 text-red-700",
    "warning": "bg-amber-100 text-amber-700",
    "info": "bg-sky-100 text-sky-700",
    None: "bg-violet-100 text-violet-700",
}


def badge_classes(variant: str | None) -> str:
    return f"{_BADGE_BASE} {_BADGE_VARIANTS.get(variant, _BADGE_VARIANTS[None])}"


# ── Tag ───────────────────────────────────────────────────────────────────────

_TAG_BASE = "inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-sm font-medium border"
_TAG_VARIANTS = {
    "primary": "bg-violet-50 text-violet-700 border-violet-200",
    "secondary": "bg-gray-50 text-gray-700 border-gray-200",
    None: "bg-gray-50 text-gray-700 border-gray-200",
}


def tag_classes(variant: str | None) -> str:
    return f"{_TAG_BASE} {_TAG_VARIANTS.get(variant, _TAG_VARIANTS[None])}"


# ── Avatar ────────────────────────────────────────────────────────────────────

_AVATAR_SIZES = {
    "xs": "h-6 w-6 text-[10px]",
    "sm": "h-8 w-8 text-xs",
    "md": "h-10 w-10 text-sm",
    "lg": "h-12 w-12 text-base",
    "xl": "h-16 w-16 text-xl",
    "2xl": "h-20 w-20 text-2xl",
}


def avatar_classes(size: str) -> str:
    s_cls = _AVATAR_SIZES.get(size, _AVATAR_SIZES["md"])
    return f"{s_cls} relative flex-shrink-0 inline-flex items-center justify-center rounded-full bg-gray-200 text-gray-600 font-bold overflow-hidden"


# ── Icon ──────────────────────────────────────────────────────────────────────


def icon_classes(color: str | None) -> str:
    # We use raw styles for size in the renderer, but can apply colors via Tailwind
    if color is None:
        return "text-current"
    return f"text-{color}"


# ── Image ─────────────────────────────────────────────────────────────────────

_IMAGE_FITS = {
    "cover": "object-cover",
    "contain": "object-contain",
    "fill": "object-fill",
    "none": "object-none",
    "scale-down": "object-scale-down",
}


def image_classes(fit: str | None) -> str:
    fit_cls = _IMAGE_FITS.get(fit or "cover", "object-cover")
    return f"rounded-lg {fit_cls} w-full h-full"


# ── Markdown ──────────────────────────────────────────────────────────────────


def markdown_classes() -> str:
    return "prose prose-violet max-w-none"


# ── Video ─────────────────────────────────────────────────────────────────────


def video_classes() -> str:
    return "rounded-lg w-full aspect-video bg-black shadow-lg overflow-hidden"


# ── Input ─────────────────────────────────────────────────────────────────────

_INPUT_BASE = (
    "block w-full rounded-md border-gray-300 shadow-sm "
    "focus:border-violet-500 focus:ring-violet-500 sm:text-sm "
    "transition-colors duration-150"
)


def input_classes() -> str:
    return _INPUT_BASE


# ── Textarea ──────────────────────────────────────────────────────────────────


def textarea_classes() -> str:
    return _INPUT_BASE


# ── Select ────────────────────────────────────────────────────────────────────


def select_classes() -> str:
    return _INPUT_BASE


# ── Checkbox ──────────────────────────────────────────────────────────────────


def checkbox_classes() -> str:
    return (
        "h-4 w-4 rounded border-gray-300 text-violet-600 "
        "focus:ring-violet-500 transition-colors duration-150"
    )


# ── Toggle (Switch) ───────────────────────────────────────────────────────────


def toggle_classes(checked: bool) -> str:
    bg = "bg-violet-600" if checked else "bg-gray-200"
    return f"{bg} relative inline-flex h-6 w-11 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-violet-500 focus:ring-offset-2"


def toggle_knob_classes(checked: bool) -> str:
    translate = "translate-x-5" if checked else "translate-x-0"
    return f"{translate} pointer-events-none inline-block h-5 w-5 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out"


# ── Slider ────────────────────────────────────────────────────────────────────


def slider_classes() -> str:
    return "w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-violet-600"


# ── DatePicker ────────────────────────────────────────────────────────────────


def datepicker_classes() -> str:
    return _INPUT_BASE


# ── FilePicker ────────────────────────────────────────────────────────────────


def filepicker_classes() -> str:
    return (
        "block w-full text-sm text-gray-500 "
        "file:mr-4 file:py-2 file:px-4 "
        "file:rounded-full file:border-0 "
        "file:text-sm file:font-semibold "
        "file:bg-violet-50 file:text-violet-700 "
        "hover:file:bg-violet-100"
    )


# ── Form ──────────────────────────────────────────────────────────────────────


def form_classes() -> str:
    return "space-y-6 bg-white p-6 rounded-xl shadow-sm border border-gray-100"


# ── Alert ─────────────────────────────────────────────────────────────────────

_ALERT_BASE = "flex p-4 rounded-lg border"
_ALERT_VARIANTS = {
    "info": "bg-blue-50 border-blue-200 text-blue-800",
    "success": "bg-emerald-50 border-emerald-200 text-emerald-800",
    "warning": "bg-amber-50 border-amber-200 text-amber-800",
    "danger": "bg-red-50 border-red-200 text-red-800",
    None: "bg-blue-50 border-blue-200 text-blue-800",
}


def alert_classes(variant: str | None) -> str:
    return f"{_ALERT_BASE} {_ALERT_VARIANTS.get(variant, _ALERT_VARIANTS[None])}"


# ── Toast ─────────────────────────────────────────────────────────────────────


def toast_classes(variant: str | None) -> str:
    # Toasts are fixed-position floating notifications
    base = "fixed bottom-5 right-5 z-50 flex items-center w-full max-w-xs p-4 text-gray-500 bg-white rounded-lg shadow"
    color = "text-violet-600 bg-violet-100" if variant == "primary" else "text-gray-500 bg-gray-100"
    return f"{base} {color}"


# ── Modal ─────────────────────────────────────────────────────────────────────


def modal_overlay_classes() -> str:
    return "fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity z-40 flex items-center justify-center p-4"


def modal_panel_classes() -> str:
    return "relative transform overflow-hidden rounded-lg bg-white text-left shadow-xl transition-all sm:my-8 sm:w-full sm:max-w-lg"


# ── Drawer ────────────────────────────────────────────────────────────────────


def drawer_overlay_classes() -> str:
    return "fixed inset-0 bg-black bg-opacity-50 z-40 transition-opacity"


def drawer_panel_classes(side: str = "right") -> str:
    side_cls = "inset-y-0 right-0 pl-10" if side == "right" else "inset-y-0 left-0 pr-10"
    return f"fixed {side_cls} max-w-full flex z-50 transition-transform"


# ── Tooltip ───────────────────────────────────────────────────────────────────


def tooltip_classes() -> str:
    return "absolute z-50 invisible inline-block px-3 py-2 text-sm font-medium text-white transition-opacity duration-300 bg-gray-900 rounded-lg shadow-sm opacity-0"


# ── Progress ──────────────────────────────────────────────────────────────────


def progress_base_classes() -> str:
    return "w-full bg-gray-200 rounded-full h-2.5 overflow-hidden"


def progress_bar_classes() -> str:
    return "bg-violet-600 h-2.5 rounded-full transition-all duration-300"


# ── Spinner ───────────────────────────────────────────────────────────────────

_SPINNER_SIZES = {
    "xs": "h-3 w-3",
    "sm": "h-4 w-4",
    "md": "h-6 w-6",
    "lg": "h-8 w-8",
    "xl": "h-12 w-12",
}


def spinner_classes(size: str) -> str:
    s_cls = _SPINNER_SIZES.get(size, _SPINNER_SIZES["md"])
    return f"{s_cls} animate-spin text-violet-600"


# ── Skeleton ──────────────────────────────────────────────────────────────────


def skeleton_classes(variant: str) -> str:
    base = "animate-pulse bg-gray-200"
    if variant == "circle":
        return f"{base} rounded-full"
    if variant == "rect":
        return f"{base} rounded-lg"
    return f"{base} rounded h-4 w-full"


# ── Navigation ────────────────────────────────────────────────────────────────


def nav_classes() -> str:
    return "flex items-center space-x-6 text-sm font-medium"


def nav_item_classes(active: bool) -> str:
    base = "transition-colors hover:text-violet-600"
    color = "text-violet-600" if active else "text-gray-600"
    return f"{base} {color}"


def tabs_list_classes() -> str:
    return "flex space-x-1 rounded-xl bg-gray-100 p-1 mb-6 w-fit"


def tab_item_classes(active: bool) -> str:
    base = "w-full rounded-lg py-2 px-6 text-sm font-semibold leading-5 transition-all duration-200 focus:outline-none"
    state = (
        "bg-white text-violet-700 shadow"
        if active
        else "text-gray-500 hover:bg-white/[0.12] hover:text-gray-700"
    )
    return f"{base} {state}"


def breadcrumb_classes() -> str:
    return "flex items-center space-x-2 text-sm text-gray-500"


def pagination_classes() -> str:
    return "flex items-center justify-center space-x-1 mt-8"


def pagination_item_classes(active: bool, disabled: bool = False) -> str:
    base = "flex items-center justify-center px-3 h-8 leading-tight rounded-lg border transition-colors"
    if disabled:
        return f"{base} text-gray-300 bg-gray-50 border-gray-200 cursor-not-allowed"
    if active:
        return f"{base} text-white bg-violet-600 border-violet-600"
    return f"{base} text-gray-500 bg-white border-gray-300 hover:bg-gray-100 hover:text-gray-700 font-medium"


def menu_classes() -> str:
    return "overflow-hidden rounded-lg border border-gray-200 bg-white shadow-lg p-1"


def menu_item_classes() -> str:
    return "flex items-center rounded-md px-3 py-2 text-sm text-gray-700 hover:bg-gray-100 transition-colors"


# ── Data ──────────────────────────────────────────────────────────────────────


def table_base_classes() -> str:
    return "min-w-full divide-y divide-gray-200 border border-gray-100 rounded-lg"


def table_header_classes() -> str:
    return "px-6 py-3 bg-gray-50 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider"


def table_row_classes(striped: bool = False) -> str:
    base = "bg-white hover:bg-gray-50 transition-colors"
    if striped:
        return f"{base} odd:bg-white even:bg-gray-50/50"
    return base


def stat_card_classes() -> str:
    return "overflow-hidden rounded-xl bg-white p-6 shadow-sm border border-gray-100 ring-1 ring-gray-900/5"


def stat_value_classes() -> str:
    return "mt-2 flex items-baseline gap-x-2"


def chart_container_classes() -> str:
    return "w-full h-80 relative bg-white p-4 rounded-xl shadow-sm border border-gray-100"


# ── Page layouts ──────────────────────────────────────────────────────────────

PAGE_LAYOUT_CLASSES: dict[str, str] = {
    "default": "container mx-auto px-4 py-8 max-w-7xl",
    "full-width": "w-full px-4 py-8",
    "sidebar": "flex gap-6 px-4 py-8 max-w-7xl mx-auto",
    "auth": "min-h-screen flex items-center justify-center bg-gray-50 px-4",
}
