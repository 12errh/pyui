from pyui.components.base import BaseComponent


class DatePicker(BaseComponent):
    """
    Calendar-based date selection input.
    """

    component_type = "datepicker"

    def __init__(self, value: str | None = None, label: str | None = None) -> None:
        super().__init__()
        self.props.update(
            {
                "value": value,
                "label": label,
            }
        )
