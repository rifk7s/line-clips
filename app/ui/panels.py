"""Side panels - two Listboxes (before/after clipping) with scrollbars.

Selection sync: clicking a row in either list selects the same shape index
in both lists and triggers the on_select callback (for halo redraw).
"""

from __future__ import annotations

import tkinter as tk
from collections.abc import Callable
from tkinter import font as tkfont
from tkinter import ttk

from app.clipping import ClipResult, ClipStatus
from app.shapes import AnyShape, Box, Circle, Line

_STATUS_TEXT = {
    ClipStatus.FULL: "terlihat penuh",
    ClipStatus.PARTIAL: "terpotong",
    ClipStatus.REJECTED: "ditolak",
}


def _before_row(idx: int, shape: AnyShape) -> str:
    return f"#{idx + 1:<3} {shape.before_label()}"


def _after_row(idx: int, shape: AnyShape, result: ClipResult) -> str:
    prefix = f"#{idx + 1:<3} "
    st = result.status

    if isinstance(shape, Line):
        if st == ClipStatus.REJECTED:
            return prefix + "Garis      ditolak"
        pts = result.polylines[0]
        s = pts[0].as_int()
        e = pts[-1].as_int()
        suffix = " *" if st == ClipStatus.PARTIAL else ""
        return prefix + f"Garis      ({s[0]},{s[1]})→({e[0]},{e[1]}){suffix}"

    if isinstance(shape, Box):
        if st == ClipStatus.REJECTED:
            return prefix + "Kotak      ditolak"
        if st == ClipStatus.FULL:
            return prefix + "Kotak      terlihat penuh"
        n = result.visible_count
        return prefix + f"Kotak      terpotong, {n} dari 4 sisi terlihat"

    if isinstance(shape, Circle):
        if st == ClipStatus.REJECTED:
            return prefix + "Lingkaran  ditolak"
        if st == ClipStatus.FULL:
            return prefix + "Lingkaran  terlihat penuh"
        n = result.visible_count
        return prefix + f"Lingkaran  terpotong, {n} busur terlihat"

    return prefix + "?"  # unreachable


class SidePanels(ttk.Frame):
    """Right-side panel with two listboxes stacked vertically."""

    def __init__(
        self,
        parent: tk.Misc,
        on_select: Callable[[int], None],
    ) -> None:
        super().__init__(parent)
        self._on_select = on_select
        self._shape_count = 0  # number of real shapes currently displayed
        self._syncing = False  # re-entrancy guard

        fixed_font = tkfont.nametofont("TkFixedFont")

        # Before clipping
        ttk.Label(self, text="Daftar Garis sebelum Clipping").pack(anchor="w", padx=4)
        before_frame = ttk.Frame(self)
        before_frame.pack(fill="both", expand=True, padx=4, pady=(0, 4))

        self._before_lb = tk.Listbox(
            before_frame,
            font=fixed_font,
            exportselection=False,
            selectmode=tk.SINGLE,
            activestyle="none",
            width=36,
        )
        before_scroll = ttk.Scrollbar(before_frame, command=self._before_lb.yview)
        self._before_lb.configure(yscrollcommand=before_scroll.set)
        self._before_lb.pack(side="left", fill="both", expand=True)
        before_scroll.pack(side="right", fill="y")
        self._before_lb.bind("<<ListboxSelect>>", self._on_before_select)

        # After clipping
        ttk.Label(self, text="Daftar Garis setelah Clipping").pack(anchor="w", padx=4)
        after_frame = ttk.Frame(self)
        after_frame.pack(fill="both", expand=True, padx=4, pady=(0, 4))

        self._after_lb = tk.Listbox(
            after_frame,
            font=fixed_font,
            exportselection=False,
            selectmode=tk.SINGLE,
            activestyle="none",
            width=36,
        )
        after_scroll = ttk.Scrollbar(after_frame, command=self._after_lb.yview)
        self._after_lb.configure(yscrollcommand=after_scroll.set)
        self._after_lb.pack(side="left", fill="both", expand=True)
        after_scroll.pack(side="right", fill="y")
        self._after_lb.bind("<<ListboxSelect>>", self._on_after_select)

        # Legend
        ttk.Label(self, text="* = hasil sudah dipotong", foreground="gray").pack(
            anchor="w", padx=4, pady=(2, 4)
        )

    # [ Public update API ]

    def update_lists(
        self,
        shapes: tuple[AnyShape, ...],
        results: list[ClipResult] | None,
    ) -> None:
        """Repopulate both listboxes. results=None means no window defined."""
        self._shape_count = len(shapes)

        # Before list
        self._before_lb.delete(0, tk.END)
        for i, shape in enumerate(shapes):
            self._before_lb.insert(tk.END, _before_row(i, shape))

        # After list
        self._after_lb.delete(0, tk.END)
        if results is None:
            self._after_lb.insert(tk.END, "Belum ada area clipping")
        else:
            for i, (shape, result) in enumerate(zip(shapes, results)):
                self._after_lb.insert(tk.END, _after_row(i, shape, result))

    def clear_selection(self) -> None:
        self._before_lb.selection_clear(0, tk.END)
        self._after_lb.selection_clear(0, tk.END)

    def set_selection(self, shape_idx: int) -> None:
        """Select a row by shape index in both listboxes (does not fire callback)."""
        self._syncing = True
        try:
            self._before_lb.selection_clear(0, tk.END)
            self._after_lb.selection_clear(0, tk.END)
            if 0 <= shape_idx < self._before_lb.size():
                self._before_lb.selection_set(shape_idx)
                self._before_lb.see(shape_idx)
            if 0 <= shape_idx < self._after_lb.size():
                # After-list may show "Belum ada area clipping" as row 0 → skip
                after_size = self._after_lb.size()
                if after_size == self._shape_count and shape_idx < after_size:
                    self._after_lb.selection_set(shape_idx)
                    self._after_lb.see(shape_idx)
        finally:
            self._syncing = False

    # [ Internal selection handlers ]

    def _on_before_select(self, _event: tk.Event) -> None:  # type: ignore[type-arg]
        if self._syncing:
            return
        sel = self._before_lb.curselection()
        if not sel:
            return
        idx = sel[0]
        if idx >= self._shape_count:
            return
        self.set_selection(idx)
        self._on_select(idx)

    def _on_after_select(self, _event: tk.Event) -> None:  # type: ignore[type-arg]
        if self._syncing:
            return
        sel = self._after_lb.curselection()
        if not sel:
            return
        idx = sel[0]
        # If after-list shows "Belum ada area clipping", size != shape_count
        if self._after_lb.size() != self._shape_count:
            return
        if idx >= self._shape_count:
            return
        self.set_selection(idx)
        self._on_select(idx)
