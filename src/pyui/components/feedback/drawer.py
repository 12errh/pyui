from pyui.components.base import BaseComponent


class Drawer(BaseComponent):
    """
    Sliding side panel overlay.
    """

    component_type = "drawer"

    def __init__(self, title: str | None = None, open: bool = False, side: str = "right") -> None:
        super().__init__()
        self.props.update(
            {
                "title": title,
                "open": open,
                "side": side,
            }
        )
