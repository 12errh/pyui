from pyui.components.base import BaseComponent


class Tooltip(BaseComponent):
    """
    Small hover-based info.
    """

    component_type = "tooltip"

    def __init__(self, text: str) -> None:
        super().__init__()
        self.props["text"] = text
