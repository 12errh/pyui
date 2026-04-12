from pyui.components.base import BaseComponent


class Textarea(BaseComponent):
    """
    Multi-line text input field.
    """

    component_type = "textarea"

    def __init__(
        self,
        value: str = "",
        placeholder: str = "",
        rows: int = 4,
        label: str | None = None,
    ) -> None:
        super().__init__()
        self.props.update(
            {
                "value": value,
                "placeholder": placeholder,
                "rows": rows,
                "label": label,
            }
        )

    def rows(self, value: int) -> "Textarea":
        self.props["rows"] = value
        return self
