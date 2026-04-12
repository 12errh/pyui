from pyui.components.base import BaseComponent


class Pagination(BaseComponent):
    """
    List paging controls.
    """

    component_type = "pagination"

    def __init__(self, current: int = 1, total: int = 1) -> None:
        super().__init__()
        self.props.update(
            {
                "current": current,
                "total": total,
            }
        )
