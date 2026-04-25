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

from pyui.components.base import BaseComponent
from pyui.page import Page

if TYPE_CHECKING:
    from pyui.app import App

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
    reactive_props: dict[str, list[str]] = field(
        default_factory=dict
    )  # prop_name -> list of dependencies
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
    persistent_vars: list[str] = field(default_factory=list)


# ── Builder functions ─────────────────────────────────────────────────────────


def build_ir_node(component: BaseComponent, path: str | None = None) -> IRNode:
    """
    Recursively convert a :class:`~pyui.components.base.BaseComponent`
    into an :class:`IRNode`.

    Parameters
    ----------
    component : BaseComponent
        Any component instance.
    path : str | None
        Optional hierarchical path for deterministic IDs.

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

    # Hook for dynamic child building (e.g. List component in Phase 3)
    if hasattr(component, "_build_children") and callable(component._build_children):
        component._build_children()

    # Detect reactive props
    reactive_bindings: list[str] = []
    reactive_props: dict[str, list[str]] = {}
    props_copy = dict(component.props)
    props_copy["class_name"] = " ".join(component._classes)

    # Promote base component attributes into props so renderers can access them
    if component._disabled is not False:
        props_copy["disabled"] = component._disabled
    if component._size is not None:
        props_copy["_size"] = component._size
    if component._hidden is not False:
        props_copy["hidden"] = component._hidden

    # If content prop is a callable (reactive lambda) or a ReactiveVar directly,
    # resolve it now and mark that this node is reactive.
    from pyui.state.reactive import _REACTIVE_CONTEXT, ReactiveVar, get_reactive_name

    is_reactive = False
    for key, val in props_copy.items():
        if isinstance(val, ReactiveVar):
            name = get_reactive_name(val)
            if name:
                reactive_bindings.append(name)
                reactive_props[key] = [name]
                is_reactive = True
            props_copy[key] = val.get()
        elif callable(val) and not isinstance(val, type):
            _REACTIVE_CONTEXT.append(set())
            try:
                resolved_val = val()
                touched = _REACTIVE_CONTEXT.pop()

                # In Phase 3, we track specific dependencies.
                # But for existing tests, we mark any lambda as reactive.
                prop_deps = []
                for var in touched:
                    name = get_reactive_name(var)
                    if name:
                        prop_deps.append(name)
                        if name not in reactive_bindings:
                            reactive_bindings.append(name)

                # If no specific reactive vars were touched, we still mark the prop as reactive
                # so the renderer knows it came from a lambda.
                reactive_props[key] = prop_deps
                is_reactive = True
                if key not in reactive_bindings:
                    reactive_bindings.append(key)

                # Resolve the value at compile-time for SSR
                props_copy[key] = resolved_val
            except Exception:
                _REACTIVE_CONTEXT.pop()
                # If resolution fails during build, use a safe default
                props_copy[key] = ""

    if is_reactive:
        props_copy["is_reactive"] = True

    # Recursively build slots (any prop that is a BaseComponent or list of BaseComponents)
    from pyui.components.base import BaseComponent

    for key, val in props_copy.items():
        if isinstance(val, BaseComponent):
            props_copy[key] = build_ir_node(val, f"{path}-{key}" if path else None)
        elif isinstance(val, list) and val and isinstance(val[0], BaseComponent):
            props_copy[key] = [
                build_ir_node(item, f"{path}-{key}-{i}" if path else None)
                for i, item in enumerate(val)
            ]

    # Recursively build children
    children = [
        build_ir_node(child, f"{path}-{i}" if path else None)
        for i, child in enumerate(component.children)
    ]

    # Deterministic ID for stability if path is provided, otherwise use random ID from component
    node_id = component._id
    if path and (not component._id or component._id.startswith("pyui-")):
        node_id = f"pyui-{path}"

    return IRNode(
        type=component.component_type,
        props=props_copy,
        children=children,
        events=events,
        reactive_bindings=reactive_bindings,
        reactive_props=reactive_props,
        style_variant=component._style_variant,
        node_id=node_id,
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
    # Call compose() to populate the children tree if using declarative style
    if hasattr(page, "compose") and callable(page.compose):
        # Clear children before compose() to prevent duplication during hot reloads
        page.children.clear()
        with page:
            page.compose()

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

    from pyui.state.reactive import ReactiveVar, register_reactive_name

    # Collect reactive vars from the App class
    reactive_vars: dict[str, Any] = {}
    persistent_vars: list[str] = []
    for attr_name, value in inspect.getmembers(app_class):
        if isinstance(value, ReactiveVar):
            reactive_vars[attr_name] = value.get()
            register_reactive_name(value, attr_name)
            if value._persist:
                persistent_vars.append(attr_name)

    pages = [build_ir_page(p) for p in app_class.get_pages()]

    return IRTree(
        app_meta={
            "name": app_class.name,
            "version": app_class.version,
            "description": app_class.description,
            "favicon": app_class.favicon,
        },
        pages=pages,
        theme=app_class.theme.get()
        if isinstance(app_class.theme, ReactiveVar)
        else app_class.theme,
        reactive_vars=reactive_vars,
        event_handlers=dict(_handler_registry),
        persistent_vars=persistent_vars,
    )
