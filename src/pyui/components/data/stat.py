from pyui.components.base import BaseComponent


class Stat(BaseComponent):
    """
    Result card showing a label, value, and optional trend.
    """

    component_type = "stat"

    def __init__(
        self, label: str, value: str, trend: str | None = None, trend_up: bool = True
    ) -> None:
        super().__init__()
        self.props.update(
            {
                "label": label,
                "value": value,
                "trend": trend,
                "trend_up": trend_up,
            }
        )
