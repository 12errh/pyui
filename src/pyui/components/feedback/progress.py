from pyui.components.base import BaseComponent


class Progress(BaseComponent):
    """
    Horizontal or circular progress bar.
    """

    component_type = "progress"

    def __init__(self, value: float = 0, max: float = 100, circular: bool = False) -> None:
        super().__init__()
        self.props.update(
            {
                "value": value,
                "max": max,
                "circular": circular,
            }
        )
