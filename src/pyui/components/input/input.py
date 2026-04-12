from pyui.components.base import BaseComponent


class Input(BaseComponent):
    """
    Standard text/email/password input field.
    """

    component_type = "input"

    def __init__(
        self,
        value: str = "",
        placeholder: str = "",
        type: str = "text",
        label: str | None = None,
    ) -> None:
        super().__init__()
        self.props.update(
            {
                "value": value,
                "placeholder": placeholder,
                "type": type,
                "label": label,
            }
        )

    def placeholder(self, value: str) -> "Input":
        self.props["placeholder"] = value
        return self

    def type(self, value: str) -> "Input":
        self.props["type"] = value
        return self

    def label(self, value: str) -> "Input":
        self.props["label"] = value
        return self
