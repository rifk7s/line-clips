"""Tests for geometry primitives."""

from __future__ import annotations

from app.geometry import Point, Rect, Segment


class TestPoint:
    def test_add(self):
        assert Point(1, 2) + Point(3, 4) == Point(4, 6)

    def test_sub(self):
        assert Point(5, 3) - Point(2, 1) == Point(3, 2)

    def test_length(self):
        assert abs(Point(3, 4).length() - 5.0) < 1e-9

    def test_as_int(self):
        assert Point(1.6, 2.4).as_int() == (2, 2)


class TestSegment:
    def test_length(self):
        s = Segment(Point(0, 0), Point(3, 4))
        assert abs(s.length() - 5.0) < 1e-9

    def test_zero_length(self):
        s = Segment(Point(2, 2), Point(2, 2))
        assert s.length() == 0.0


class TestRect:
    def test_from_points_normal(self):
        r = Rect.from_points(Point(10, 20), Point(100, 200))
        assert r.xmin == 10 and r.ymin == 20
        assert r.xmax == 100 and r.ymax == 200

    def test_from_points_reversed(self):
        """Right-to-left, bottom-to-top drag must still produce valid rect."""
        r = Rect.from_points(Point(100, 200), Point(10, 20))
        assert r.xmin == 10 and r.ymin == 20
        assert r.xmax == 100 and r.ymax == 200

    def test_from_points_all_quadrant_orderings(self):
        corners = [
            (Point(0, 0), Point(50, 50)),
            (Point(50, 0), Point(0, 50)),
            (Point(0, 50), Point(50, 0)),
            (Point(50, 50), Point(0, 0)),
        ]
        for p0, p1 in corners:
            r = Rect.from_points(p0, p1)
            assert r.xmin == 0 and r.xmax == 50
            assert r.ymin == 0 and r.ymax == 50

    def test_width_height(self):
        r = Rect(10, 20, 110, 70)
        assert r.width == 100
        assert r.height == 50

    def test_center(self):
        r = Rect(0, 0, 100, 50)
        assert r.center == Point(50, 25)
