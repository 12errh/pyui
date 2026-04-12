from pyui.components.base import BaseComponent


class Alert(BaseComponent):
    """
    Inline status messages.
    """

    component_type = "alert"

    def __init__(self, title: str, description: str | None = None, variant: str = "info") -> None:
        super().__init__()
        self.props.update(
            {
                "title": title,
                "description": description,
            }
        )
        self.style(variant)

    def icon(self, value: bool = True) -> "Alert":
        self.props["show_icon"] = value
        return self
