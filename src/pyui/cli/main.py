"""
PyUI CLI entry point.

All subcommands live under the ``pyui`` group. Run ``pyui --help`` for usage.
"""

from __future__ import annotations

import click
from rich import box
from rich.console import Console
from rich.panel import Panel

import pyui
from pyui.utils.logging import configure_logging

console = Console()


# ── Main group ────────────────────────────────────────────────────────────────


@click.group(
    context_settings={"help_option_names": ["-h", "--help"]},
    invoke_without_command=True,
)
@click.version_option(pyui.__version__, "-V", "--version", prog_name="PyUI")
@click.option("-v", "--verbose", is_flag=True, help="Enable verbose (DEBUG) logging.")
@click.pass_context
def main(ctx: click.Context, verbose: bool) -> None:
    """
    \b
    PyUI -- Write Python. Render anywhere.
    Web | Desktop | CLI from a single Python codebase.
    """
    configure_logging("DEBUG" if verbose else "INFO")

    if ctx.invoked_subcommand is None:
        console.print(
            Panel.fit(
                f"[bold cyan]PyUI[/bold cyan] [dim]v{pyui.__version__}[/dim]\n"
                "[dim]Run [bold]pyui --help[/bold] to see available commands.[/dim]",
                box=box.ASCII,
                border_style="cyan",
            )
        )


# ── new ───────────────────────────────────────────────────────────────────────


@main.command("new")
@click.argument("name")
@click.option(
    "--template",
    default="blank",
    type=click.Choice(["blank", "dashboard", "landing", "admin", "auth"]),
    show_default=True,
    help="Project template to scaffold from.",
)
@click.option(
    "--target",
    default="web",
    type=click.Choice(["web", "desktop", "cli", "all"]),
    show_default=True,
    help="Default render target.",
)
def cmd_new(name: str, template: str, target: str) -> None:
    """Scaffold a new PyUI project called NAME."""
    console.print(
        f"[yellow]![/yellow]  [bold]pyui new[/bold] is not yet implemented "
        f"(Phase 0 stub). Project name: [cyan]{name}[/cyan], "
        f"template: [cyan]{template}[/cyan], target: [cyan]{target}[/cyan]."
    )


# ── run ───────────────────────────────────────────────────────────────────────


@main.command("run")
@click.option(
    "--target",
    "-t",
    default="web",
    type=click.Choice(["web", "desktop", "cli"]),
    show_default=True,
    help="Render target.",
)
@click.option("--port", "-p", default=8000, show_default=True, help="Dev server port.")
@click.option("--host", default="localhost", show_default=True, help="Dev server host.")
@click.option(
    "--no-browser", is_flag=True, default=False, help="Do not open browser automatically."
)
@click.argument("app_file", default="app.py", required=False)
def cmd_run(target: str, port: int, host: str, no_browser: bool, app_file: str) -> None:
    """Start the PyUI dev server (APP_FILE defaults to app.py)."""
    try:
        from pyui.compiler.discovery import discover_app

        AppClass = discover_app(app_file)
    except FileNotFoundError:
        console.print(f"[red]Error:[/red] App file not found: [cyan]{app_file}[/cyan]")
        raise SystemExit(1) from None
    except Exception as exc:
        console.print(f"[red]Error:[/red] {exc}")
        raise SystemExit(1) from None

    if target == "web":
        from pyui.server.dev_server import run_dev_server

        run_dev_server(AppClass, host=host, port=port, open_browser=not no_browser)

    elif target == "desktop":
        console.print(f"[bold cyan]Launching desktop window for[/bold cyan] [dim]{app_file}[/dim]")
        from pyui.renderers.desktop import run_desktop_app

        run_desktop_app(AppClass)

    elif target == "cli":
        from pyui.renderers.cli import run_cli_app

        run_cli_app(AppClass)

    else:
        console.print(f"[red]Error:[/red] Unknown target: [cyan]{target}[/cyan]")
        raise SystemExit(1) from None


# ── build ─────────────────────────────────────────────────────────────────────


@main.command("build")
@click.option(
    "--target",
    "-t",
    default="web",
    type=click.Choice(["web", "desktop", "cli", "all"]),
    show_default=True,
)
@click.option("--out", default="./dist", show_default=True, help="Output directory.")
@click.argument("app_file", default="app.py", required=False)
def cmd_build(target: str, out: str, app_file: str) -> None:
    """Build a production bundle from APP_FILE."""
    try:
        from pyui.compiler.discovery import discover_app

        AppClass = discover_app(app_file)
    except Exception as exc:
        console.print(f"[red]Error:[/red] {exc}")
        raise SystemExit(1) from None

    from pyui.compiler import compile_app

    try:
        output_path = compile_app(AppClass, target=target, output_dir=out)
        console.print(f"[green]Built[/green] [cyan]{app_file}[/cyan] -> [cyan]{output_path}[/cyan]")
    except NotImplementedError as exc:
        console.print(f"[yellow]![/yellow]  {exc}")


# ── publish ───────────────────────────────────────────────────────────────────


@main.command("publish")
@click.option("--name", default=None, help="Override package name.")
def cmd_publish(name: str | None) -> None:
    """Publish a component package to the PyUI marketplace."""
    console.print("[yellow]![/yellow]  [bold]pyui publish[/bold] is not yet implemented (Phase 5).")


# ── doctor ────────────────────────────────────────────────────────────────────


@main.command("doctor")
def cmd_doctor() -> None:
    """Check environment health (Python version, dependencies, ports)."""
    import platform
    import sys

    console.print("[bold]PyUI Doctor[/bold]\n")
    console.print(f"  Python   : [cyan]{sys.version.split()[0]}[/cyan]")
    console.print(f"  Platform : [cyan]{platform.system()} {platform.release()}[/cyan]")
    console.print(f"  PyUI     : [cyan]{pyui.__version__}[/cyan]")

    py_ok = sys.version_info >= (3, 10)
    status = "[green]OK[/green]" if py_ok else "[red]FAIL -- upgrade to Python 3.10+[/red]"
    console.print(f"  Python >= 3.10 : {status}")
    console.print("\n[dim]Full dependency checks will be added in Phase 6.[/dim]")


# ── lint ──────────────────────────────────────────────────────────────────────


@main.command("lint")
@click.argument("app_file", default="app.py", required=False)
def cmd_lint(app_file: str) -> None:
    """Lint component definitions in APP_FILE."""
    console.print(
        f"[yellow]![/yellow]  [bold]pyui lint[/bold] is not yet implemented (Phase 6). "
        f"Would lint [cyan]{app_file}[/cyan]."
    )


# ── storybook ───────────────────────────────────────────────────────────────


@main.command("storybook")
@click.option("--port", "-p", default=9000, show_default=True, help="Storybook port.")
@click.option(
    "--no-browser", is_flag=True, default=False, help="Do not open browser automatically."
)
def cmd_storybook(port: int, no_browser: bool) -> None:
    """Open the component storybook (gallery)."""
    from pyui.cli.storybook import run_storybook

    console.print("[bold cyan]Opening PyUI Storybook...[/bold cyan]")
    run_storybook(port=port, open_browser=not no_browser)


# ── info ──────────────────────────────────────────────────────────────────────


@main.command("info")
def cmd_info() -> None:
    """Show PyUI version and project info."""
    console.print(
        Panel.fit(
            f"[bold cyan]PyUI Framework[/bold cyan] [dim]v{pyui.__version__}[/dim]\n"
            "[dim]Write Python. Render anywhere.[/dim]\n\n"
            f"[dim]Docs    :[/dim] https://pyui.dev\n"
            f"[dim]GitHub  :[/dim] https://github.com/pyui-framework/pyui\n"
            f"[dim]License :[/dim] MIT",
            box=box.ASCII,
            border_style="cyan",
        )
    )
