"""
Compiler package.

Public API:
    compile_app(app_class, target, output_dir) — build production output
    discover_app(module_path)                  — import module + find App
    build_ir_tree(app_class)                   — build intermediate representation
"""

from pathlib import Path
from typing import TYPE_CHECKING

from pyui.compiler.discovery import discover_app
from pyui.compiler.ir import IRNode, IRPage, IRTree, build_ir_node, build_ir_page, build_ir_tree

if TYPE_CHECKING:
    from pyui.app import App


def compile_app(
    app_class: "type[App]",
    target: str = "web",
    output_dir: str = "./dist",
) -> Path:
    """
    Compile *app_class* for *target* and write output to *output_dir*.

    Parameters
    ----------
    app_class : type[App]
        The App subclass to compile.
    target : str
        ``"web"``, ``"desktop"``, or ``"cli"``.
    output_dir : str
        Directory to write the compiled output to.

    Returns
    -------
    Path
        The resolved output directory path.
    """
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    if target == "web":
        from pyui.renderers.web.generator import WebGenerator

        ir = build_ir_tree(app_class)
        gen = WebGenerator(ir)
        gen.write_to_disk(out)
    elif target == "desktop":
        # Desktop target: launch the native window (no static output)
        from pyui.renderers.desktop import run_desktop_app

        run_desktop_app(app_class)
    elif target == "cli":
        # CLI target: render in the terminal (no static output)
        from pyui.renderers.cli import run_cli_app

        run_cli_app(app_class)
    else:
        raise NotImplementedError(
            f"Target '{target}' is not yet implemented. Available targets: 'web', 'desktop', 'cli'."
        )

    return out


__all__ = [
    "compile_app",
    "discover_app",
    "build_ir_node",
    "build_ir_page",
    "build_ir_tree",
    "IRNode",
    "IRPage",
    "IRTree",
]
