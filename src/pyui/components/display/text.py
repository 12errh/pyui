"""
Text component — inline or block text display.

Example::

    from pyui import Text, reactive

    count = reactive(0)
    Text("Static text")
    Text(lambda: f"Dynamic count: {count.get()}")
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from pyui.components.base import BaseComponent


class Text(BaseComponent):
    """
    Renders a span or paragraph of text.

    Parameters
    ----------
    content : str | Callable[[], str]
        A plain string or a zero-argument lambda that returns one.
        When a callable is provided the compiler treats this node as
        reactive and re-evaluates on every state change.

    Style variants
    --------------
    ``"muted"``  — secondary text colour
    ``"code"``   — monospace font
    ``"lead"``   — larger intro paragraph
    ``"small"``  — smaller helper text
    """

    component_type = "text"

    def __init__(self, content: str | Callable[[], str] = "") -> None:
        super().__init__()
        self.props: dict[str, Any] = {
            "content": content,
            "is_reactive": callable(content),
            "element": "span",  # HTML element: "span" | "p" | "label"
            "truncate": False,
        }

    def paragraph(self) -> Text:
        """Render as a ``<p>`` element instead of ``<span>``."""
        self.props["element"] = "p"
        return self

    def label(self) -> Text:
        """Render as a ``<label>`` element."""
        self.props["element"] = "label"
        return self

    def truncate(self, enabled: bool = True) -> Text:
        """Truncate overflowing text with an ellipsis."""
        self.props["truncate"] = enabled
        return self

    def __repr__(self) -> str:
        content = self.props["content"]
        display = content if isinstance(content, str) else "<reactive>"
        return f"Text(content={display!r})"
