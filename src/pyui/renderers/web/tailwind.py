"""
Web renderer — Tailwind CSS class mappings.

Design philosophy: premium design-agency quality.
Every component is crafted to the standard of Linear, Vercel, Stripe, Resend.
Sharp edges, intentional whitespace, refined typography, subtle depth.
"""

from __future__ import annotations

# ── Button ────────────────────────────────────────────────────────────────────
# Tight tracking, sharp corners on primary, pill on ghost/secondary.
# Micro-interactions via scale + shadow lift.

_BUTTON_BASE = (
    "inline-flex items-center justify-center gap-2 font-medium tracking-tight "
    "transition-all duration-200 ease-out focus-visible:outline-none "
    "focus-visible:ring-2 focus-visible:ring-offset-2 select-none cursor-pointer "
    "active:scale-[0.97]"
)

_BUTTON_SIZES: dict[str | None, str] = {
    "xs": "h-7 px-3 text-xs rounded-md",
    "sm": "h-8 px-3.5 text-sm rounded-lg",
    "md": "h-9 px-4 text-sm rounded-lg",
    "lg": "h-11 px-6 text-base rounded-xl",
    "xl": "h-12 px-8 text-base rounded-xl",
    None: "h-9 px-4 text-sm rounded-lg",
}

_BUTTON_VARIANTS: dict[str | None, str] = {
    # Solid black — the primary action. Confident, no-nonsense.
    "primary": (
        "bg-gray-950 text-white shadow-sm "
        "hover:bg-gray-800 hover:shadow-md hover:-translate-y-px "
        "focus-visible:ring-gray-950"
    ),
    # Soft fill — secondary actions, less visual weight.
    "secondary": (
        "bg-gray-100 text-gray-800 "
        "hover:bg-gray-200 hover:-translate-y-px "
        "focus-visible:ring-gray-400"
    ),
    # Outlined — tertiary, ghost-like but with clear boundary.
    "ghost": (
        "border border-gray-200 bg-white text-gray-700 shadow-sm "
        "hover:bg-gray-50 hover:border-gray-300 hover:-translate-y-px "
        "focus-visible:ring-gray-300"
    ),
    # Danger — destructive actions. Red, but not alarming.
    "danger": (
        "bg-red-500 text-white shadow-sm "
        "hover:bg-red-600 hover:shadow-md hover:-translate-y-px "
        "focus-visible:ring-red-500"
    ),
    # Success — confirmation actions.
    "success": (
        "bg-emerald-500 text-white shadow-sm "
        "hover:bg-emerald-600 hover:-translate-y-px "
        "focus-visible:ring-emerald-500"
    ),
    # Link — inline text action, no chrome.
    "link": (
        "text-gray-900 underline underline-offset-4 decoration-gray-300 p-0 h-auto "
        "hover:decoration-gray-900 focus-visible:ring-gray-400"
    ),
    # Gradient — hero CTAs, high-impact moments.
    "gradient": (
        "bg-gradient-to-r from-violet-600 via-purple-600 to-indigo-600 text-white shadow-lg "
        "shadow-violet-500/25 hover:shadow-violet-500/40 hover:-translate-y-0.5 "
        "focus-visible:ring-violet-500"
    ),
    None: (
        "bg-gray-950 text-white shadow-sm "
        "hover:bg-gray-800 hover:shadow-md hover:-translate-y-px "
        "focus-visible:ring-gray-950"
    ),
}

_BUTTON_DISABLED = "opacity-40 cursor-not-allowed pointer-events-none saturate-0"


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
# Refined typographic scale. Muted uses a warm gray, not cold.
# Code blocks have a subtle inset look with a left accent.

_TEXT_VARIANTS: dict[str | None, str] = {
    "muted": "text-gray-500 leading-relaxed",
    "code": (
        "font-mono text-[13px] bg-gray-50 border border-gray-200 "
        "px-1.5 py-0.5 rounded-md text-gray-800 tracking-tight"
    ),
    "lead": "text-lg text-gray-600 leading-[1.75] font-light",
    "small": "text-xs text-gray-500 tracking-wide",
    "error": "text-red-500 text-sm",
    "success": "text-emerald-600 text-sm",
    "caption": "text-xs text-gray-400 uppercase tracking-widest font-medium",
    None: "text-gray-700 leading-relaxed",
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
# Tight tracking on large sizes. Balanced weight progression.
# Gradient variant uses a rich multi-stop for depth.

_HEADING_LEVEL_CLASSES: dict[int, str] = {
    1: "text-4xl font-bold tracking-[-0.03em] leading-[1.1]",
    2: "text-3xl font-bold tracking-[-0.02em] leading-[1.2]",
    3: "text-2xl font-semibold tracking-[-0.015em] leading-[1.3]",
    4: "text-xl font-semibold tracking-tight leading-snug",
    5: "text-lg font-medium tracking-tight",
    6: "text-base font-medium tracking-tight",
}

_HEADING_VARIANTS: dict[str | None, str] = {
    # Rich violet → indigo gradient — premium, not garish
    "gradient": (
        "bg-gradient-to-br from-gray-900 via-violet-800 to-indigo-700 "
        "bg-clip-text text-transparent"
    ),
    "muted": "text-gray-400 font-normal",
    # Display: editorial, oversized
    "display": "text-6xl font-extrabold tracking-[-0.04em] leading-[0.95]",
    # Mono: terminal / code aesthetic
    "mono": "font-mono text-gray-900 tracking-tight",
    None: "text-gray-950",
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


# ── Badge ─────────────────────────────────────────────────────────────────────
# Pill shape, tight tracking, subtle dot indicator feel.
# Each variant has a distinct but harmonious palette.

_BADGE_BASE = (
    "inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full "
    "text-xs font-medium tracking-wide border"
)
_BADGE_VARIANTS = {
    "primary":   "bg-violet-50 text-violet-700 border-violet-200/80",
    "secondary": "bg-gray-50 text-gray-600 border-gray-200",
    "success":   "bg-emerald-50 text-emerald-700 border-emerald-200/80",
    "danger":    "bg-red-50 text-red-600 border-red-200/80",
    "warning":   "bg-amber-50 text-amber-700 border-amber-200/80",
    "info":      "bg-sky-50 text-sky-700 border-sky-200/80",
    "dark":      "bg-gray-900 text-gray-100 border-gray-800",
    None:        "bg-violet-50 text-violet-700 border-violet-200/80",
}


def badge_classes(variant: str | None) -> str:
    return f"{_BADGE_BASE} {_BADGE_VARIANTS.get(variant, _BADGE_VARIANTS[None])}"


# ── Tag ───────────────────────────────────────────────────────────────────────
# Slightly larger than badge, used for categorization.
# Rounded-full with a clean border — no background noise.

_TAG_BASE = (
    "inline-flex items-center gap-1.5 px-3 py-1 rounded-full "
    "text-sm font-medium border transition-colors duration-150"
)
_TAG_VARIANTS = {
    "primary":   "bg-violet-50 text-violet-700 border-violet-200 hover:bg-violet-100",
    "secondary": "bg-white text-gray-600 border-gray-200 hover:bg-gray-50",
    "success":   "bg-emerald-50 text-emerald-700 border-emerald-200 hover:bg-emerald-100",
    "danger":    "bg-red-50 text-red-600 border-red-200 hover:bg-red-100",
    None:        "bg-white text-gray-600 border-gray-200 hover:bg-gray-50",
}


def tag_classes(variant: str | None) -> str:
    return f"{_TAG_BASE} {_TAG_VARIANTS.get(variant, _TAG_VARIANTS[None])}"


# ── Avatar ────────────────────────────────────────────────────────────────────
# Ring on hover, warm gray fallback, precise size scale.

_AVATAR_SIZES = {
    "xs":  "h-6 w-6 text-[9px]",
    "sm":  "h-8 w-8 text-[11px]",
    "md":  "h-10 w-10 text-sm",
    "lg":  "h-12 w-12 text-base",
    "xl":  "h-16 w-16 text-xl",
    "2xl": "h-20 w-20 text-2xl",
}


def avatar_classes(size: str) -> str:
    s_cls = _AVATAR_SIZES.get(size, _AVATAR_SIZES["md"])
    return (
        f"{s_cls} relative flex-shrink-0 inline-flex items-center justify-center "
        "rounded-full bg-gradient-to-br from-gray-100 to-gray-200 "
        "text-gray-600 font-semibold overflow-hidden "
        "ring-2 ring-white shadow-sm"
    )


# ── Icon ──────────────────────────────────────────────────────────────────────


def icon_classes(color: str | None) -> str:
    # We use raw styles for size in the renderer, but can apply colors via Tailwind
    if color is None:
        return "text-current"
    return f"text-{color}"


# ── Image ─────────────────────────────────────────────────────────────────────
# Rounded corners, subtle shadow, overflow hidden for clean edges.

_IMAGE_FITS = {
    "cover":      "object-cover",
    "contain":    "object-contain",
    "fill":       "object-fill",
    "none":       "object-none",
    "scale-down": "object-scale-down",
}


def image_classes(fit: str | None) -> str:
    fit_cls = _IMAGE_FITS.get(fit or "cover", "object-cover")
    return f"rounded-2xl {fit_cls} w-full h-full shadow-sm"


# ── Markdown ──────────────────────────────────────────────────────────────────
# Prose with tighter line-height and refined link colors.

def markdown_classes() -> str:
    return (
        "prose prose-gray max-w-none "
        "prose-headings:tracking-tight prose-headings:font-semibold "
        "prose-a:text-violet-600 prose-a:no-underline hover:prose-a:underline "
        "prose-code:text-gray-800 prose-code:bg-gray-100 prose-code:rounded "
        "prose-code:px-1 prose-code:py-0.5 prose-code:text-sm prose-code:font-normal "
        "prose-pre:bg-gray-950 prose-pre:text-gray-100 prose-pre:rounded-xl"
    )


# ── Video ─────────────────────────────────────────────────────────────────────

def video_classes() -> str:
    return "rounded-2xl w-full aspect-video bg-gray-950 shadow-xl overflow-hidden"


# ── Input ─────────────────────────────────────────────────────────────────────
# Floating-label feel via placeholder-shown. Clean border, sharp focus ring.
# No box-shadow on default — only on focus. Matches Linear's input style.

_INPUT_BASE = (
    "block w-full rounded-xl border border-gray-200 bg-white px-3.5 py-2.5 "
    "text-sm text-gray-900 placeholder:text-gray-400 "
    "shadow-sm transition-all duration-150 "
    "focus:outline-none focus:border-gray-400 focus:ring-2 focus:ring-gray-900/10 "
    "hover:border-gray-300"
)


def input_classes() -> str:
    return _INPUT_BASE


# ── Textarea ──────────────────────────────────────────────────────────────────

def textarea_classes() -> str:
    return (
        "block w-full rounded-xl border border-gray-200 bg-white px-3.5 py-2.5 "
        "text-sm text-gray-900 placeholder:text-gray-400 "
        "shadow-sm transition-all duration-150 resize-y min-h-[100px] "
        "focus:outline-none focus:border-gray-400 focus:ring-2 focus:ring-gray-900/10 "
        "hover:border-gray-300"
    )


# ── Select ────────────────────────────────────────────────────────────────────

def select_classes() -> str:
    return (
        "block w-full rounded-xl border border-gray-200 bg-white px-3.5 py-2.5 "
        "text-sm text-gray-900 shadow-sm transition-all duration-150 "
        "focus:outline-none focus:border-gray-400 focus:ring-2 focus:ring-gray-900/10 "
        "hover:border-gray-300 cursor-pointer appearance-none "
        "bg-[url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 20 20'%3E%3Cpath stroke='%236b7280' stroke-linecap='round' stroke-linejoin='round' stroke-width='1.5' d='M6 8l4 4 4-4'/%3E%3C/svg%3E\")] "
        "bg-[position:right_12px_center] bg-[size:16px] bg-no-repeat pr-10"
    )


# ── Checkbox ──────────────────────────────────────────────────────────────────
# Larger hit area, sharp corners, strong checked state.

def checkbox_classes() -> str:
    return (
        "h-4 w-4 rounded border-gray-300 bg-white text-gray-900 shadow-sm "
        "transition-all duration-150 cursor-pointer "
        "focus:ring-2 focus:ring-gray-900/20 focus:ring-offset-1 "
        "checked:bg-gray-900 checked:border-gray-900"
    )


# ── Toggle (Switch) ───────────────────────────────────────────────────────────
# Smooth, satisfying. Dark checked state. Pill shape.

def toggle_classes(checked: bool) -> str:
    bg = "bg-gray-900" if checked else "bg-gray-200"
    return (
        f"{bg} relative inline-flex h-6 w-11 flex-shrink-0 cursor-pointer "
        "rounded-full border-2 border-transparent shadow-inner "
        "transition-colors duration-200 ease-in-out "
        "focus:outline-none focus:ring-2 focus:ring-gray-900/20 focus:ring-offset-2"
    )


def toggle_knob_classes(checked: bool) -> str:
    translate = "translate-x-5" if checked else "translate-x-0"
    return (
        f"{translate} pointer-events-none inline-block h-5 w-5 transform "
        "rounded-full bg-white shadow-md ring-0 transition-transform duration-200 ease-in-out"
    )


# ── Slider ────────────────────────────────────────────────────────────────────
# Thin track, dark thumb. Clean and precise.

def slider_classes() -> str:
    return (
        "w-full h-1.5 bg-gray-200 rounded-full appearance-none cursor-pointer "
        "accent-gray-900 transition-all duration-150 "
        "[&::-webkit-slider-thumb]:w-4 [&::-webkit-slider-thumb]:h-4 "
        "[&::-webkit-slider-thumb]:rounded-full [&::-webkit-slider-thumb]:bg-gray-900 "
        "[&::-webkit-slider-thumb]:shadow-sm [&::-webkit-slider-thumb]:appearance-none"
    )


# ── DatePicker ────────────────────────────────────────────────────────────────

def datepicker_classes() -> str:
    return (
        "block w-full rounded-xl border border-gray-200 bg-white px-3.5 py-2.5 "
        "text-sm text-gray-900 shadow-sm transition-all duration-150 "
        "focus:outline-none focus:border-gray-400 focus:ring-2 focus:ring-gray-900/10 "
        "hover:border-gray-300 cursor-pointer"
    )


# ── FilePicker ────────────────────────────────────────────────────────────────

def filepicker_classes() -> str:
    return (
        "block w-full text-sm text-gray-500 cursor-pointer "
        "file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 "
        "file:text-sm file:font-medium file:bg-gray-900 file:text-white "
        "file:cursor-pointer file:transition-colors file:duration-150 "
        "hover:file:bg-gray-700"
    )


# ── Form ──────────────────────────────────────────────────────────────────────
# Card-like container. Clean white, subtle border, generous padding.

def form_classes() -> str:
    return (
        "space-y-5 bg-white p-8 rounded-2xl "
        "shadow-[0_1px_3px_rgba(0,0,0,0.06),0_1px_2px_rgba(0,0,0,0.04)] "
        "border border-gray-100"
    )


# ── Alert ─────────────────────────────────────────────────────────────────────
# Left accent border — a design pattern used by Stripe, Linear, Notion.
# Clean white background, colored left border, icon-friendly layout.

_ALERT_BASE = "flex gap-3 p-4 rounded-xl border-l-4 bg-white shadow-sm border border-gray-100"
_ALERT_VARIANTS = {
    "info":    "border-l-sky-500 [&_.alert-icon]:text-sky-500 [&_.alert-title]:text-sky-900 [&_.alert-body]:text-sky-700",
    "success": "border-l-emerald-500 [&_.alert-icon]:text-emerald-500 [&_.alert-title]:text-emerald-900 [&_.alert-body]:text-emerald-700",
    "warning": "border-l-amber-500 [&_.alert-icon]:text-amber-500 [&_.alert-title]:text-amber-900 [&_.alert-body]:text-amber-700",
    "danger":  "border-l-red-500 [&_.alert-icon]:text-red-500 [&_.alert-title]:text-red-900 [&_.alert-body]:text-red-700",
    None:      "border-l-sky-500 [&_.alert-icon]:text-sky-500 [&_.alert-title]:text-sky-900 [&_.alert-body]:text-sky-700",
}


def alert_classes(variant: str | None) -> str:
    return f"{_ALERT_BASE} {_ALERT_VARIANTS.get(variant, _ALERT_VARIANTS[None])}"


# ── Toast ─────────────────────────────────────────────────────────────────────
# Floating card with strong shadow. Dark background for contrast.
# Positioned bottom-right, max-width constrained.

def toast_classes(variant: str | None) -> str:
    base = (
        "fixed bottom-6 right-6 z-50 flex items-start gap-3 w-full max-w-sm "
        "p-4 rounded-2xl shadow-[0_8px_30px_rgba(0,0,0,0.12)] "
        "border border-gray-100 bg-white backdrop-blur-sm"
    )
    accent = {
        "primary": "border-l-4 border-l-violet-500",
        "success": "border-l-4 border-l-emerald-500",
        "danger":  "border-l-4 border-l-red-500",
        "warning": "border-l-4 border-l-amber-500",
    }
    return f"{base} {accent.get(variant or '', '')}"


# ── Modal ─────────────────────────────────────────────────────────────────────
# Frosted glass overlay. Panel with generous padding and strong shadow.

def modal_overlay_classes() -> str:
    return (
        "fixed inset-0 bg-gray-950/60 backdrop-blur-sm z-40 "
        "transition-opacity duration-200"
    )


def modal_panel_classes() -> str:
    return (
        "relative w-full max-w-lg bg-white rounded-2xl "
        "shadow-[0_25px_60px_rgba(0,0,0,0.15)] "
        "border border-gray-100 overflow-hidden"
    )


# ── Drawer ────────────────────────────────────────────────────────────────────
# Slides in from the side. Frosted overlay, clean panel.

def drawer_overlay_classes() -> str:
    return "fixed inset-0 bg-gray-950/50 backdrop-blur-sm z-40 transition-opacity duration-300"


def drawer_panel_classes(side: str = "right") -> str:
    side_cls = "inset-y-0 right-0" if side == "right" else "inset-y-0 left-0"
    return (
        f"fixed {side_cls} w-full max-w-md bg-white z-50 "
        "shadow-[0_0_60px_rgba(0,0,0,0.15)] "
        "flex flex-col"
    )


# ── Tooltip ───────────────────────────────────────────────────────────────────
# Dark, compact, sharp. Appears above the target.

def tooltip_classes() -> str:
    return (
        "absolute z-50 bottom-full left-1/2 -translate-x-1/2 mb-2 "
        "px-2.5 py-1.5 rounded-lg text-xs font-medium text-white "
        "bg-gray-950 shadow-lg whitespace-nowrap pointer-events-none "
        "opacity-0 invisible transition-all duration-150 "
        "group-hover:opacity-100 group-hover:visible"
    )


# ── Progress ──────────────────────────────────────────────────────────────────
# Thin, elegant. Gradient fill for visual interest.

def progress_base_classes() -> str:
    return "w-full bg-gray-100 rounded-full h-1.5 overflow-hidden"


def progress_bar_classes() -> str:
    return (
        "h-1.5 rounded-full transition-all duration-500 ease-out "
        "bg-gradient-to-r from-gray-700 to-gray-900"
    )


# ── Spinner ───────────────────────────────────────────────────────────────────
# Dual-ring style — outer ring faint, inner arc dark.

_SPINNER_SIZES = {
    "xs": "h-3 w-3",
    "sm": "h-4 w-4",
    "md": "h-6 w-6",
    "lg": "h-8 w-8",
    "xl": "h-12 w-12",
}


def spinner_classes(size: str) -> str:
    s_cls = _SPINNER_SIZES.get(size, _SPINNER_SIZES["md"])
    return f"{s_cls} animate-spin text-gray-900"


# ── Skeleton ──────────────────────────────────────────────────────────────────
# Shimmer animation instead of plain pulse. More premium feel.

def skeleton_classes(variant: str) -> str:
    base = "skeleton-shimmer"
    if variant == "circle":
        return f"{base} rounded-full"
    if variant == "rect":
        return f"{base} rounded-xl"
    return f"{base} rounded-lg h-4 w-full"


# ── Navigation ────────────────────────────────────────────────────────────────
# Nav: clean horizontal links, no underlines by default.
# Tabs: pill-style active state on a muted track — like Linear's tabs.
# Breadcrumb: slash-separated, muted with active final item.
# Pagination: bordered items, strong active state.
# Menu: floating card with hover rows.

def nav_classes() -> str:
    return "flex items-center gap-1 text-sm font-medium"


def nav_item_classes(active: bool) -> str:
    base = "px-3 py-1.5 rounded-lg transition-colors duration-150"
    if active:
        return f"{base} bg-gray-100 text-gray-900 font-semibold"
    return f"{base} text-gray-500 hover:text-gray-900 hover:bg-gray-50"


def tabs_list_classes() -> str:
    return (
        "inline-flex items-center gap-0.5 rounded-xl bg-gray-100/80 p-1 mb-6"
    )


def tab_item_classes(active: bool) -> str:
    base = "rounded-lg py-1.5 px-5 text-sm font-medium leading-5 transition-all duration-200 focus:outline-none"
    if active:
        return f"{base} bg-white text-gray-900 shadow-sm shadow-gray-200/80"
    return f"{base} text-gray-500 hover:text-gray-700 hover:bg-white/50"


def breadcrumb_classes() -> str:
    return "flex items-center gap-1.5 text-sm"


def pagination_classes() -> str:
    return "flex items-center justify-center gap-1 mt-8"


def pagination_item_classes(active: bool, disabled: bool = False) -> str:
    base = (
        "flex items-center justify-center w-9 h-9 rounded-xl text-sm "
        "font-medium border transition-all duration-150"
    )
    if disabled:
        return f"{base} text-gray-300 bg-white border-gray-100 cursor-not-allowed"
    if active:
        return f"{base} text-white bg-gray-900 border-gray-900 shadow-sm"
    return f"{base} text-gray-600 bg-white border-gray-200 hover:bg-gray-50 hover:border-gray-300"


def menu_classes() -> str:
    return (
        "overflow-hidden rounded-xl border border-gray-100 bg-white "
        "shadow-[0_8px_30px_rgba(0,0,0,0.08)] p-1.5 min-w-[180px]"
    )


def menu_item_classes() -> str:
    return (
        "flex items-center gap-2.5 rounded-lg px-3 py-2 text-sm text-gray-700 "
        "hover:bg-gray-50 hover:text-gray-900 transition-colors duration-100 cursor-pointer"
    )


# ── Data ──────────────────────────────────────────────────────────────────────
# Table: clean, no outer border noise. Header is barely-there gray.
# Stat card: large number, tight label, trend indicator.
# Chart: white card, generous padding, rounded corners.

def table_base_classes() -> str:
    return "min-w-full divide-y divide-gray-100"


def table_header_classes() -> str:
    return (
        "px-5 py-3 text-left text-xs font-semibold text-gray-400 "
        "uppercase tracking-widest bg-gray-50/80"
    )


def table_row_classes(striped: bool = False) -> str:
    base = "transition-colors duration-100 hover:bg-gray-50/60"
    if striped:
        return f"{base} odd:bg-white even:bg-gray-50/40"
    return f"{base} bg-white"


def stat_card_classes() -> str:
    return (
        "relative overflow-hidden rounded-2xl bg-white p-6 "
        "shadow-[0_1px_3px_rgba(0,0,0,0.06),0_1px_2px_rgba(0,0,0,0.04)] "
        "border border-gray-100 transition-shadow duration-200 hover:shadow-md"
    )


def stat_value_classes() -> str:
    return "mt-2 flex items-baseline gap-2"


def chart_container_classes() -> str:
    return (
        "w-full h-80 relative bg-white p-5 rounded-2xl "
        "shadow-[0_1px_3px_rgba(0,0,0,0.06),0_1px_2px_rgba(0,0,0,0.04)] "
        "border border-gray-100"
    )


# ── Page layouts ──────────────────────────────────────────────────────────────

PAGE_LAYOUT_CLASSES: dict[str, str] = {
    "default":    "container mx-auto px-6 py-10 max-w-7xl",
    "full-width": "w-full",
    "sidebar":    "flex gap-8 px-6 py-10 max-w-7xl mx-auto",
    "auth":       "min-h-screen flex items-center justify-center bg-gray-50 px-4",
}


# ── Container ─────────────────────────────────────────────────────────────────
# Slightly more generous padding than before.

_CONTAINER_SIZES = {
    "sm":   "max-w-screen-sm",
    "md":   "max-w-screen-md",
    "lg":   "max-w-screen-lg",
    "xl":   "max-w-screen-xl",
    "2xl":  "max-w-screen-2xl",
    "6xl":  "max-w-[1400px]",
    "full": "max-w-full",
}


def container_classes(size: str, centered: bool) -> str:
    size_cls = _CONTAINER_SIZES.get(size, "max-w-screen-xl")
    mx_cls = "mx-auto" if centered else ""
    return f"w-full {size_cls} {mx_cls} px-6"


# ── Divider ───────────────────────────────────────────────────────────────────
# Hairline — barely visible, just enough to separate.

def divider_classes(direction: str, has_label: bool) -> str:
    if direction == "vertical":
        return "inline-block flex-shrink-0 w-px self-stretch bg-gray-100 mx-3"
    if has_label:
        return "relative flex items-center py-4 w-full"
    return "w-full border-t border-gray-100 my-6"


# ── Spacer ────────────────────────────────────────────────────────────────────

def spacer_classes(size: int | None) -> str:
    if size is None:
        return "flex-grow"
    return f"flex-none h-{size} w-{size}"
