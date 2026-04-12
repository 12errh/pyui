from pyui.components.base import BaseComponent


class Split(BaseComponent):
    """
    Resizable or fixed split-pane layout.
    """

    component_type = "split"

    def __init__(self, direction: str = "horizontal", ratio: float = 0.5) -> None:
        super().__init__()
        self.props.update(
            {
                "direction": direction,
                "ratio": ratio,
            }
        )
        self._left_pane: list[BaseComponent] = []
        self._right_pane: list[BaseComponent] = []

    def first(self, *components: BaseComponent) -> "Split":
        if "first_pane" not in self.props:
            self.props["first_pane"] = []
        self.props["first_pane"].extend(components)
        return self

    def second(self, *components: BaseComponent) -> "Split":
        if "second_pane" not in self.props:
            self.props["second_pane"] = []
        self.props["second_pane"].extend(components)
        return self

    def ratio(self, value: float) -> "Split":
        self.props["ratio"] = value
        return self
