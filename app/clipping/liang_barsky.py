"""Liang-Barsky line clipping algorithm.

Parametric form: P(t) = P1 + t*(P2 - P1),  t in [0, 1].

  p = [-dx, dx, -dy, dy]
  q = [x1-xmin, xmax-x1, y1-ymin, ymax-y1]

Window edges are inclusive (q >= 0 accepted at boundary).

Returns the clipped Segment, or None if fully outside.
The <1 px degenerate filter is applied in clip_shape(), not here.
"""

from __future__ import annotations

from app.geometry import Point, Rect, Segment


def clip_segment(segment: Segment, window: Rect) -> Segment | None:
    """Clip *segment* against *window*.  Returns clipped Segment or None."""
    x1, y1 = segment.start.x, segment.start.y
    x2, y2 = segment.end.x, segment.end.y

    dx = x2 - x1
    dy = y2 - y1

    p = [-dx, dx, -dy, dy]
    q = [
        x1 - window.xmin,  # LEFT   boundary:  x >= xmin
        window.xmax - x1,  # RIGHT  boundary:  x <= xmax
        y1 - window.ymin,  # TOP    boundary:  y >= ymin  (canvas: above top edge)
        window.ymax - y1,  # BOTTOM boundary:  y <= ymax  (canvas: below bottom edge)
    ]

    t_enter = 0.0  # max of all entering t-values
    t_exit = 1.0  # min of all exiting  t-values

    for pi, qi in zip(p, q):
        if pi == 0:
            # Parallel to this boundary
            if qi < 0:
                # Outside and parallel - fully rejected
                return None
            # else: inside and parallel - no constraint from this boundary
        elif pi < 0:
            # Entering intersection
            t = qi / pi
            t_enter = max(t_enter, t)
        else:
            # Exiting intersection
            t = qi / pi
            t_exit = min(t_exit, t)

    if t_enter > t_exit:
        return None  # fully outside

    # Direction preservation: t_enter < t_exit guarantees same direction as original.
    clipped_start = Point(x1 + t_enter * dx, y1 + t_enter * dy)
    clipped_end = Point(x1 + t_exit * dx, y1 + t_exit * dy)
    return Segment(clipped_start, clipped_end)
