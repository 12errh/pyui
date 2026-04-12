from pyui.components.base import BaseComponent


class FilePicker(BaseComponent):
    """
    Styled file upload input.
    """

    component_type = "filepicker"

    def __init__(
        self, label: str | None = None, multiple: bool = False, accept: str | None = None
    ) -> None:
        super().__init__()
        self.props.update(
            {
                "label": label,
                "multiple": multiple,
                "accept": accept,
            }
        )

    def multiple(self, value: bool = True) -> "FilePicker":
        self.props["multiple"] = value
        return self

    def accept(self, value: str) -> "FilePicker":
        self.props["accept"] = value
        return self
