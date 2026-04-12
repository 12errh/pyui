from pyui.components.base import BaseComponent


class Table(BaseComponent):
    """
    Structured data grid.
    """

    component_type = "table"

    def __init__(self, headers: list[str], rows: list[list[str]]) -> None:
        super().__init__()
        self.props.update(
            {
                "headers": headers,
                "rows": rows,
            }
        )

    def striped(self, value: bool = True) -> "Table":
        self.props["striped"] = value
        return self

    def scrollable(self, value: bool = True) -> "Table":
        self.props["scrollable"] = value
        return self
