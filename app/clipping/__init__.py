"""Clipping subsystem public API.

Algorithm enum, registry, ClipResult/ClipStatus, and the single clip_shape() entry point.
UI code only ever touches ClipResult - it never calls algorithm internals directly.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.shapes import Shape

from app.geometry import Point, Rect, Segment

# Algorithm enum + registry


class Algorithm(Enum):
    COHEN_SUTHERLAND = "cohen_sutherland"
    LIANG_BARSKY = "liang_barsky"


def _get_registry() -> dict:
    """Lazy import to avoid circular imports at module load time."""
    from app.clipping.cohen_sutherland import clip_segment as cs_clip
    from app.clipping.liang_barsky import clip_segment as lb_clip

    return {
        Algorithm.COHEN_SUTHERLAND: cs_clip,
        Algorithm.LIANG_BARSKY: lb_clip,
    }


# Result types


class ClipStatus(Enum):
    FULL = "full"  # all segments unchanged
    PARTIAL = "partial"  # at least one segment clipped or missing
    REJECTED = "rejected"  # no visible segments


@dataclass(frozen=True, slots=True)
class ClipResult:
    """Fully computed clipping result for one shape.

    polylines: each inner tuple is a sequence of Points forming one continuous
               visible arc/polyline. Pass directly to create_line(*points).
    visible_count:
        Line   - 1 if not rejected, else 0
        Box    - number of sides (0-4) with non-empty clip result
        Circle - number of contiguous visible arcs after merging
    total_count:
        Line   - 1
        Box    - 4
        Circle - adaptive segment count n
    """

    status: ClipStatus
    polylines: tuple[tuple[Point, ...], ...]
    visible_count: int
    total_count: int


# Shared degenerate filter

_MIN_LENGTH = 1.0  # px - segments shorter than this are treated as rejected


def _clip_segment_filtered(segment: Segment, window: Rect, algorithm: Algorithm) -> Segment | None:
    """Run the chosen algorithm then apply the shared <1 px filter."""
    registry = _get_registry()
    raw = registry[algorithm](segment, window)
    if raw is not None and raw.length() < _MIN_LENGTH:
        return None
    return raw


# clip_shape - the single clipping entry point


def clip_shape(shape: Shape, window: Rect, algorithm: Algorithm) -> ClipResult:
    """Clip a shape against window using the given algorithm.

    This is the *only* place where clipping is called.  UI code reads the
    returned ClipResult; it never calls algorithm functions directly.
    """
    segments = shape.to_segments()
    total = len(segments)

    clipped: list[Segment | None] = [_clip_segment_filtered(s, window, algorithm) for s in segments]

    visible = [s for s in clipped if s is not None]
    visible_count = len(visible)

    if visible_count == 0:
        return ClipResult(
            status=ClipStatus.REJECTED,
            polylines=(),
            visible_count=0,
            total_count=total,
        )

    # Determine overall status
    if visible_count == total and all(
        c is not None and c.start == o.start and c.end == o.end for c, o in zip(clipped, segments)
    ):
        status = ClipStatus.FULL
    else:
        status = ClipStatus.PARTIAL

    # Build polylines by merging consecutive visible arcs
    polylines = _build_polylines(segments, clipped, shape.is_closed())

    return ClipResult(
        status=status,
        polylines=polylines,
        visible_count=_count_arcs(polylines) if shape.is_closed() else visible_count,
        total_count=total,
    )


# Polyline / arc merging helpers


def _build_polylines(
    originals: list[Segment],
    clipped: list[Segment | None],
    closed: bool,
) -> tuple[tuple[Point, ...], ...]:
    """Merge adjacent visible clipped segments into continuous polylines.

    For closed shapes (Box, Circle) merging wraps around circularly so that
    an arc spanning the seam between the last and first segment is joined.

    Two consecutive segments are merged into one polyline only when the
    shared endpoint was NOT moved by clipping (i.e. it is the original
    unclipped interior point).  If either endpoint was clipped to the window
    boundary, the segments stay in separate polylines.
    """
    n = len(originals)
    if n == 0:
        return ()

    # For a Line (n==1) just return the single clipped segment.
    if n == 1:
        seg = clipped[0]
        if seg is None:
            return ()
        return ((seg.start, seg.end),)

    # Build groups of consecutive visible indices.
    # Each group will become one polyline.
    groups: list[list[int]] = []
    current: list[int] = []

    # Determine iteration order; for closed shapes we may need to wrap.
    indices = list(range(n))

    for i in indices:
        if clipped[i] is not None:
            current.append(i)
        else:
            if current:
                groups.append(current)
                current = []
    if current:
        groups.append(current)

    if not groups:
        return ()

    # For closed shapes: try to merge the last group with the first group
    # if they connect at the seam (index n-1 → index 0).
    if closed and len(groups) > 1:
        last_group = groups[-1]
        first_group = groups[0]
        last_idx = last_group[-1]
        first_idx = first_group[0]
        # Seam connection: last segment's end == first segment's start (in originals)
        # AND neither endpoint was clipped at the seam.
        if last_idx == n - 1 and first_idx == 0:
            last_seg = clipped[last_idx]
            first_seg = clipped[first_idx]
            orig_last = originals[last_idx]
            orig_first = originals[first_idx]
            assert last_seg is not None and first_seg is not None
            last_end_unclipped = _approx_equal(last_seg.end, orig_last.end)
            first_start_unclipped = _approx_equal(first_seg.start, orig_first.start)
            if last_end_unclipped and first_start_unclipped:
                merged = last_group + first_group
                groups = [merged] + groups[1:-1]

    # Convert each group to a polyline of Points.
    polylines: list[tuple[Point, ...]] = []
    for group in groups:
        pts: list[Point] = []
        for j, idx in enumerate(group):
            seg = clipped[idx]
            assert seg is not None
            if j == 0:
                pts.append(seg.start)
            else:
                # Check if the join between previous and this segment is seamless.
                prev_seg = clipped[group[j - 1]]
                assert prev_seg is not None
                orig_prev = originals[group[j - 1]]
                orig_curr = originals[idx]
                prev_end_unclipped = _approx_equal(prev_seg.end, orig_prev.end)
                curr_start_unclipped = _approx_equal(seg.start, orig_curr.start)
                if prev_end_unclipped and curr_start_unclipped:
                    # Seamless join - continue the polyline
                    pts.append(seg.start)
                else:
                    # Clipped boundary - split into a new polyline
                    polylines.append(tuple(pts))
                    pts = [seg.start]
            pts.append(seg.end)
        if pts:
            polylines.append(tuple(pts))

    return tuple(polylines)


def _count_arcs(polylines: tuple[tuple[Point, ...], ...]) -> int:
    return len(polylines)


def _approx_equal(a: Point, b: Point, eps: float = 1e-6) -> bool:
    return abs(a.x - b.x) < eps and abs(a.y - b.y) < eps
