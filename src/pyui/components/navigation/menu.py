from pyui.components.base import BaseComponent


class Menu(BaseComponent):
    """
    Contextual or dropdown menus.
    """

    component_type = "menu"

    def __init__(self, items: list[tuple[str, str]] | None = None) -> None:
        super().__init__()
        self.props["items"] = items or []
