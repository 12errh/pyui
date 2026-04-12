from pyui.components.base import BaseComponent


class Radio(BaseComponent):
    """
    Single-select radio input group.
    """

    component_type = "radio_group"

    def __init__(
        self, options: list[tuple[str, str]], value: str | None = None, label: str | None = None
    ) -> None:
        super().__init__()
        self.props.update(
            {
                "options": options,
                "value": value,
                "label": label,
            }
        )
