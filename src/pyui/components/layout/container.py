from pyui.components.base import BaseComponent


class Container(BaseComponent):
    """
    Fixed-width centered wrapper for content.
    """

    component_type = "container"

    def __init__(self, size: str = "xl", centered: bool = True) -> None:
        super().__init__()
        self.props.update(
            {
                "size": size,
                "centered": centered,
            }
        )

    def size(self, value: str) -> "Container":
        self.props["size"] = value
        return self

    def fluid(self) -> "Container":
        self.props["size"] = "full"
        return self
