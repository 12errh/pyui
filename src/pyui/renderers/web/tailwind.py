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


# ── Page layouts ──────────────────────────────────────────────────────────────

PAGE_LAYOUT_CLASSES: dict[str, str] = {
    "default": "container mx-auto px-4 py-8 max-w-7xl",
    "full-width": "w-full px-4 py-8",
    "sidebar": "flex gap-6 px-4 py-8 max-w-7xl mx-auto",
    "auth": "min-h-screen flex items-center justify-center bg-gray-50 px-4",
}
