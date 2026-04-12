from pyui.components.base import BaseComponent


class Checkbox(BaseComponent):
    """
    Boolean checkbox input.
    """

    component_type = "checkbox"

    def __init__(self, checked: bool = False, label: str | None = None) -> None:
        super().__init__()
        self.props.update(
            {
                "checked": checked,
                "label": label,
            }
        )

    def checked(self, value: bool = True) -> "Checkbox":
        self.props["checked"] = value
        return self
