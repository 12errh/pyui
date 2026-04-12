from pyui.components.base import BaseComponent


class Modal(BaseComponent):
    """
    Centered overlay dialog.
    """

    component_type = "modal"

    def __init__(self, title: str | None = None, open: bool = False) -> None:
        super().__init__()
        self.props.update(
            {
                "title": title,
                "open": open,
            }
        )

    def open(self, value: bool = True) -> "Modal":
        self.props["open"] = value
        return self

    def footer(self, *components: BaseComponent) -> "Modal":
        if "footer_children" not in self.props:
            self.props["footer_children"] = []
        self.props["footer_children"].extend(components)
        return self
