from pyui.components.base import BaseComponent


class Badge(BaseComponent):
    """
    Small count or status indicator.
    """

    component_type = "badge"

    def __init__(self, text: str, variant: str = "primary") -> None:
        super().__init__()
        self.props["text"] = text
        self.style(variant)

    def text(self, value: str) -> "Badge":
        self.props["text"] = value
        return self
