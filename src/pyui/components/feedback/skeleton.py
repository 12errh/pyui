from pyui.components.base import BaseComponent


class Skeleton(BaseComponent):
    """
    Placeholder loading block.
    """

    component_type = "skeleton"

    def __init__(self, variant: str = "text") -> None:
        super().__init__()
        self.props["variant"] = variant
