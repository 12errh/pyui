"""
PyUI App base class.

Users subclass ``App`` to define their application. Pages are declared
as class-level attributes; the framework auto-discovers them via ``inspect``.

Example::

    from pyui import App, Page, Button, Text

    class MyApp(App):
        name = "My Application"
        theme = "dark"

        home = Page(title="Home", route="/")
        home.add(Text("Hello, world!"))
"""

from __future__ import annotations

import inspect
from typing import Any

from pyui.exceptions import PyUIError
from pyui.page import Page


class AppMeta(type):
    """Metaclass that auto-discovers ``Page`` attributes on App subclasses."""

    def __new__(
        mcs,
        name: str,
        bases: tuple[type, ...],
        namespace: dict[str, Any],
    ) -> AppMeta:
        cls = super().__new__(mcs, name, bases, namespace)

        # Collect and register Page attributes
        pages: dict[str, Page] = {}
        for attr_name, value in inspect.getmembers(cls):
            if isinstance(value, Page):
                if value.route is None:
                    raise PyUIError(f"Page '{attr_name}' on App '{name}' is missing a 'route'.")
                pages[attr_name] = value

        cls._pages = pages  # type: ignore[attr-defined]
        return cls


class App(metaclass=AppMeta):
    """
    Root application class.

    Class attributes
    ----------------
    name : str
        Application display name.
    version : str
        Application version string.
    description : str
        Short description used in meta tags.
    icon : str | None
        Path or URL to application icon.
    favicon : str | None
        Path or URL to browser favicon.
    theme : str | dict
        Built-in theme name (e.g. ``"dark"``) or a custom token dict.
    fonts : list[str]
        Google Font family names to load.
    meta : dict
        Extra ``<meta>`` tags as key-value pairs.
    plugins : list
        Instances of :class:`~pyui.plugins.base.PyUIPlugin`.
    """

    name: str = "PyUI App"
    version: str = "1.0.0"
    description: str = ""
    icon: str | None = None
    favicon: str | None = None
    theme: str | dict[str, str] = "light"
    fonts: list[str] = ["Inter"]
    meta: dict[str, str] = {}
    plugins: list[Any] = []

    # Populated by AppMeta
    _pages: dict[str, Page] = {}

    @classmethod
    def get_pages(cls) -> list[Page]:
        """Return all registered pages, ordered by route."""
        return sorted(cls._pages.values(), key=lambda p: p.route or "")

    @classmethod
    def get_page(cls, route: str) -> Page | None:
        """Look up a page by its route string."""
        for page in cls._pages.values():
            if page.route == route:
                return page
        return None
