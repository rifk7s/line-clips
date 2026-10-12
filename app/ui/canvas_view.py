"""Canvas view - mouse events, rubber-band preview, and the single redraw().

Drawing layers (bottom to top):
  0: Halo for selected shape   (orange, width+6)
  1: Original shapes           (solid if no window; gray dashed width=1 if window exists)
  2: Clipped result            (solid with shape attrs, only if window exists + non-empty result)
  3: Clipping window outline   (blue, 2 px)

Preview during drag: dashed rubber-band for each active tool.
"""

from __future__ import annotations

import math
import tkinter as tk
from collections.abc import Callable

from app.clipping import Algorithm, ClipResult, ClipStatus
from app.geometry import Point, Rect
from app.shapes import (
    COLOR_GHOST,
    COLOR_HALO,
    COLOR_MAP,
    COLOR_WINDOW,
    AnyShape,
    Line,
    _circle_segments,
)

# Canvas tag names for each layer
_TAG_HALO = "halo"
_TAG_GHOST = "ghost"
_TAG_CLIPPED = "clipped"
_TAG_WINDOW = "window"
_TAG_PREVIEW = "preview"


def _pts_to_flat(points: tuple[Point, ...]) -> list[float]:
    flat = []
    for p in points:
        flat.extend([p.x, p.y])
    return flat


def _hex_color(name: str) -> str:
    return COLOR_MAP.get(name, "#000000")


class CanvasView(tk.Canvas):
    """The main drawing canvas."""

    def __init__(
        self,
        parent: tk.Misc,
        on_drag_done: Callable[[Point, Point], None],
        get_tools: Callable[[], dict[str, bool]],
        get_color: Callable[[], str],
        get_thickness: Callable[[], int],
        get_algorithm: Callable[[], Algorithm],
    ) -> None:
        super().__init__(parent, bg="white", cursor="crosshair")

        self._on_drag_done = on_drag_done
        self._get_tools = get_tools
        self._get_color = get_color
        self._get_thickness = get_thickness
        self._get_algorithm = get_algorithm

        self._drag_start: Point | None = None

        self.bind("<ButtonPress-1>", self._on_press)
        self.bind("<B1-Motion>", self._on_motion)
        self.bind("<ButtonRelease-1>", self._on_release)

    # [ Mouse events ]

    def _on_press(self, event: tk.Event) -> None:  # type: ignore[type-arg]
        self._drag_start = Point(float(event.x), float(event.y))

    def _on_motion(self, event: tk.Event) -> None:  # type: ignore[type-arg]
        if self._drag_start is None:
            return
        self._draw_preview(self._drag_start, Point(float(event.x), float(event.y)))

    def _on_release(self, event: tk.Event) -> None:  # type: ignore[type-arg]
        self.delete(_TAG_PREVIEW)
        if self._drag_start is None:
            return
        p0, p1 = self._drag_start, Point(float(event.x), float(event.y))
        self._drag_start = None
        self._on_drag_done(p0, p1)

    # [ Rubber-band preview during drag ]

    def _draw_preview(self, p0: Point, p1: Point) -> None:
        self.delete(_TAG_PREVIEW)
        tools = self._get_tools()
        color_hex = _hex_color(self._get_color())
        w = self._get_thickness()
        rect = Rect.from_points(p0, p1)

        dash = (6, 4)

        # Garis preview
        if tools["garis"]:
            seg_len = (p1 - p0).length()
            if seg_len >= 3:
                self.create_line(
                    p0.x,
                    p0.y,
                    p1.x,
                    p1.y,
                    dash=dash,
                    fill=color_hex,
                    width=w,
                    tags=_TAG_PREVIEW,
                    capstyle=tk.ROUND,
                )

        # Kotak preview
        if tools["kotak"] and rect.width >= 3 and rect.height >= 3:
            tl, tr, br, bl = rect.corners()
            pts = [tl, tr, br, bl, tl]
            self.create_line(
                _pts_to_flat(tuple(pts)),
                dash=dash,
                fill=color_hex,
                width=w,
                tags=_TAG_PREVIEW,
                smooth=False,
            )

        # Lingkaran preview
        if tools["lingkaran"] and rect.width >= 3 and rect.height >= 3:
            cx, cy = rect.center.x, rect.center.y
            r = min(rect.width, rect.height) / 2.0
            n = _circle_segments(r)
            pts_c = [
                Point(
                    cx + r * math.cos(2 * math.pi * i / n), cy + r * math.sin(2 * math.pi * i / n)
                )
                for i in range(n)
            ]
            pts_c.append(pts_c[0])  # close
            self.create_line(
                _pts_to_flat(tuple(pts_c)),
                dash=dash,
                fill=color_hex,
                width=w,
                tags=_TAG_PREVIEW,
                smooth=False,
            )

        # Area Clipping preview
        if tools["area_clip"] and rect.width >= 3 and rect.height >= 3:
            tl, tr, br, bl = rect.corners()
            pts = [tl, tr, br, bl, tl]
            self.create_line(
                _pts_to_flat(tuple(pts)),
                dash=(8, 4),
                fill=COLOR_WINDOW,
                width=2,
                tags=_TAG_PREVIEW,
                smooth=False,
            )

    # [ Idempotent redraw ]

    def redraw(
        self,
        shapes: tuple[AnyShape, ...],
        clip_window: Rect | None,
        results: list[ClipResult] | None,
        selected_idx: int | None,
        algorithm: Algorithm,
    ) -> None:
        """Delete all tagged items and repaint all layers from scratch."""
        for tag in (_TAG_HALO, _TAG_GHOST, _TAG_CLIPPED, _TAG_WINDOW):
            self.delete(tag)

        has_window = clip_window is not None

        # Layer 0: halo for selected shape
        if selected_idx is not None and 0 <= selected_idx < len(shapes):
            self._draw_halo(shapes[selected_idx])

        # Layer 1: original shapes (ghost or solid)
        for shape in shapes:
            self._draw_shape_layer1(shape, has_window)

        # Layer 2: clipped results (only if window exists)
        if has_window and results is not None:
            for shape, result in zip(shapes, results):
                if result.status != ClipStatus.REJECTED:
                    self._draw_clipped(shape, result)

        # Layer 3: clipping window outline
        if has_window and clip_window is not None:
            tl, tr, br, bl = clip_window.corners()
            pts = [tl, tr, br, bl, tl]
            self.create_line(
                _pts_to_flat(tuple(pts)),
                fill=COLOR_WINDOW,
                width=2,
                tags=_TAG_WINDOW,
                smooth=False,
            )

    # [ Drawing helpers ]

    def _draw_halo(self, shape: AnyShape) -> None:
        segs = shape.to_segments()
        w = (shape.width if hasattr(shape, "width") else 2) + 6

        if isinstance(shape, Line):
            s = segs[0]
            self.create_line(
                s.start.x,
                s.start.y,
                s.end.x,
                s.end.y,
                fill=COLOR_HALO,
                width=w,
                tags=_TAG_HALO,
                capstyle=tk.ROUND,
            )
        else:
            # Closed shape: draw as single closed polyline
            pts = [s.start for s in segs]
            pts.append(pts[0])
            self.create_line(
                _pts_to_flat(tuple(pts)),
                fill=COLOR_HALO,
                width=w,
                tags=_TAG_HALO,
                smooth=False,
            )

    def _draw_shape_layer1(self, shape: AnyShape, has_window: bool) -> None:
        segs = shape.to_segments()
        color = COLOR_GHOST if has_window else _hex_color(shape.color)
        width = 1 if has_window else shape.width
        dash = (5, 4) if has_window else None

        opts: dict = {"fill": color, "width": width, "tags": _TAG_GHOST, "capstyle": tk.ROUND}
        if dash:
            opts["dash"] = dash

        if isinstance(shape, Line):
            s = segs[0]
            self.create_line(s.start.x, s.start.y, s.end.x, s.end.y, **opts)
        else:
            pts = [s.start for s in segs]
            pts.append(pts[0])
            self.create_line(_pts_to_flat(tuple(pts)), smooth=False, **opts)

    def _draw_clipped(self, shape: AnyShape, result: ClipResult) -> None:
        color_hex = _hex_color(shape.color)
        width = shape.width
        for polyline in result.polylines:
            if len(polyline) < 2:
                continue
            self.create_line(
                _pts_to_flat(polyline),
                fill=color_hex,
                width=width,
                tags=_TAG_CLIPPED,
                joinstyle=tk.ROUND,
                capstyle=tk.ROUND,
            )
