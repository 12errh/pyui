"""
CLI renderer package — Rich TUI backend.

Public API::

    from pyui.renderers.cli import run_cli_app, render_to_rich

    run_cli_app(MyApp)
"""

from pyui.renderers.cli.generator import CliRenderer, render_to_rich, run_cli_app

__all__ = ["CliRenderer", "render_to_rich", "run_cli_app"]
