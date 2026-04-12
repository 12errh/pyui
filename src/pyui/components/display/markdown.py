from pyui.components.base import BaseComponent


class Markdown(BaseComponent):
    """
    Markdown content renderer.
    """

    component_type = "markdown"

    def __init__(self, content: str) -> None:
        super().__init__()
        self.props["content"] = content

    def content(self, value: str) -> "Markdown":
        self.props["content"] = value
        return self
