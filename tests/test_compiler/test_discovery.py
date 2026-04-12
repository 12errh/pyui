"""
Phase 1 — compiler discovery tests.

Tests from the PyUI spec Section 5, Phase 1.
"""

from __future__ import annotations

from pathlib import Path

import pytest


def test_discovers_app_subclass(tmp_path: Path) -> None:
    """discover_app() must find an App subclass in the given file."""
    app_file = tmp_path / "app.py"
    app_file.write_text("from pyui import App\nclass MyApp(App): pass\n")

    from pyui.compiler.discovery import discover_app

    cls = discover_app(str(app_file))
    assert cls.__name__ == "MyApp"


def test_raises_if_no_app_subclass(tmp_path: Path) -> None:
    """discover_app() must raise PyUIError when no App subclass exists."""
    f = tmp_path / "app.py"
    f.write_text("x = 1\n")

    from pyui.compiler.discovery import discover_app
    from pyui.exceptions import PyUIError

    with pytest.raises(PyUIError, match="No App subclass found"):
        discover_app(str(f))


def test_raises_if_file_not_found() -> None:
    """discover_app() must raise FileNotFoundError for a missing file."""
    from pyui.compiler.discovery import discover_app

    with pytest.raises(FileNotFoundError):
        discover_app("/nonexistent/path/to/app.py")


def test_raises_if_module_has_syntax_error(tmp_path: Path) -> None:
    """discover_app() must raise PyUIError for a broken module."""
    bad_file = tmp_path / "app.py"
    bad_file.write_text("def broken syntax!!!\n")

    from pyui.compiler.discovery import discover_app
    from pyui.exceptions import PyUIError

    with pytest.raises(PyUIError):
        discover_app(str(bad_file))


def test_app_with_page_discovered(tmp_path: Path) -> None:
    """discover_app() works with a realistic App that has Pages."""
    app_file = tmp_path / "my_app.py"
    app_file.write_text(
        "from pyui import App, Page\nclass MyApp(App):\n    home = Page(title='Home', route='/')\n"
    )
    from pyui.compiler.discovery import discover_app

    cls = discover_app(str(app_file))
    assert cls.__name__ == "MyApp"
    assert len(cls.get_pages()) == 1
