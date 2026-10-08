"""Tests for shape types and to_segments()."""

from __future__ import annotations

import pytest

from app.geometry import Point, Rect
from app.shapes import Box, Circle, Line, _circle_segments


class TestLine:
    def test_to_segments_count(self):
        line = Line(Point(0, 0), Point(100, 100))
        assert len(line.to_segments()) == 1

    def test_to_segments_content(self):
        line = Line(Point(10, 20), Point(30, 40))
        segs = line.to_segments()
        assert segs[0].start == Point(10, 20)
        assert segs[0].end == Point(30, 40)

    def test_is_closed(self):
        assert Line(Point(0, 0), Point(1, 1)).is_closed() is False


class TestBox:
    def test_to_segments_count(self):
        box = Box(Rect(0, 0, 100, 50))
        assert len(box.to_segments()) == 4

    def test_to_segments_forms_closed_loop(self):
        box = Box(Rect(0, 0, 100, 50))
        segs = box.to_segments()
        for i in range(len(segs)):
            assert segs[i].end == segs[(i + 1) % 4].start, (
                f"Segment {i} end doesn't connect to segment {(i + 1) % 4} start"
            )

    def test_is_closed(self):
        assert Box(Rect(0, 0, 10, 10)).is_closed() is True


class TestCircle:
    def test_to_segments_count_small(self):
        c = Circle(Point(50, 50), 10.0)
        n = _circle_segments(10.0)
        assert len(c.to_segments()) == n

    def test_to_segments_count_min(self):
        """Very small radius → minimum 24 segments."""
        c = Circle(Point(50, 50), 1.0)
        assert len(c.to_segments()) == 24

    def test_to_segments_count_max(self):
        """Very large radius → capped at 360 segments."""
        c = Circle(Point(50, 50), 1000.0)
        assert len(c.to_segments()) == 360

    def test_to_segments_forms_closed_loop(self):
        c = Circle(Point(50, 50), 30.0)
        segs = c.to_segments()
        n = len(segs)
        for i in range(n):
            assert abs(segs[i].end.x - segs[(i + 1) % n].start.x) < 1e-9
            assert abs(segs[i].end.y - segs[(i + 1) % n].start.y) < 1e-9

    def test_is_closed(self):
        assert Circle(Point(0, 0), 5.0).is_closed() is True


class TestCircleAdaptiveSegments:
    @pytest.mark.parametrize(
        "r,expected_min,expected_max",
        [
            (0.1, 24, 24),  # tiny → 24
            (10.0, 15, 24),  # small-ish, should hit 24 floor
            (100.0, 100, 200),  # medium
            (5000.0, 360, 360),  # huge → 360
        ],
    )
    def test_clamp(self, r, expected_min, expected_max):
        n = _circle_segments(r)
        assert expected_min <= n <= expected_max
