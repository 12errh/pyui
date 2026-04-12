from typing import Any

from pyui.components.base import BaseComponent


class Chart(BaseComponent):
    """
    Responsive vector charts via Chart.js.
    """

    component_type = "chart"

    def __init__(
        self,
        type: str = "line",
        labels: list[str] | None = None,
        datasets: list[dict[str, Any]] | None = None,
    ) -> None:
        super().__init__()
        self.props.update(
            {
                "chart_type": type,
                "labels": labels or [],
                "datasets": datasets or [],
            }
        )

    def line(self) -> "Chart":
        self.props["chart_type"] = "line"
        return self

    def bar(self) -> "Chart":
        self.props["chart_type"] = "bar"
        return self

    def pie(self) -> "Chart":
        self.props["chart_type"] = "pie"
        return self
