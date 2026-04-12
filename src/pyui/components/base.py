"""
BaseComponent — the root of the PyUI component hierarchy.

Every built-in and third-party component inherits from ``BaseComponent``.
All mutating methods return *self* to enable method chaining::

    Button("Save").style("primary").size("lg").disabled(False)
"""

from __future__ import annotations

import uuid
from collections.abc import Callable
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from pyui.state.reactive import ReactiveVar

# Sentinel for "not set"
_UNSET: Any = object()


class BaseComponent:
    """
    Abstract base for all PyUI components.

    Subclasses must set ``component_type`` (e.g. ``"button"``, ``"grid"``).
    """

    component_type: str = "base"

    def __init__(self) -> None:
        # Unique DOM / widget id — overridable via .id()
        self._id: str = f"pyui-{uuid.uuid4().hex[:8]}"

        # Style / layout props
        self._style_variant: str | None = None
        self._size: str | None = None
        self._margin: tuple[Any, ...] = ()
        self._padding: tuple[Any, ...] = ()
        self._width: str | int | None = None
        self._height: str | int | None = None
        self._classes: list[str] = []

        # Visibility / interactivity
        self._hidden: bool | ReactiveVar[bool] = False
        self._disabled: bool | ReactiveVar[bool] = False

        # Event handlers
        self._on_click: Callable[..., Any] | None = None
        self._on_change: Callable[..., Any] | None = None
        self._on_hover: Callable[..., Any] | None = None
        self._on_mount: Callable[..., Any] | None = None
        self._on_unmount: Callable[..., Any] | None = None

        # Children
        self.children: list[BaseComponent] = []

        # Extra arbitrary props (set by subclasses)
        self.props: dict[str, Any] = {}

    # ── Style & layout ────────────────────────────────────────────────────────

    def style(self, variant: str) -> BaseComponent:
        """Set the style variant (e.g. ``"primary"``, ``"ghost"``, ``"danger"``)."""
        self._style_variant = variant
        return self

    def size(self, size: str) -> BaseComponent:
        """Set the size (``"xs"``, ``"sm"``, ``"md"``, ``"lg"``, ``"xl"``)."""
        self._size = size
        return self

    def margin(self, *args: str | int) -> BaseComponent:
        """CSS-style margin shorthand — up to 4 values."""
        self._margin = args
        return self

    def padding(self, *args: str | int) -> BaseComponent:
        """CSS-style padding shorthand — up to 4 values."""
        self._padding = args
        return self

    def width(self, value: str | int) -> BaseComponent:
        """Set width (e.g. ``"100%"``, ``400``, ``"auto"``)."""
        self._width = value
        return self

    def height(self, value: str | int) -> BaseComponent:
        """Set height."""
        self._height = value
        return self

    def className(self, *classes: str) -> BaseComponent:
        """Append raw CSS class names (escape hatch for advanced users)."""
        self._classes.extend(classes)
        return self

    # ── Visibility & state ────────────────────────────────────────────────────

    def hidden(self, condition: bool | ReactiveVar[bool]) -> BaseComponent:
        """
        Hide the component when *condition* is truthy.
        Accepts a plain ``bool`` or a :class:`~pyui.state.reactive.ReactiveVar`.
        """
        self._hidden = condition
        return self

    def disabled(self, condition: bool | ReactiveVar[bool]) -> BaseComponent:
        """Disable the component when *condition* is truthy."""
        self._disabled = condition
        return self

    # ── Identity ──────────────────────────────────────────────────────────────

    def id(self, identifier: str) -> BaseComponent:
        """Override the auto-generated element ID."""
        self._id = identifier
        return self

    # ── Event handlers ────────────────────────────────────────────────────────

    def onClick(self, handler: Callable[..., Any]) -> BaseComponent:  # noqa: N802
        """Register a click handler."""
        self._on_click = handler
        return self

    def onChange(self, handler: Callable[..., Any]) -> BaseComponent:  # noqa: N802
        """Register a change handler (input, select, toggle, etc.)."""
        self._on_change = handler
        return self

    def onHover(self, handler: Callable[..., Any]) -> BaseComponent:  # noqa: N802
        """Register a hover handler."""
        self._on_hover = handler
        return self

    def onMount(self, handler: Callable[..., Any]) -> BaseComponent:  # noqa: N802
        """Register a mount lifecycle handler."""
        self._on_mount = handler
        return self

    def onUnmount(self, handler: Callable[..., Any]) -> BaseComponent:  # noqa: N802
        """Register an unmount lifecycle handler."""
        self._on_unmount = handler
        return self

    # ── Children ─────────────────────────────────────────────────────────────

    def add(self, *children: BaseComponent) -> BaseComponent:
        """Append child components. Returns *self* for chaining."""
        self.children.extend(children)
        return self

    def remove(self, child: BaseComponent) -> BaseComponent:
        """Remove a specific child."""
        self.children.remove(child)
        return self

    def clear(self) -> BaseComponent:
        """Remove all children."""
        self.children.clear()
        return self

    # ── Serialisation helpers ─────────────────────────────────────────────────

    def _collect_events(self) -> dict[str, str]:
        """Return a mapping of event name → handler id (for the IR)."""
        events: dict[str, str] = {}
        if self._on_click is not None:
            events["click"] = id_of(self._on_click)
        if self._on_change is not None:
            events["change"] = id_of(self._on_change)
        if self._on_hover is not None:
            events["hover"] = id_of(self._on_hover)
        if self._on_mount is not None:
            events["mount"] = id_of(self._on_mount)
        if self._on_unmount is not None:
            events["unmount"] = id_of(self._on_unmount)
        return events

    # ── Render (overridden by compiler — not called directly by users) ────────

    def render(self, target: str = "web") -> Any:  # noqa: ARG002
        """
        Called by the compiler to produce an ``IRNode``.
        Default implementation raises; renderers call the IR builder instead.
        """
        raise NotImplementedError(
            f"Component '{self.component_type}' has no render() implementation. "
            "Use pyui.compiler.ir.build_ir_node() instead."
        )

    # ── Dunder helpers ────────────────────────────────────────────────────────

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"id={self._id!r}, "
            f"variant={self._style_variant!r}, "
            f"children={len(self.children)})"
        )


def id_of(handler: Callable[..., Any]) -> str:
    """Return a stable string key for an event handler callable."""
    return f"handler_{id(handler)}"
