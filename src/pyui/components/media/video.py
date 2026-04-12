from pyui.components.base import BaseComponent


class Video(BaseComponent):
    """
    Native video player component.
    """

    component_type = "video"

    def __init__(self, src: str, poster: str | None = None, controls: bool = True) -> None:
        super().__init__()
        self.props.update(
            {
                "src": src,
                "poster": poster,
                "controls": controls,
            }
        )

    def autoplay(self, value: bool = True) -> "Video":
        self.props["autoplay"] = value
        return self

    def loop(self, value: bool = True) -> "Video":
        self.props["loop"] = value
        return self
