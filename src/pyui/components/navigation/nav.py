from pyui.components.base import BaseComponent


class Nav(BaseComponent):
    """
    Main navigation links/bar.
    """

    component_type = "nav"

    def __init__(self, items: list[tuple[str, str]] | None = None) -> None:
        super().__init__()
        self.props["items"] = items or []

    def add_item(self, label: str, route: str) -> "Nav":
        self.props["items"].append((label, route))
        return self
