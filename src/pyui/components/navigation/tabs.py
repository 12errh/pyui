from pyui.components.base import BaseComponent


class Tabs(BaseComponent):
    """
    Content switching with tab bars.
    """

    component_type = "tabs"

    def __init__(self, active_tab: str | None = None) -> None:
        super().__init__()
        self.props["active_tab"] = active_tab
        self.props["tabs"] = []

    def add_tab(self, label: str, *components: BaseComponent) -> "Tabs":
        self.props["tabs"].append({"label": label, "children": list(components)})
        return self
