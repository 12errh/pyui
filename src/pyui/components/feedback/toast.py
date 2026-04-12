from pyui.components.base import BaseComponent


class Toast(BaseComponent):
    """
    Floating notification.
    """

    component_type = "toast"

    def __init__(self, message: str, variant: str = "info", duration: int = 3000) -> None:
        super().__init__()
        self.props.update(
            {
                "message": message,
                "duration": duration,
            }
        )
        self.style(variant)
