"""Primitive geometry types used throughout the app.

Canvas coordinates: x grows rightward, y grows downward.
All types are frozen dataclasses with __slots__ for cheap snapshot storage.
"""

from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Point:
    x: float
    y: float

    def __add__(self, other: Point) -> Point:
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Point) -> Point:
        return Point(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar: float) -> Point:
        return Point(self.x * scalar, self.y * scalar)

    def dot(self, other: Point) -> float:
        return self.x * other.x + self.y * other.y

    def length(self) -> float:
        return math.hypot(self.x, self.y)

    def as_int(self) -> tuple[int, int]:
        return (round(self.x), round(self.y))


@dataclass(frozen=True, slots=True)
class Segment:
    """A finite directed line segment from start to end."""

    start: Point
    end: Point

    def length(self) -> float:
        return (self.end - self.start).length()

    def direction(self) -> Point:
        """Unit vector from start to end (undefined for zero-length segment)."""
        d = self.end - self.start
        mag = d.length()
        if mag == 0.0:
            return Point(0.0, 0.0)
        return Point(d.x / mag, d.y / mag)


@dataclass(frozen=True, slots=True)
class Rect:
    """Axis-aligned rectangle in canvas coordinates.

    xmin <= xmax, ymin <= ymax always holds (enforced by from_points).
    """

    xmin: float
    ymin: float
    xmax: float
    ymax: float

    @staticmethod
    def from_points(p0: Point, p1: Point) -> Rect:
        """Create a Rect from any two corner points (order does not matter)."""
        return Rect(
            xmin=min(p0.x, p1.x),
            ymin=min(p0.y, p1.y),
            xmax=max(p0.x, p1.x),
            ymax=max(p0.y, p1.y),
        )

    @property
    def width(self) -> float:
        return self.xmax - self.xmin

    @property
    def height(self) -> float:
        return self.ymax - self.ymin

    @property
    def center(self) -> Point:
        return Point((self.xmin + self.xmax) / 2.0, (self.ymin + self.ymax) / 2.0)

    def corners(self) -> tuple[Point, Point, Point, Point]:
        """Top-left, top-right, bottom-right, bottom-left (canvas coords)."""
        return (
            Point(self.xmin, self.ymin),
            Point(self.xmax, self.ymin),
            Point(self.xmax, self.ymax),
            Point(self.xmin, self.ymax),
        )
