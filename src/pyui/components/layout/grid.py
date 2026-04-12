"""
Grid component — CSS grid layout container.

Example::

    from pyui import Grid, Card

    Grid(cols=3).add(
        Card(title="Fast",     body="Compiles to native code"),
        Card(title="Beautiful",body="Gorgeous by default"),
        Card(title="Simple",   body="Pure Python"),
    )
"""

from __future__ import annotations

from typing import Any

from pyui.components.base import BaseComponent


class Grid(BaseComponent):
    """
    A responsive CSS grid container.

    Parameters
    ----------
    cols : int | str
        Number of columns (1–12) or a responsive spec string
        like ``"1 sm:2 lg:3"``.
    gap : int
        Gap size on the 4px / 8px scale (default ``4`` = 16px).
    rows : int | None
        Number of explicit rows (optional).

    Example
    -------
    ::

        Grid(cols=3, gap=6).add(Card(...), Card(...), Card(...))
    """

    component_type = "grid"

    def __init__(
        self,
        cols: int | str = 1,
        gap: int = 4,
        rows: int | None = None,
    ) -> None:
        super().__init__()
        self.props: dict[str, Any] = {
            "cols": cols,
            "gap": gap,
            "rows": rows,
            "align": "stretch",  # "start" | "center" | "end" | "stretch"
            "justify": "start",  # "start" | "center" | "end" | "between"
        }

    def align(self, value: str) -> Grid:
        """Set ``align-items``. One of ``"start"``, ``"center"``, ``"end"``, ``"stretch"``."""
        self.props["align"] = value
        return self

    def justify(self, value: str) -> Grid:
        """Set ``justify-items``. One of ``"start"``, ``"center"``, ``"end"``, ``"between"``."""
        self.props["justify"] = value
        return self

    def __repr__(self) -> str:
        return (
            f"Grid(cols={self.props['cols']!r}, "
            f"gap={self.props['gap']!r}, "
            f"children={len(self.children)})"
        )
