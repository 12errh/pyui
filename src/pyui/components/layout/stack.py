from pyui.components.base import BaseComponent


class Stack(BaseComponent):
    """
    Vertical or horizontal stack of components with consistent spacing.

    API::

        Stack(direction="vertical", spacing=4).add(...)
    """

    component_type = "stack"

    def __init__(self, direction: str = "vertical", spacing: int = 4) -> None:
        super().__init__()
        self.props.update(
            {
                "direction": direction,
                "spacing": spacing,
            }
        )

    def vertical(self) -> "Stack":
        self.props["direction"] = "vertical"
        return self

    def horizontal(self) -> "Stack":
        self.props["direction"] = "horizontal"
        return self

    def spacing(self, value: int) -> "Stack":
        self.props["spacing"] = value
        return self
