from pyui.components.base import BaseComponent


class Spinner(BaseComponent):
    """
    Loading state indicator.
    """

    component_type = "spinner"

    def __init__(self, size: str = "md") -> None:
        super().__init__()
        self.props["spinner_size"] = size
