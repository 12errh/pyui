from pyui.components.base import BaseComponent


class Toggle(BaseComponent):
    """
    Visual boolean switch (Toggle).
    """

    component_type = "toggle"

    def __init__(self, checked: bool = False, label: str | None = None) -> None:
        super().__init__()
        self.props.update(
            {
                "checked": checked,
                "label": label,
            }
        )
