from pyui.components.base import BaseComponent


class Slider(BaseComponent):
    """
    Range slider input.
    """

    component_type = "slider"

    def __init__(
        self,
        value: float = 0,
        min: float = 0,
        max: float = 100,
        step: float = 1,
        label: str | None = None,
    ) -> None:
        super().__init__()
        self.props.update(
            {
                "value": value,
                "min": min,
                "max": max,
                "step": step,
                "label": label,
            }
        )

    def range(self, min: float, max: float) -> "Slider":
        self.props["min"] = min
        self.props["max"] = max
        return self
