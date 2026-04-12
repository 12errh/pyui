"""
Phase 0 tests — project setup & foundations.

These are the six required tests from the PyUI spec (Section 5, Phase 0).
All must pass for Phase 0 to be considered complete.
"""

from __future__ import annotations

import re

# ── P0-01: package importable ─────────────────────────────────────────────────


def test_package_importable() -> None:
    """The pyui package must be importable and expose __version__."""
    import pyui

    assert pyui.__version__ is not None


# ── P0-02: version format ─────────────────────────────────────────────────────


def test_version_format() -> None:
    """__version__ must follow semantic versioning (MAJOR.MINOR.PATCH[...])."""
    import pyui

    assert re.match(r"^\d+\.\d+\.\d+", pyui.__version__), (
        f"Invalid version format: {pyui.__version__!r}"
    )


# ── P0-03: CLI entry point callable ───────────────────────────────────────────


def test_cli_entry_point() -> None:
    """The CLI entry point must be importable and callable."""
    from pyui.cli.main import main

    assert callable(main)


# ── P0-04: exceptions importable ──────────────────────────────────────────────


def test_exceptions_importable() -> None:
    """All exception classes must be importable from pyui.exceptions."""
    from pyui.exceptions import (
        CompilerError,
        ComponentError,
        PluginError,
        PyUIError,
        ThemeError,
    )

    # Confirm they're all actual classes
    for exc in (PyUIError, CompilerError, ComponentError, ThemeError, PluginError):
        assert isinstance(exc, type), f"{exc} is not a class"


# ── P0-05: PyUIError is an Exception ──────────────────────────────────────────


def test_pyui_error_is_exception() -> None:
    """PyUIError must inherit from the built-in Exception."""
    from pyui.exceptions import PyUIError

    assert issubclass(PyUIError, Exception)


# ── P0-06: CompilerError inherits PyUIError ───────────────────────────────────


def test_compiler_error_inherits_pyui_error() -> None:
    """CompilerError must be a subclass of PyUIError."""
    from pyui.exceptions import CompilerError, PyUIError

    assert issubclass(CompilerError, PyUIError)


# ── Bonus: full exception hierarchy ───────────────────────────────────────────


def test_all_errors_inherit_pyui_error() -> None:
    """Every domain error must trace back to PyUIError."""
    from pyui.exceptions import (
        CompilerError,
        ComponentError,
        PluginError,
        PyUIError,
        ThemeError,
    )

    for cls in (CompilerError, ComponentError, ThemeError, PluginError):
        assert issubclass(cls, PyUIError), f"{cls.__name__} does not inherit PyUIError"


def test_exceptions_are_raiseable() -> None:
    """Domain exceptions must be raiseable and catchable as PyUIError."""
    import pytest

    from pyui.exceptions import CompilerError, PyUIError

    with pytest.raises(PyUIError):
        raise CompilerError("test error")


# ── Bonus: App and Page importable ────────────────────────────────────────────


def test_app_importable() -> None:
    from pyui import App

    assert callable(App)


def test_page_importable() -> None:
    from pyui import Page

    p = Page(title="Test", route="/")
    assert p.title == "Test"
    assert p.route == "/"


# ── Bonus: reactive importable ────────────────────────────────────────────────


def test_reactive_importable() -> None:
    from pyui import reactive

    count = reactive(0)
    assert count.get() == 0


# ── Bonus: components importable ─────────────────────────────────────────────


def test_components_importable() -> None:
    from pyui import Button, Heading, Text

    btn = Button("Click me")
    txt = Text("Hello")
    hdg = Heading("Title", level=1)
    assert btn.props["label"] == "Click me"
    assert txt.props["content"] == "Hello"
    assert hdg.props["text"] == "Title"
