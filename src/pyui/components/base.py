"""
BaseComponent — the root of the PyUI component hierarchy.

Every built-in and third-party component inherits from ``BaseComponent``.
All mutating methods return *self* to enable method chaining::

    Button("Save").style("primary").size("lg").disabled(False)
"""

from __future__ import annotations

import uuid
from collections.abc import Callable
from typing import TYPE_CHECKING, Any, TypeVar

if TYPE_CHECKING:
    from pyui.state.reactive import ReactiveVar

_T = TypeVar("_T", bound="BaseComponent")

# Sentinel for "not set"
_UNSET: Any = object()

# Global stack of active containers (BaseComponent or Page)
_CONTEXT_STACK: list[Any] = []


class BaseComponent:
    """
    Abstract base for all PyUI components.

    Subclasses must set ``component_type`` (e.g. ``"button"``, ``"grid"``).
    """

    component_type: str = "base"

    def __init__(self) -> None:
        self._id: str = f"pyui-{uuid.uuid4().hex[:8]}"
        self._style_variant: str | None = None
        self._size: str | None = None
        self._margin: tuple[Any, ...] = ()
        self._padding: tuple[Any, ...] = ()
        self._width: str | int | None = None
        self._height: str | int | None = None
        self._classes: list[str] = []
        self._hidden: bool | ReactiveVar[bool] = False
        self._disabled: bool | ReactiveVar[bool] = False
        self._on_click: Callable[..., Any] | None = None
        self._on_change: Callable[..., Any] | None = None
        self._on_hover: Callable[..., Any] | None = None
        self._on_mount: Callable[..., Any] | None = None
        self._on_unmount: Callable[..., Any] | None = None
        self.children: list[BaseComponent] = []

        if _CONTEXT_STACK:
            parent = _CONTEXT_STACK[-1]
            if hasattr(parent, "add"):
                parent.add(self)

        self.props: dict[str, Any] = {}

    # ── Style & layout ────────────────────────────────────────────────────────

    def style(self: _T, variant: str) -> _T:
        """Set the style variant (e.g. ``"primary"``, ``"ghost"``, ``"danger"``)."""
        self._style_variant = variant
        return self

    def size(self: _T, size: str) -> _T:
        """Set the size (``"xs"``, ``"sm"``, ``"md"``, ``"lg"``, ``"xl"``)."""
        self._size = size
        return self

    def margin(self: _T, *args: str | int) -> _T:
        """CSS-style margin shorthand — up to 4 values."""
        self._margin = args
        return self

    def padding(self: _T, *args: str | int) -> _T:
        """CSS-style padding shorthand — up to 4 values."""
        self._padding = args
        return self

    def width(self: _T, value: str | int) -> _T:
        """Set width (e.g. ``"100%"``, ``400``, ``"auto"``)."""
        self._width = value
        return self

    def height(self: _T, value: str | int) -> _T:
        """Set height."""
        self._height = value
        return self

    def className(self: _T, *classes: str) -> _T:
        """Append raw CSS class names (escape hatch for advanced users)."""
        self._classes.extend(classes)
        return self

    # ── Visibility & state ────────────────────────────────────────────────────

    def hidden(self: _T, condition: bool | ReactiveVar[bool]) -> _T:
        """Hide the component when *condition* is truthy."""
        self._hidden = condition
        return self

    def disabled(self: _T, condition: bool | ReactiveVar[bool]) -> _T:
        """Disable the component when *condition* is truthy."""
        self._disabled = condition
        return self

    # ── Identity ──────────────────────────────────────────────────────────────

    def id(self: _T, identifier: str) -> _T:
        """Override the auto-generated element ID."""
        self._id = identifier
        return self

    # ── Event handlers ────────────────────────────────────────────────────────

    def onClick(self: _T, handler: Callable[..., Any]) -> _T:  # noqa: N802
        """Register a click handler."""
        self._on_click = handler
        return self

    def onChange(self: _T, handler: Callable[..., Any]) -> _T:  # noqa: N802
        """Register a change handler (input, select, toggle, etc.)."""
        self._on_change = handler
        return self

    def onHover(self: _T, handler: Callable[..., Any]) -> _T:  # noqa: N802
        """Register a hover handler."""
        self._on_hover = handler
        return self

    def onMount(self: _T, handler: Callable[..., Any]) -> _T:  # noqa: N802
        """Register a mount lifecycle handler."""
        self._on_mount = handler
        return self

    def onUnmount(self: _T, handler: Callable[..., Any]) -> _T:  # noqa: N802
        """Register an unmount lifecycle handler."""
        self._on_unmount = handler
        return self

    # ── Children ─────────────────────────────────────────────────────────────

    def add(self: _T, *children: BaseComponent) -> _T:
        """Append child components. Returns *self* for chaining."""
        self.children.extend(children)
        return self

    def remove(self: _T, child: BaseComponent) -> _T:
        """Remove a specific child."""
        self.children.remove(child)
        return self

    def clear(self: _T) -> _T:
        """Remove all children."""
        self.children.clear()
        return self

    # ── Context Manager ──────────────────────────────────────────────────────

    def __enter__(self: _T) -> _T:
        _CONTEXT_STACK.append(self)
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        if _CONTEXT_STACK and _CONTEXT_STACK[-1] is self:
            _CONTEXT_STACK.pop()

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

    def render(self, target: str = "web") -> Any:  # noqa: ARG002
        """Called by the compiler to produce an ``IRNode``."""
        raise NotImplementedError(
            f"Component '{self.component_type}' has no render() implementation. "
            "Use pyui.compiler.ir.build_ir_node() instead."
        )

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
