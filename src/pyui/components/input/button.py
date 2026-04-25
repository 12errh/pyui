"""
Button component.

Example::

    from pyui import Button

    btn = Button("Save changes").style("primary").size("lg").onClick(save)
    btn_danger = Button("Delete").style("danger").disabled(True)
"""

from __future__ import annotations

from typing import Any

from pyui.components.base import BaseComponent


class Button(BaseComponent):
    """
    A clickable button component.

    Parameters
    ----------
    label : str
        The text label displayed inside the button.

    Style variants
    --------------
    ``"primary"``  — filled, brand colour
    ``"secondary"``— subtle filled
    ``"ghost"``    — transparent with border
    ``"danger"``   — red, for destructive actions
    ``"link"``     — looks like an inline link

    Size presets
    ------------
    ``"xs"`` / ``"sm"`` / ``"md"`` (default) / ``"lg"`` / ``"xl"``
    """

    component_type = "button"

    def __init__(self, label: str = "", type: str = "button") -> None:
        super().__init__()
        self.props: dict[str, Any] = {
            "label": label,
            "type": type,
            "loading": False,
            "icon": None,
            "icon_right": None,
        }

    def submit(self) -> Button:
        """Set HTML type to ``"submit"`` (for use inside a ``Form``)."""
        self.props["type"] = "submit"
        return self

    def loading(self, state: bool = True) -> Button:
        """Show a loading spinner inside the button."""
        self.props["loading"] = state
        return self

    def icon(self, name: str, position: str = "left") -> Button:
        """
        Attach an icon to the button.

        Parameters
        ----------
        name : str
            Icon identifier (Lucide icon name, e.g. ``"zap"``).
        position : str
            ``"left"`` or ``"right"``.
        """
        if position == "right":
            self.props["icon_right"] = name
        else:
            self.props["icon"] = name
        return self

    def __repr__(self) -> str:
        return (
            f"Button(label={self.props['label']!r}, "
            f"variant={self._style_variant!r}, "
            f"size={self._size!r})"
        )
