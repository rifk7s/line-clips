"""Shape types: Line, Box, Circle.

Each shape stores its drawing attributes (color, width) and exposes
to_segments() which returns the list of Segments that clip_shape() will process.
All shapes are frozen dataclasses for cheap snapshot storage in scene.py.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Protocol

from app.geometry import Point, Rect, Segment

# Shape protocol (structural typing - no ABC needed)


class Shape(Protocol):
    color: str
    width: int

    def to_segments(self) -> list[Segment]: ...
    def is_closed(self) -> bool: ...
    def label(self) -> str: ...
    def before_label(self) -> str: ...


# Color palette (Indonesian names → hex)

COLOR_MAP: dict[str, str] = {
    "Hitam": "#000000",
    "Merah": "#E53935",
    "Hijau": "#43A047",
    "Ungu": "#8E24AA",
    "Cokelat": "#6D4C41",
}

COLOR_NAMES = list(COLOR_MAP.keys())

# Reserved UI colors (NOT in the dropdown)
COLOR_WINDOW = "#2196F3"  # clipping window outline (blue)
COLOR_GHOST = "#AAAAAA"  # unclipped shape when window exists (gray)
COLOR_HALO = "#FF9800"  # selected shape halo (orange)


# Thickness options

THICKNESS_OPTIONS: list[int] = [1, 2, 3, 4, 5]


# Adaptive circle segment count


def _circle_segments(r: float) -> int:
    """Adaptive segment count: clamp(int(2π·r / 4), 24, 360)."""
    return max(24, min(360, int(2 * math.pi * r / 4)))


# Concrete shape types


@dataclass(frozen=True, slots=True)
class Line:
    """A directed line segment (called 'Garis' in the UI)."""

    start: Point
    end: Point
    color: str = "Hitam"
    width: int = 2

    def to_segments(self) -> list[Segment]:
        return [Segment(self.start, self.end)]

    def is_closed(self) -> bool:
        return False

    def label(self) -> str:
        s = self.start.as_int()
        e = self.end.as_int()
        return f"Garis      ({s[0]},{s[1]})→({e[0]},{e[1]})"

    def before_label(self) -> str:
        return self.label()


@dataclass(frozen=True, slots=True)
class Box:
    """An axis-aligned rectangle (called 'Kotak' in the UI)."""

    rect: Rect
    color: str = "Hitam"
    width: int = 2

    def to_segments(self) -> list[Segment]:
        tl, tr, br, bl = self.rect.corners()
        # Four sides in order: top, right, bottom, left
        return [
            Segment(tl, tr),  # top
            Segment(tr, br),  # right
            Segment(br, bl),  # bottom
            Segment(bl, tl),  # left
        ]

    def is_closed(self) -> bool:
        return True

    def label(self) -> str:
        tl = Point(self.rect.xmin, self.rect.ymin).as_int()
        br = Point(self.rect.xmax, self.rect.ymax).as_int()
        return f"Kotak      ({tl[0]},{tl[1]})→({br[0]},{br[1]})"

    def before_label(self) -> str:
        return self.label()


@dataclass(frozen=True, slots=True)
class Circle:
    """A circle approximated as N line segments (called 'Lingkaran' in the UI)."""

    center: Point
    radius: float
    color: str = "Hitam"
    width: int = 2

    def to_segments(self) -> list[Segment]:
        n = _circle_segments(self.radius)
        pts = [
            Point(
                self.center.x + self.radius * math.cos(2 * math.pi * i / n),
                self.center.y + self.radius * math.sin(2 * math.pi * i / n),
            )
            for i in range(n)
        ]
        # Closed polygon: last point back to first
        return [Segment(pts[i], pts[(i + 1) % n]) for i in range(n)]

    def is_closed(self) -> bool:
        return True

    def label(self) -> str:
        c = self.center.as_int()
        r = round(self.radius)
        return f"Lingkaran  pusat ({c[0]},{c[1]})  r={r}"

    def before_label(self) -> str:
        return self.label()


# Union type for scene storage
AnyShape = Line | Box | Circle
