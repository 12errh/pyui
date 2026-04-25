from pyui.components.base import BaseComponent


class Image(BaseComponent):
    """
    Responsive image component.
    """

    component_type = "image"

    def __init__(self, src: str, alt: str = "", width: int | None = None, height: int | None = None) -> None:
        super().__init__()
        self.props.update(
            {
                "src": src,
                "alt": alt,
                "width": width,
                "height": height,
            }
        )

    def alt(self, value: str) -> "Image":
        self.props["alt"] = value
        return self

    def fit(self, value: str) -> "Image":
        self.props["fit"] = value  # cover, contain, etc.
        return self
