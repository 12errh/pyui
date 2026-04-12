"""
Intermediate Representation (IR) — the compiler's target-agnostic tree.

Pipeline:
    BaseComponent  →  IRNode
    Page           →  IRPage
    App class      →  IRTree

The IR decouples the user's Python component tree from any specific
renderer. All renderers (web, desktop, CLI) consume IRTree.

Public functions:
    build_ir_node(component)   → IRNode
    build_ir_page(page)        → IRPage
    build_ir_tree(app_class)   → IRTree
"""

from __future__ import annotations

import uuid
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from pyui.app import App
    from pyui.components.base import BaseComponent
    from pyui.page import Page

# Global event-handler registry — maps handler_id → callable.
# The dev server looks handlers up here on each event POST.
_handler_registry: dict[str, Callable[..., Any]] = {}


def _register_handler(handler: Callable[..., Any]) -> str:
    """Store *handler* in the registry and return its stable ID."""
    h_id = f"h_{id(handler):x}"
    _handler_registry[h_id] = handler
    return h_id


def get_handler(handler_id: str) -> Callable[..., Any] | None:
    """Retrieve a registered handler by ID (used by the dev server)."""
    return _handler_registry.get(handler_id)


def clear_registry() -> None:
    """Clear the handler registry. Useful between hot-reloads."""
    _handler_registry.clear()


# ── Dataclasses ───────────────────────────────────────────────────────────────


@dataclass
class IRNode:
    """
    A single node in the Intermediate Representation tree.

    Attributes
    ----------
    type : str
        Component type identifier (``"button"``, ``"grid"``, etc.).
    props : dict
        All resolved, serialisable properties for this node.
    children : list[IRNode]
        Ordered child nodes.
    events : dict[str, str]
        Maps event name (``"click"``) to a handler ID in ``_handler_registry``.
    reactive_bindings : list[str]
        Names of reactive variables this node depends on.
    style_variant : str | None
        Active style variant (``"primary"``, ``"ghost"``, …).
    theme_tokens : dict
        Snapshot of theme tokens relevant to this node (populated by renderer).
    node_id : str
        Unique DOM / widget identifier.
    """

    type: str
    props: dict[str, Any]
    children: list[IRNode] = field(default_factory=list)
    events: dict[str, str] = field(default_factory=dict)
    reactive_bindings: list[str] = field(default_factory=list)
    style_variant: str | None = None
    theme_tokens: dict[str, str] = field(default_factory=dict)
    node_id: str = field(default_factory=lambda: f"pyui-{uuid.uuid4().hex[:8]}")


@dataclass
class IRPage:
    """A compiled page ready for a renderer to consume."""

    route: str
    title: str
    layout: str
    children: list[IRNode]  # top-level component nodes on this page
    meta: dict[str, str] = field(default_factory=dict)


@dataclass
class IRTree:
    """The top-level IR for an entire App — passed to renderers."""

    app_meta: dict[str, Any]
    pages: list[IRPage]
    theme: str | dict[str, str]
    reactive_vars: dict[str, Any]  # key → current value snapshot
    event_handlers: dict[str, Callable[..., Any]]  # id → callable


# ── Builder functions ─────────────────────────────────────────────────────────


def build_ir_node(component: BaseComponent) -> IRNode:
    """
    Recursively convert a :class:`~pyui.components.base.BaseComponent`
    into an :class:`IRNode`.

    Parameters
    ----------
    component : BaseComponent
        Any component instance.

    Returns
    -------
    IRNode
    """
    # Register event handlers
    events: dict[str, str] = {}
    handler_map = {
        "click": component._on_click,
        "change": component._on_change,
        "hover": component._on_hover,
        "mount": component._on_mount,
        "unmount": component._on_unmount,
    }
    for event_name, handler in handler_map.items():
        if handler is not None:
            events[event_name] = _register_handler(handler)

    # Detect reactive props
    reactive_bindings: list[str] = []
    props_copy = dict(component.props)

    # If content prop is a callable (reactive lambda), resolve it now
    # and mark that this node is reactive.
    for key, val in props_copy.items():
        if callable(val) and not isinstance(val, type):
            reactive_bindings.append(key)
            props_copy["is_reactive"] = True  # explicitly flag for renderer
            # Resolve the value at compile-time for SSR
            try:
                props_copy[key] = val()
            except Exception:
                props_copy[key] = ""

    # Recursively build children
    children = [build_ir_node(child) for child in component.children]

    return IRNode(
        type=component.component_type,
        props=props_copy,
        children=children,
        events=events,
        reactive_bindings=reactive_bindings,
        style_variant=component._style_variant,
        node_id=component._id,
    )


def build_ir_page(page: Page) -> IRPage:
    """
    Convert a :class:`~pyui.page.Page` into an :class:`IRPage`.

    Parameters
    ----------
    page : Page

    Returns
    -------
    IRPage
    """
    children = [build_ir_node(c) for c in page.children]
    return IRPage(
        route=page.route or "/",
        title=page.title,
        layout=page.layout,
        children=children,
        meta=page.meta,
    )


def build_ir_tree(app_class: type[App]) -> IRTree:
    """
    Build the complete :class:`IRTree` for an entire :class:`~pyui.app.App`.

    Parameters
    ----------
    app_class : type[App]
        The App subclass (not an instance).

    Returns
    -------
    IRTree
    """
    import inspect

    from pyui.state.reactive import ReactiveVar

    # Collect reactive vars from the App class
    reactive_vars: dict[str, Any] = {}
    for attr_name, value in inspect.getmembers(app_class):
        if isinstance(value, ReactiveVar):
            reactive_vars[attr_name] = value.get()

    pages = [build_ir_page(p) for p in app_class.get_pages()]

    return IRTree(
        app_meta={
            "name": app_class.name,
            "version": app_class.version,
            "description": app_class.description,
            "favicon": app_class.favicon,
        },
        pages=pages,
        theme=app_class.theme,
        reactive_vars=reactive_vars,
        event_handlers=dict(_handler_registry),
    )
