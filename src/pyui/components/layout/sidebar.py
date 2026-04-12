from pyui.components.base import BaseComponent


class Sidebar(BaseComponent):
    """
    Layout shell with a side panel and a main content area.
    """

    component_type = "sidebar_layout"

    def __init__(self, side: str = "left", width: str = "64") -> None:
        super().__init__()
        self.props.update(
            {
                "side": side,
                "width": width,
            }
        )
        self._sidebar_content: list[BaseComponent] = []
        self._main_content: list[BaseComponent] = []

    def sidebar(self, *components: BaseComponent) -> "Sidebar":
        if "sidebar_children" not in self.props:
            self.props["sidebar_children"] = []
        self.props["sidebar_children"].extend(components)
        return self

    def content(self, *components: BaseComponent) -> "Sidebar":
        if "main_children" not in self.props:
            self.props["main_children"] = []
        self.props["main_children"].extend(components)
        return self
