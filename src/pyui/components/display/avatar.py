from pyui.components.base import BaseComponent


class Avatar(BaseComponent):
    """
    User profile image or placeholder with initials support.
    """

    component_type = "avatar"

    def __init__(self, src: str | None = None, name: str | None = None, size: str = "md") -> None:
        super().__init__()
        self.props.update(
            {
                "src": src,
                "name": name,
                "size": size,
            }
        )

    def src(self, value: str) -> "Avatar":
        self.props["src"] = value
        return self

    def name(self, value: str) -> "Avatar":
        self.props["name"] = value
        return self
