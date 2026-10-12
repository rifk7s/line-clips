"""Pure application state - no tkinter import allowed in this module.

Stores:
  - shapes: ordered tuple of AnyShape
  - clip_window: Rect | None
  - undo/redo stacks of (shapes, window) snapshots

One undo step = one finished drag (even if it produced multiple shapes),
window replacement, or Clear.
Not undoable: algorithm change, Color/Thickness change.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from app.geometry import Rect

if TYPE_CHECKING:
    from app.shapes import AnyShape

_Snapshot = tuple[tuple["AnyShape", ...], Rect | None]


@dataclass
class Scene:
    shapes: tuple[AnyShape, ...] = field(default_factory=tuple)
    clip_window: Rect | None = None
    _undo_stack: list[_Snapshot] = field(default_factory=list, repr=False)
    _redo_stack: list[_Snapshot] = field(default_factory=list, repr=False)

    # Snapshot helpers

    def _snapshot(self) -> _Snapshot:
        return (self.shapes, self.clip_window)

    def _restore(self, snap: _Snapshot) -> None:
        self.shapes, self.clip_window = snap

    # Mutating operations (each pushes to undo and clears redo)

    def add_shapes(self, new_shapes: list[AnyShape]) -> None:
        """Append shapes from one finished drag. Clears redo stack."""
        self._push_undo()
        self.shapes = self.shapes + tuple(new_shapes)

    def apply_drag(self, new_shapes: list[AnyShape], window: Rect | None) -> None:
        """Apply everything one finished drag produced as a single undo step."""
        if not new_shapes and window is None:
            return
        self._push_undo()
        self.shapes = self.shapes + tuple(new_shapes)
        if window is not None:
            self.clip_window = window

    def set_window(self, rect: Rect) -> None:
        """Replace (or set) the clipping window. Clears redo stack."""
        self._push_undo()
        self.clip_window = rect

    def clear(self) -> None:
        """Clear all shapes and window. Does NOT push if already empty."""
        if self.shapes or self.clip_window is not None:
            self._push_undo()
        self.shapes = ()
        self.clip_window = None

    # Undo / Redo

    def _push_undo(self) -> None:
        self._undo_stack.append(self._snapshot())
        self._redo_stack.clear()

    def can_undo(self) -> bool:
        return bool(self._undo_stack)

    def can_redo(self) -> bool:
        return bool(self._redo_stack)

    def undo(self) -> bool:
        if not self._undo_stack:
            return False
        self._redo_stack.append(self._snapshot())
        self._restore(self._undo_stack.pop())
        return True

    def redo(self) -> bool:
        if not self._redo_stack:
            return False
        self._undo_stack.append(self._snapshot())
        self._restore(self._redo_stack.pop())
        return True
