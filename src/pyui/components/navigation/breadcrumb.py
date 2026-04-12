from pyui.components.base import BaseComponent


class Breadcrumb(BaseComponent):
    """
    Path-based navigation.
    """

    component_type = "breadcrumb"

    def __init__(self, items: list[tuple[str, str]] | None = None) -> None:
        super().__init__()
        self.props["items"] = items or []

    def add_item(self, label: str, route: str) -> "Breadcrumb":
        self.props["items"].append((label, route))
        return self
