from pyui.components.base import BaseComponent


class Divider(BaseComponent):
    """
    A horizontal or vertical line for visual separation.
    """

    component_type = "divider"

    def __init__(self, direction: str = "horizontal", label: str | None = None) -> None:
        super().__init__()
        self.props.update(
            {
                "direction": direction,
                "label": label,
            }
        )

    def vertical(self) -> "Divider":
        self.props["direction"] = "vertical"
        return self

    def label(self, text: str) -> "Divider":
        self.props["label"] = text
        return self
