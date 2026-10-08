"""Toolbar panel - Buat, Algoritma, Atribut panels.

Uses ttk widgets throughout (tk.Button ignores color on macOS).
"""

from __future__ import annotations

import tkinter as tk
from collections.abc import Callable
from tkinter import ttk

from app.clipping import Algorithm
from app.shapes import COLOR_NAMES, THICKNESS_OPTIONS


class Toolbar(ttk.Frame):
    """Top toolbar containing three sub-panels: Buat, Algoritma, Atribut."""

    def __init__(
        self,
        parent: tk.Widget,
        on_tool_change: Callable[[], None],
        on_algo_change: Callable[[], None],
        on_attr_change: Callable[[], None],
    ) -> None:
        super().__init__(parent, relief="flat")
        self._on_tool_change = on_tool_change
        self._on_algo_change = on_algo_change
        self._on_attr_change = on_attr_change

        # BooleanVar for each Buat tool
        self.var_garis = tk.BooleanVar(value=True)
        self.var_area_clip = tk.BooleanVar(value=False)
        self.var_kotak = tk.BooleanVar(value=False)
        self.var_lingkaran = tk.BooleanVar(value=False)

        # Algorithm radio
        self.var_algo = tk.StringVar(value=Algorithm.COHEN_SUTHERLAND.value)

        # Attribute comboboxes
        self.var_color = tk.StringVar(value=COLOR_NAMES[0])  # Hitam
        self.var_thickness = tk.IntVar(value=2)

        self._build()

    # [ Build UI ]

    def _build(self) -> None:
        # Panel Buat
        buat_frame = ttk.LabelFrame(self, text="Buat")
        buat_frame.pack(side="left", padx=(4, 8), pady=4, fill="y")

        tools = [
            ("Garis", self.var_garis),
            ("Area Clipping", self.var_area_clip),
            ("Kotak (opsional)", self.var_kotak),
            ("Lingkaran (opsional)", self.var_lingkaran),
        ]
        for label, var in tools:
            cb = ttk.Checkbutton(
                buat_frame,
                text=label,
                variable=var,
                command=self._on_tool_change,
            )
            cb.pack(anchor="w", padx=4, pady=1)

        # Panel Algoritma
        algo_frame = ttk.LabelFrame(self, text="Algoritma")
        algo_frame.pack(side="left", padx=8, pady=4, fill="y")

        algos = [
            ("Cohen-Sutherland", Algorithm.COHEN_SUTHERLAND.value),
            ("Liang-Barsky", Algorithm.LIANG_BARSKY.value),
        ]
        for label, value in algos:
            rb = ttk.Radiobutton(
                algo_frame,
                text=label,
                variable=self.var_algo,
                value=value,
                command=self._on_algo_change,
            )
            rb.pack(anchor="w", padx=4, pady=1)

        # Panel Atribut Warna dan Ketebalan
        attr_frame = ttk.LabelFrame(self, text="Atribut Warna dan Ketebalan")
        attr_frame.pack(side="left", padx=8, pady=4, fill="y")

        # Color
        ttk.Label(attr_frame, text="Warna:").grid(row=0, column=0, sticky="w", padx=4, pady=2)
        color_cb = ttk.Combobox(
            attr_frame,
            textvariable=self.var_color,
            values=COLOR_NAMES,
            state="readonly",
            width=10,
        )
        color_cb.grid(row=0, column=1, padx=4, pady=2)
        color_cb.bind("<<ComboboxSelected>>", lambda _e: self._on_attr_change())

        # Thickness
        ttk.Label(attr_frame, text="Ketebalan:").grid(row=1, column=0, sticky="w", padx=4, pady=2)
        thick_cb = ttk.Combobox(
            attr_frame,
            textvariable=self.var_thickness,
            values=THICKNESS_OPTIONS,
            state="readonly",
            width=10,
        )
        thick_cb.grid(row=1, column=1, padx=4, pady=2)
        thick_cb.bind("<<ComboboxSelected>>", lambda _e: self._on_attr_change())

    # [ Property accessors used by main_window / canvas_view ]

    @property
    def active_tools(self) -> dict[str, bool]:
        return {
            "garis": self.var_garis.get(),
            "area_clip": self.var_area_clip.get(),
            "kotak": self.var_kotak.get(),
            "lingkaran": self.var_lingkaran.get(),
        }

    @property
    def algorithm(self) -> Algorithm:
        return Algorithm(self.var_algo.get())

    @property
    def color(self) -> str:
        return self.var_color.get()

    @property
    def thickness(self) -> int:
        return int(self.var_thickness.get())

    def active_tool_names(self) -> list[str]:
        """Human-readable names of checked tools, in display order."""
        mapping = [
            ("garis", "Garis"),
            ("area_clip", "Area Clipping"),
            ("kotak", "Kotak"),
            ("lingkaran", "Lingkaran"),
        ]
        return [label for key, label in mapping if self.active_tools[key]]
