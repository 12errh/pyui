"""
Heading component — semantic HTML headings h1–h6.

Example::

    from pyui import Heading

    Heading("Welcome to PyUI", level=1)
    Heading("Section title", level=2).style("gradient")
"""

from __future__ import annotations

from typing import Any

from pyui.components.base import BaseComponent


class Heading(BaseComponent):
    """
    A semantic heading (``<h1>`` – ``<h6>``).

    Parameters
    ----------
    text : str
        The heading text.
    level : int
        Heading level 1–6 (default: ``1``).

    Style variants
    --------------
    ``"gradient"``  — purple-to-pink gradient text
    ``"muted"``     — subdued, secondary heading
    ``"display"``   — extra-large, hero-size heading
    """

    component_type = "heading"

    def __init__(self, text: str = "", level: int = 1, subtitle: str | None = None) -> None:
        super().__init__()
        if not 1 <= level <= 6:
            raise ValueError(f"Heading level must be 1–6, got {level!r}.")
        self.props: dict[str, Any] = {
            "text": text,
            "level": level,
            "subtitle": subtitle,
        }

    def subtitle(self, text: str) -> Heading:
        """Add a subtitle rendered directly beneath the heading."""
        self.props["subtitle"] = text
        return self

    def __repr__(self) -> str:
        return f"Heading(text={self.props['text']!r}, level={self.props['level']!r})"
