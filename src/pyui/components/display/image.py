from pyui.components.base import BaseComponent


class Image(BaseComponent):
    """
    Responsive image component.
    """

    component_type = "image"

    def __init__(self, src: str, alt: str = "") -> None:
        super().__init__()
        self.props.update(
            {
                "src": src,
                "alt": alt,
            }
        )

    def alt(self, value: str) -> "Image":
        self.props["alt"] = value
        return self

    def fit(self, value: str) -> "Image":
        self.props["fit"] = value  # cover, contain, etc.
        return self
