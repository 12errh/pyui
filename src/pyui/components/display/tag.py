from pyui.components.base import BaseComponent


class Tag(BaseComponent):
    """
    Categorization label.
    """

    component_type = "tag"

    def __init__(self, text: str, variant: str = "secondary") -> None:
        super().__init__()
        self.props["text"] = text
        self.style(variant)

    def closable(self, value: bool = True) -> "Tag":
        self.props["closable"] = value
        return self
