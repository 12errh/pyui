from pyui.components.base import BaseComponent


class Select(BaseComponent):
    """
    Dropdown selection input.
    """

    component_type = "select"

    def __init__(
        self, options: list[tuple[str, str]], value: str | None = None, label: str | None = None
    ) -> None:
        super().__init__()
        self.props.update(
            {
                "options": options,  # [(value, label), ...]
                "value": value,
                "label": label,
            }
        )

    def options(self, value: list[tuple[str, str]]) -> "Select":
        self.props["options"] = value
        return self
