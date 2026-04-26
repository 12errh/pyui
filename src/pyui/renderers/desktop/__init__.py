"""Desktop renderer package — tkinter backend."""

from pyui.renderers.desktop.tkinter_renderer import (
    TkinterRenderer,
    build_widget_tree,
    run_desktop_app,
)

__all__ = ["TkinterRenderer", "build_widget_tree", "run_desktop_app"]
