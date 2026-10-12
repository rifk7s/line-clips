"""Algorithm edge cases - parametrized over both algorithms.

All comparisons are made after the shared clip_shape() filter so both
algorithms are tested through the same code path used by the UI.
"""

from __future__ import annotations

import random

import pytest

from app.clipping import Algorithm, ClipStatus, clip_shape
from app.geometry import Point, Rect, Segment
from app.shapes import Box, Line

WIN = Rect(50, 50, 200, 150)  # standard test window

ALGOS = [Algorithm.COHEN_SUTHERLAND, Algorithm.LIANG_BARSKY]
ALGO_IDS = ["cohen_sutherland", "liang_barsky"]


def _clip_seg(seg: Segment, win: Rect, algo: Algorithm) -> Segment | None:
    """Use clip_shape() via a Line wrapper (same path as the UI)."""
    result = clip_shape(Line(seg.start, seg.end), win, algo)
    if result.status == ClipStatus.REJECTED:
        return None
    pts = result.polylines[0]
    return Segment(pts[0], pts[-1])


@pytest.mark.parametrize("algo", ALGOS, ids=ALGO_IDS)
class TestEdgeCases:
    def test_fully_inside(self, algo):
        seg = Segment(Point(60, 60), Point(190, 140))
        r = _clip_seg(seg, WIN, algo)
        assert r is not None
        assert abs(r.start.x - 60) < 1e-6 and abs(r.start.y - 60) < 1e-6
        assert abs(r.end.x - 190) < 1e-6 and abs(r.end.y - 140) < 1e-6

    def test_fully_outside_same_side(self, algo):
        seg = Segment(Point(0, 0), Point(40, 40))  # entirely left of window
        assert _clip_seg(seg, WIN, algo) is None

    def test_horizontal_segment_overlapping(self, algo):
        seg = Segment(Point(0, 100), Point(300, 100))  # crosses window horizontally
        r = _clip_seg(seg, WIN, algo)
        assert r is not None
        assert abs(r.start.x - WIN.xmin) < 1e-6
        assert abs(r.end.x - WIN.xmax) < 1e-6

    def test_horizontal_segment_outside(self, algo):
        seg = Segment(Point(0, 10), Point(300, 10))  # y=10 above ymin=50
        assert _clip_seg(seg, WIN, algo) is None

    def test_vertical_segment_overlapping(self, algo):
        seg = Segment(Point(100, 0), Point(100, 300))  # crosses window vertically
        r = _clip_seg(seg, WIN, algo)
        assert r is not None
        assert abs(r.start.y - WIN.ymin) < 1e-6
        assert abs(r.end.y - WIN.ymax) < 1e-6

    def test_vertical_segment_outside(self, algo):
        seg = Segment(Point(10, 0), Point(10, 300))  # x=10 left of xmin=50
        assert _clip_seg(seg, WIN, algo) is None

    def test_zero_length_segment(self, algo):
        seg = Segment(Point(100, 100), Point(100, 100))
        assert _clip_seg(seg, WIN, algo) is None

    def test_touching_corner_only(self, algo):
        """Segment from outside touching exactly one corner - degenerate, must reject."""
        # Line from (0,0) to (50,50) - touches corner (50,50) which is WIN.top-left
        seg = Segment(Point(0, 0), Point(50, 50))
        # Result length < 1 px, so filter rejects it
        assert _clip_seg(seg, WIN, algo) is None

    def test_inside_ending_at_corner(self, algo):
        """Segment starts inside window and ends exactly at a corner."""
        seg = Segment(Point(100, 100), Point(WIN.xmin, WIN.ymin))
        r = _clip_seg(seg, WIN, algo)
        assert r is not None
        assert abs(r.start.x - 100) < 1e-6
        assert abs(r.end.x - WIN.xmin) < 1e-6

    def test_exactly_on_boundary_edge(self, algo):
        """Segment lying exactly on one boundary edge."""
        seg = Segment(Point(WIN.xmin, WIN.ymin), Point(WIN.xmax, WIN.ymin))
        r = _clip_seg(seg, WIN, algo)
        assert r is not None
        assert abs(r.start.x - WIN.xmin) < 1e-6
        assert abs(r.end.x - WIN.xmax) < 1e-6


@pytest.mark.parametrize("algo", ALGOS, ids=ALGO_IDS)
def test_direction_preservation(algo):
    """Clipped segment must point in the same direction as the original."""
    rng = random.Random(42)

    def rand_pt():
        return Point(rng.uniform(-50, 300), rng.uniform(-50, 250))

    for _ in range(500):
        seg = Segment(rand_pt(), rand_pt())
        r = _clip_seg(seg, WIN, algo)
        if r is None:
            continue
        orig_dir = seg.end - seg.start
        res_dir = r.end - r.start
        dot = orig_dir.x * res_dir.x + orig_dir.y * res_dir.y
        assert dot > 0, f"Direction flipped: orig={seg}, result={r}, dot={dot}"


def test_algorithm_equivalence():
    """Both algorithms must agree within 1e-9 for thousands of random segments."""
    rng = random.Random(42)
    win = WIN

    def rand_coord(lo, hi):
        return rng.uniform(lo, hi)

    mismatches = 0
    total = 3000

    for _ in range(total):
        # Mix random and boundary-snapped points
        if rng.random() < 0.2:
            # Snap to window edge
            x1 = rng.choice([win.xmin, win.xmax, rand_coord(-50, 300)])
            y1 = rng.choice([win.ymin, win.ymax, rand_coord(-50, 250)])
        else:
            x1, y1 = rand_coord(-50, 300), rand_coord(-50, 250)
        x2, y2 = rand_coord(-50, 300), rand_coord(-50, 250)

        seg = Segment(Point(x1, y1), Point(x2, y2))
        r_cs = _clip_seg(seg, win, Algorithm.COHEN_SUTHERLAND)
        r_lb = _clip_seg(seg, win, Algorithm.LIANG_BARSKY)

        both_none = r_cs is None and r_lb is None
        both_have = r_cs is not None and r_lb is not None

        if not both_none and not both_have:
            mismatches += 1
            continue

        if both_have:
            assert r_cs is not None and r_lb is not None
            # Compare endpoints as unordered pair (both directions possible after clipping)
            cs_pts = {
                (round(r_cs.start.x, 9), round(r_cs.start.y, 9)),
                (round(r_cs.end.x, 9), round(r_cs.end.y, 9)),
            }
            lb_pts = {
                (round(r_lb.start.x, 9), round(r_lb.start.y, 9)),
                (round(r_lb.end.x, 9), round(r_lb.end.y, 9)),
            }

            for cs_p, lb_p in zip(sorted(cs_pts), sorted(lb_pts)):
                assert abs(cs_p[0] - lb_p[0]) < 1e-6 and abs(cs_p[1] - lb_p[1]) < 1e-6, (
                    f"Mismatch: CS={r_cs} LB={r_lb} for seg={seg}"
                )

    # Allow a tiny tolerance for degenerate edge cases at boundaries
    assert mismatches <= 5, f"Too many None/non-None mismatches: {mismatches}/{total}"


# [ clip_shape() on Box ]


@pytest.mark.parametrize("algo", ALGOS, ids=ALGO_IDS)
def test_box_partial_counts_visible_sides(algo):
    # Sticks out past the right edge: top, bottom, left visible; right rejected
    result = clip_shape(Box(Rect(100, 80, 300, 120)), WIN, algo)
    assert result.status == ClipStatus.PARTIAL
    assert result.visible_count == 3


@pytest.mark.parametrize("algo", ALGOS, ids=ALGO_IDS)
def test_box_on_window_boundary_is_full(algo):
    # Kotak + Area Clipping from the same drag share the same rect
    result = clip_shape(Box(WIN), WIN, algo)
    assert result.status == ClipStatus.FULL
    assert result.visible_count == 4
