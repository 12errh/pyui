from pyui.components.base import BaseComponent


class Spacer(BaseComponent):
    """
    A flexible space pusher for flex layouts.
    """

    component_type = "spacer"

    def __init__(self, size: int | None = None) -> None:
        super().__init__()
        self.props["size"] = size

    def size(self, value: int) -> "Spacer":
        self.props["size"] = value
        return self
