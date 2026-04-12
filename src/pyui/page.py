"""
PyUI Page class.

A ``Page`` represents a routable screen within an ``App``. It holds a tree
of components and optional lifecycle hooks.

Example::

    from pyui import Page, Text, Button

    home = Page(title="Home", route="/")
    home.add(
        Text("Welcome!"),
        Button("Get Started").style("primary"),
    )
"""

from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from pyui.components.base import BaseComponent


class Page:
    """
    A routable screen within an App.

    Parameters
    ----------
    title : str
        Page title shown in the browser tab / window title bar.
    route : str
        URL path for web output (e.g. ``"/"``, ``"/about"``).
    layout : str
        Layout preset — one of ``"default"``, ``"full-width"``,
        ``"sidebar"``, ``"auth"``.
    meta : dict
        Extra HTML ``<meta>`` key-value pairs for this page.
    guard : Callable | None
        Optional async function; if it returns ``False`` the router redirects.
    """

    def __init__(
        self,
        title: str = "",
        route: str | None = None,
        layout: str = "default",
        meta: dict[str, str] | None = None,
        guard: Callable[..., Any] | None = None,
    ) -> None:
        self.title = title
        self.route = route
        self.layout = layout
        self.meta: dict[str, str] = meta or {}
        self.guard = guard
        self.children: list[BaseComponent] = []
        self._on_enter: Callable[..., Any] | None = None
        self._on_leave: Callable[..., Any] | None = None

    # ── Child management ─────────────────────────────────────────────────────

    def add(self, *components: BaseComponent) -> Page:
        """Append one or more child components. Returns *self* for chaining."""
        self.children.extend(components)
        return self

    def remove(self, component: BaseComponent) -> Page:
        """Remove a child component."""
        self.children.remove(component)
        return self

    def clear(self) -> Page:
        """Remove all child components."""
        self.children.clear()
        return self

    # ── Lifecycle hooks ───────────────────────────────────────────────────────

    def on_enter(self, handler: Callable[..., Any]) -> Page:
        """Register a callback that fires when the user navigates *to* this page."""
        self._on_enter = handler
        return self

    def on_leave(self, handler: Callable[..., Any]) -> Page:
        """Register a callback that fires when the user navigates *away* from this page."""
        self._on_leave = handler
        return self

    # ── Dunder helpers ────────────────────────────────────────────────────────

    def __repr__(self) -> str:
        return f"Page(title={self.title!r}, route={self.route!r}, children={len(self.children)})"
