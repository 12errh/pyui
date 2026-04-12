"""
Global state store — app-wide shared reactive state.

Usage::

    from pyui.state.store import store

    username = store.define("username", "Guest")
    store.get("username").set("Alice")
    store.snapshot()  # → {"username": "Alice"}
"""

from __future__ import annotations

from typing import Any

from pyui.exceptions import PyUIError
from pyui.state.reactive import ReactiveVar, reactive


class Store:
    """
    Global singleton that holds named :class:`~pyui.state.reactive.ReactiveVar`
    instances, accessible across pages and components.
    """

    def __init__(self) -> None:
        self._state: dict[str, ReactiveVar[Any]] = {}

    # ── API ───────────────────────────────────────────────────────────────────

    def define(self, key: str, initial: Any) -> ReactiveVar[Any]:
        """
        Define a new reactive variable in the store.

        Parameters
        ----------
        key : str
            Unique identifier for the variable.
        initial :
            Initial value.

        Returns
        -------
        ReactiveVar
            The newly created variable.

        Raises
        ------
        PyUIError
            If *key* is already defined.
        """
        if key in self._state:
            raise PyUIError(
                f"Store key '{key}' is already defined. Use store.get('{{key}}') to access it."
            )
        var: ReactiveVar[Any] = reactive(initial)
        self._state[key] = var
        return var

    def get(self, key: str) -> ReactiveVar[Any]:
        """
        Retrieve a reactive variable by key.

        Raises
        ------
        PyUIError
            If *key* has not been defined.
        """
        if key not in self._state:
            raise PyUIError(
                f"Store key '{key}' is not defined. "
                "Call store.define('{key}', initial_value) first."
            )
        return self._state[key]

    def snapshot(self) -> dict[str, Any]:
        """Return a plain dict of all current values (not reactive)."""
        return {k: v.get() for k, v in self._state.items()}

    def reset(self) -> None:
        """Clear all state. Useful in tests."""
        self._state.clear()

    def __repr__(self) -> str:
        keys = list(self._state.keys())
        return f"Store(keys={keys!r})"


# Singleton — import this in user code
store = Store()
