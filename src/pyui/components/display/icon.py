from pyui.components.base import BaseComponent


class Icon(BaseComponent):
    """
    Vector icons via Lucide.
    """

    component_type = "icon"

    def __init__(self, name: str, size: int = 24, color: str | None = None) -> None:
        super().__init__()
        self.props.update(
            {
                "name": name,
                "icon_size": size,
                "color": color,
            }
        )

    def name(self, value: str) -> "Icon":
        self.props["name"] = value
        return self

    def icon_size(self, value: int) -> "Icon":
        self.props["icon_size"] = value
        return self

    def color(self, value: str) -> "Icon":
        self.props["color"] = value
        return self
