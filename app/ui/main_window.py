"""Main window - thin controller that wires toolbar, canvas, panels, and scene.

Layout (grid):
  Row 0: Toolbar (columnspan=2)
  Row 1: Canvas (col 0) | SidePanels (col 1)
  Row 2: Status bar (columnspan=2)
"""

from __future__ import annotations

import sys
import tkinter as tk
from tkinter import ttk

from app.clipping import ClipResult, clip_shape
from app.geometry import Point, Rect
from app.scene import Scene
from app.shapes import AnyShape, Box, Circle, Line
from app.ui.canvas_view import CanvasView
from app.ui.panels import SidePanels
from app.ui.toolbar import Toolbar


class MainWindow:
    def __init__(self, root: tk.Tk) -> None:
        self._root = root
        root.title("Line Clipping App")
        root.resizable(True, True)

        self._scene = Scene()
        self._results: list[ClipResult] | None = None
        self._selected_idx: int | None = None
        self._pending_refresh = False  # after_idle guard

        self._build_menu()
        self._build_layout()
        self._bind_keys()
        self._refresh()

    # Layout

    def _build_layout(self) -> None:
        self._root.columnconfigure(0, weight=1)
        self._root.columnconfigure(1, weight=0)
        self._root.rowconfigure(1, weight=1)

        # Toolbar
        self._toolbar = Toolbar(
            self._root,
            on_tool_change=self._on_tool_change,
            on_algo_change=self._on_algo_change,
            on_attr_change=lambda: None,  # no action needed
        )
        self._toolbar.grid(row=0, column=0, columnspan=2, sticky="ew")

        # Canvas
        self._canvas = CanvasView(
            self._root,
            on_drag_done=self._on_drag_done,
            get_tools=lambda: self._toolbar.active_tools,
            get_color=lambda: self._toolbar.color,
            get_thickness=lambda: self._toolbar.thickness,
            get_algorithm=lambda: self._toolbar.algorithm,
        )
        self._canvas.grid(row=1, column=0, sticky="nsew")

        # Side panels
        self._panels = SidePanels(self._root, on_select=self._on_select)
        self._panels.grid(row=1, column=1, sticky="ns", padx=(0, 4), pady=4)

        # Status bar
        self._status_var = tk.StringVar(value="")
        status_bar = ttk.Label(
            self._root,
            textvariable=self._status_var,
            relief="sunken",
            anchor="w",
            padding=(4, 2),
        )
        status_bar.grid(row=2, column=0, columnspan=2, sticky="ew")

        self._update_status()

    def _build_menu(self) -> None:
        menu = tk.Menu(self._root)
        self._root.configure(menu=menu)

        self._edit_menu = tk.Menu(menu, tearoff=False)
        menu.add_cascade(label="Edit", menu=self._edit_menu)

        is_mac = sys.platform == "darwin"
        undo_accel = "Cmd+Z" if is_mac else "Ctrl+Z"
        redo_accel = "Cmd+Shift+Z" if is_mac else "Ctrl+Y"
        clear_accel = "Cmd+Shift+Backspace" if is_mac else "Ctrl+Shift+Del"

        self._edit_menu.add_command(
            label="Urungkan (Undo)",
            accelerator=undo_accel,
            command=self._undo,
        )
        self._edit_menu.add_command(
            label="Ulangi (Redo)",
            accelerator=redo_accel,
            command=self._redo,
        )
        self._edit_menu.add_separator()
        self._edit_menu.add_command(
            label="Hapus Semua",
            accelerator=clear_accel,
            command=self._clear,
        )

    def _bind_keys(self) -> None:
        root = self._root
        is_mac = sys.platform == "darwin"

        if is_mac:
            root.bind_all("<Command-z>", lambda e: self._undo())
            root.bind_all("<Command-Z>", lambda e: self._undo())
            root.bind_all("<Command-Shift-z>", lambda e: self._redo())
            root.bind_all("<Command-Shift-Z>", lambda e: self._redo())
            root.bind_all("<Command-Shift-BackSpace>", lambda e: self._clear())
        else:
            root.bind_all("<Control-z>", lambda e: self._undo())
            root.bind_all("<Control-Z>", lambda e: self._undo())
            root.bind_all("<Control-y>", lambda e: self._redo())
            root.bind_all("<Control-Y>", lambda e: self._redo())
            root.bind_all("<Control-Shift-Delete>", lambda e: self._clear())

    # Callbacks

    def _on_drag_done(self, p0: Point, p1: Point) -> None:
        tools = self._toolbar.active_tools
        color = self._toolbar.color
        thick = self._toolbar.thickness

        names = self._toolbar.active_tool_names()
        if not names:
            self._status_var.set("Pilih minimal satu tool di panel Buat")
            return

        new_shapes: list[AnyShape] = []

        rect = Rect.from_points(p0, p1)
        seg_len = (p1 - p0).length()

        if tools["garis"] and seg_len >= 3:
            new_shapes.append(Line(p0, p1, color, thick))

        if tools["kotak"] and rect.width >= 3 and rect.height >= 3:
            new_shapes.append(Box(rect, color, thick))

        if tools["lingkaran"] and rect.width >= 3 and rect.height >= 3:
            cx, cy = rect.center.x, rect.center.y
            r = min(rect.width, rect.height) / 2.0
            new_shapes.append(Circle(Point(cx, cy), r, color, thick))

        # Area Clipping: replaces window; does NOT go into shapes list
        if tools["area_clip"] and rect.width >= 3 and rect.height >= 3:
            if new_shapes:
                # Add shapes first, then set window (two undo steps intentionally merged)
                self._scene.add_shapes(new_shapes)
                new_shapes = []
            self._scene.set_window(rect)
        elif new_shapes:
            self._scene.add_shapes(new_shapes)

        self._selected_idx = None
        self._panels.clear_selection()
        self._schedule_refresh()

    def _on_algo_change(self) -> None:
        self._schedule_refresh()

    def _on_tool_change(self) -> None:
        self._update_status()

    def _on_select(self, idx: int) -> None:
        self._selected_idx = idx
        # Only redraw for halo - do NOT re-run clipping
        self._canvas.redraw(
            self._scene.shapes,
            self._scene.clip_window,
            self._results,
            self._selected_idx,
            self._toolbar.algorithm,
        )

    # Undo / Redo / Clear

    def _undo(self) -> None:
        if self._scene.undo():
            self._selected_idx = None
            self._panels.clear_selection()
            self._schedule_refresh()

    def _redo(self) -> None:
        if self._scene.redo():
            self._selected_idx = None
            self._panels.clear_selection()
            self._schedule_refresh()

    def _clear(self) -> None:
        self._scene.clear()
        self._selected_idx = None
        self._panels.clear_selection()
        self._schedule_refresh()

    # Refresh pipeline

    def _schedule_refresh(self) -> None:
        """Coalesce multiple triggers into one refresh per event-loop turn."""
        if not self._pending_refresh:
            self._pending_refresh = True
            self._root.after_idle(self._refresh)

    def _refresh(self) -> None:
        self._pending_refresh = False

        # Compute clipping results
        shapes = self._scene.shapes
        window = self._scene.clip_window
        algo = self._toolbar.algorithm

        if window is None:
            self._results = None
        else:
            self._results = [clip_shape(s, window, algo) for s in shapes]

        # Update panels
        self._panels.update_lists(shapes, self._results)

        # Update canvas
        self._canvas.redraw(shapes, window, self._results, self._selected_idx, algo)

        # Update menu item states
        self._update_menu()

        # Update status bar
        self._update_status()

    def _update_menu(self) -> None:
        self._edit_menu.entryconfigure(0, state="normal" if self._scene.can_undo() else "disabled")
        self._edit_menu.entryconfigure(1, state="normal" if self._scene.can_redo() else "disabled")

    def _update_status(self) -> None:
        names = self._toolbar.active_tool_names()
        if names:
            self._status_var.set("Aktif: " + " + ".join(names))
        else:
            self._status_var.set("Pilih minimal satu tool di panel Buat")
