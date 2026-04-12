"""
Computed values — reactive values derived from other reactive values.

Usage::

    from pyui.state.reactive import reactive
    from pyui.state.computed import computed

    count = reactive(3)
    doubled = computed(lambda: count.get() * 2)

    doubled.get()  # → 6
    count.set(5)
    doubled.get()  # → 10
"""

from __future__ import annotations

from collections.abc import Callable
from typing import TypeVar

from pyui.state.reactive import ReactiveVar

T = TypeVar("T")


class ComputedVar(ReactiveVar[T]):
    """
    A read-only :class:`~pyui.state.reactive.ReactiveVar` whose value
    is derived from a computation function.

    The value is re-computed eagerly whenever any dependency calls
    :meth:`invalidate`. In Phase 3 this will grow automatic dependency
    tracking; for now invalidation is manual or triggered by explicit
    subscriptions wired by the user.
    """

    def __init__(self, fn: Callable[[], T]) -> None:
        self._fn = fn
        super().__init__(fn())

    def get(self) -> T:
        """Re-evaluate and return the computed value."""
        self._value = self._fn()
        return self._value

    def set(self, value: T) -> None:
        """Computed vars are read-only. Raises ``AttributeError``."""
        raise AttributeError("Cannot set a computed value directly.")

    def invalidate(self) -> None:
        """
        Recompute the value and notify subscribers if it changed.

        Call this from a dependency's subscriber to propagate changes::

            count.subscribe(lambda _: doubled.invalidate())
        """
        old = self._value
        self._value = self._fn()
        if old != self._value:
            self._notify()

    def __repr__(self) -> str:
        return f"ComputedVar(value={self._value!r}, fn={self._fn})"


def computed(fn: Callable[[], T]) -> ComputedVar[T]:
    """
    Create a :class:`ComputedVar` from a zero-argument callable.

    ::

        count   = reactive(0)
        doubled = computed(lambda: count.get() * 2)
        # Wire invalidation (Phase 3 will do this automatically):
        count.subscribe(lambda _: doubled.invalidate())
    """
    return ComputedVar(fn)
