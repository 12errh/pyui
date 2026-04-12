from pyui.components.base import BaseComponent


class Flex(BaseComponent):
    """
    Flexbox container for aligning and distributing space among items.

    API::

        Flex(direction="row", gap=4).add(
            Text("Left"),
            Text("Right")
        )
    """

    component_type = "flex"

    def __init__(
        self,
        direction: str = "row",
        align: str = "center",
        justify: str = "start",
        gap: int = 4,
        wrap: bool = False,
    ) -> None:
        super().__init__()
        self.props.update(
            {
                "direction": direction,
                "align": align,
                "justify": justify,
                "gap": gap,
                "wrap": wrap,
            }
        )

    def direction(self, value: str) -> "Flex":
        self.props["direction"] = value
        return self

    def align(self, value: str) -> "Flex":
        self.props["align"] = value
        return self

    def justify(self, value: str) -> "Flex":
        self.props["justify"] = value
        return self

    def gap(self, value: int) -> "Flex":
        self.props["gap"] = value
        return self

    def wrap(self, value: bool = True) -> "Flex":
        self.props["wrap"] = value
        return self
