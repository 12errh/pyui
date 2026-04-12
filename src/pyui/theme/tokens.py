"""
PyUI theme tokens — the design system foundation.

All theme values are flat dictionaries mapping token keys to values.
Renderers translate these to CSS variables, tkinter style settings,
or Rich styles depending on the target.
"""

from __future__ import annotations

DEFAULT_TOKENS: dict[str, str] = {
    # ── Colors ────────────────────────────────────────────────────────────────
    "color.primary": "#6C63FF",
    "color.primary.hover": "#5A52E0",
    "color.secondary": "#F3F4F6",
    "color.secondary.hover": "#E5E7EB",
    "color.background": "#FFFFFF",
    "color.surface": "#F9FAFB",
    "color.text": "#111827",
    "color.text.muted": "#6B7280",
    "color.border": "#E5E7EB",
    "color.success": "#10B981",
    "color.warning": "#F59E0B",
    "color.danger": "#EF4444",
    "color.info": "#3B82F6",
    # ── Typography ────────────────────────────────────────────────────────────
    "font.family": "Inter, system-ui, sans-serif",
    "font.size.xs": "12px",
    "font.size.sm": "14px",
    "font.size.md": "16px",
    "font.size.lg": "18px",
    "font.size.xl": "24px",
    "font.size.2xl": "32px",
    "font.weight.normal": "400",
    "font.weight.medium": "500",
    "font.weight.bold": "700",
    # ── Spacing (8px base grid) ───────────────────────────────────────────────
    "space.1": "4px",
    "space.2": "8px",
    "space.3": "12px",
    "space.4": "16px",
    "space.6": "24px",
    "space.8": "32px",
    "space.12": "48px",
    "space.16": "64px",
    # ── Shape ─────────────────────────────────────────────────────────────────
    "radius.sm": "4px",
    "radius.md": "8px",
    "radius.lg": "12px",
    "radius.xl": "16px",
    "radius.full": "9999px",
    # ── Shadow ────────────────────────────────────────────────────────────────
    "shadow.sm": "0 1px 2px rgba(0,0,0,0.05)",
    "shadow.md": "0 4px 6px rgba(0,0,0,0.07)",
    "shadow.lg": "0 10px 15px rgba(0,0,0,0.10)",
    # ── Animation ─────────────────────────────────────────────────────────────
    "transition.fast": "100ms ease",
    "transition.normal": "200ms ease",
    "transition.slow": "300ms ease",
}

# ── Built-in theme overrides ──────────────────────────────────────────────────

DARK_OVERRIDES: dict[str, str] = {
    "color.primary": "#7C73FF",
    "color.primary.hover": "#6A61F0",
    "color.background": "#0F172A",
    "color.surface": "#1E293B",
    "color.text": "#F1F5F9",
    "color.text.muted": "#94A3B8",
    "color.border": "#334155",
    "color.secondary": "#1E293B",
}

OCEAN_OVERRIDES: dict[str, str] = {
    "color.primary": "#0EA5E9",
    "color.primary.hover": "#0284C7",
    "color.background": "#F0F9FF",
    "color.surface": "#E0F2FE",
    "color.text": "#0C4A6E",
    "color.text.muted": "#0369A1",
    "color.border": "#BAE6FD",
}

SUNSET_OVERRIDES: dict[str, str] = {
    "color.primary": "#F97316",
    "color.primary.hover": "#EA580C",
    "color.background": "#FFF7ED",
    "color.surface": "#FFEDD5",
    "color.text": "#431407",
    "color.text.muted": "#9A3412",
    "color.border": "#FDBA74",
}

FOREST_OVERRIDES: dict[str, str] = {
    "color.primary": "#10B981",
    "color.primary.hover": "#059669",
    "color.background": "#F0FDF4",
    "color.surface": "#DCFCE7",
    "color.text": "#052E16",
    "color.text.muted": "#166534",
    "color.border": "#86EFAC",
}

ROSE_OVERRIDES: dict[str, str] = {
    "color.primary": "#F43F5E",
    "color.primary.hover": "#E11D48",
    "color.background": "#FFF1F2",
    "color.surface": "#FFE4E6",
    "color.text": "#4C0519",
    "color.text.muted": "#9F1239",
    "color.border": "#FECDD3",
}

BUILT_IN_THEMES: dict[str, dict[str, str]] = {
    "light": {},
    "dark": DARK_OVERRIDES,
    "ocean": OCEAN_OVERRIDES,
    "sunset": SUNSET_OVERRIDES,
    "forest": FOREST_OVERRIDES,
    "rose": ROSE_OVERRIDES,
}
