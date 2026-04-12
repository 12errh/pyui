from collections.abc import Callable
from typing import Any

from pyui.components.base import BaseComponent


class Form(BaseComponent):
    """
    Container for grouping inputs and handling submission.
    """

    component_type = "form"

    def __init__(self, title: str | None = None) -> None:
        super().__init__()
        self.props["title"] = title

    def onSubmit(self, handler: Callable[..., Any]) -> "Form":  # noqa: N802
        self._on_change = handler  # We'll use _on_change internally or a dedicated handler
        return self
