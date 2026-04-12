"""
PyUI — Write Python. Render anywhere.

Web · Desktop · CLI from a single Python codebase.
"""

from __future__ import annotations

__version__ = "0.1.0"
__author__ = "PyUI Core Team"
__license__ = "MIT"

# ── Core classes ─────────────────────────────────────────────────────────────
from pyui.app import App

# ── Compiler public API ───────────────────────────────────────────────────────
from pyui.compiler import compile_app

# ── Components ────────────────────────────────────────────────────────────────
from pyui.components.base import BaseComponent
from pyui.components.display.heading import Heading
from pyui.components.display.text import Text
from pyui.components.input.button import Button
from pyui.components.layout.grid import Grid

# ── Exceptions ────────────────────────────────────────────────────────────────
from pyui.exceptions import (
    CompilerError,
    ComponentError,
    PluginError,
    PyUIError,
    ThemeError,
)
from pyui.page import Page
from pyui.state.computed import computed

# ── State system ─────────────────────────────────────────────────────────────
from pyui.state.reactive import ReactiveVar, reactive
from pyui.state.store import Store, store

__all__ = [
    # Meta
    "__version__",
    # Core
    "App",
    "Page",
    # State
    "ReactiveVar",
    "reactive",
    "computed",
    "Store",
    "store",
    # Components
    "BaseComponent",
    "Button",
    "Text",
    "Heading",
    "Grid",
    # Compiler
    "compile_app",
    # Exceptions
    "PyUIError",
    "CompilerError",
    "ComponentError",
    "ThemeError",
    "PluginError",
]
