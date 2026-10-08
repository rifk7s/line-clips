"""Cohen-Sutherland line clipping algorithm.

Region codes use canvas coordinates (y grows downward):
  TOP    - y < ymin  (visually above the window's top edge)
  BOTTOM - y > ymax  (visually below the window's bottom edge)
  LEFT   - x < xmin
  RIGHT  - x > xmax

Returns the clipped Segment, or None if the segment is fully outside.
The <1 px degenerate filter is applied in clip_shape(), not here.
"""

from __future__ import annotations

from app.geometry import Point, Rect, Segment

# Region codes (4-bit bitmask)
_INSIDE = 0  # 0000
_LEFT = 1  # 0001  x < xmin
_RIGHT = 2  # 0010  x > xmax
_TOP = 4  # 0100  y < ymin  (canvas: visually above top edge)
_BOTTOM = 8  # 1000  y > ymax  (canvas: visually below bottom edge)

_MAX_ITER = 10  # guard against floating-point infinite loops


def _region_code(x: float, y: float, win: Rect) -> int:
    code = _INSIDE
    if x < win.xmin:
        code |= _LEFT
    elif x > win.xmax:
        code |= _RIGHT
    if y < win.ymin:
        code |= _TOP  # canvas: y < ymin is above the top edge
    elif y > win.ymax:
        code |= _BOTTOM  # canvas: y > ymax is below the bottom edge
    return code


def clip_segment(segment: Segment, window: Rect) -> Segment | None:
    """Clip *segment* against *window*.  Returns clipped Segment or None."""
    x0, y0 = segment.start.x, segment.start.y
    x1, y1 = segment.end.x, segment.end.y

    code0 = _region_code(x0, y0, window)
    code1 = _region_code(x1, y1, window)

    for _ in range(_MAX_ITER):
        if not (code0 | code1):
            # Trivial accept - both endpoints inside
            return Segment(Point(x0, y0), Point(x1, y1))

        if code0 & code1:
            # Trivial reject - both endpoints in the same outside region
            return None

        # Pick an outside point and clip it to the boundary
        outside = code0 if code0 else code1

        dx = x1 - x0
        dy = y1 - y0

        if outside & _BOTTOM:  # y > ymax
            t = (window.ymax - y0) / dy if dy != 0 else 0.0
            x = x0 + t * dx
            y = window.ymax
        elif outside & _TOP:  # y < ymin
            t = (window.ymin - y0) / dy if dy != 0 else 0.0
            x = x0 + t * dx
            y = window.ymin
        elif outside & _RIGHT:  # x > xmax
            t = (window.xmax - x0) / dx if dx != 0 else 0.0
            x = window.xmax
            y = y0 + t * dy
        else:  # _LEFT: x < xmin
            t = (window.xmin - x0) / dx if dx != 0 else 0.0
            x = window.xmin
            y = y0 + t * dy

        if outside == code0:
            x0, y0 = x, y
            code0 = _region_code(x0, y0, window)
        else:
            x1, y1 = x, y
            code1 = _region_code(x1, y1, window)

    # Iteration guard exhausted - treat as rejected to avoid bad output
    return None
