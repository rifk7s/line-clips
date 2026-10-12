"""Tests for Scene state - undo, redo, clear."""

from __future__ import annotations

from app.geometry import Point, Rect
from app.scene import Scene
from app.shapes import Line


def _line(x1=0, y1=0, x2=10, y2=10):
    return Line(Point(x1, y1), Point(x2, y2))


class TestSceneUndo:
    def test_undo_reverts_last_drag(self):
        scene = Scene()
        scene.add_shapes([_line(0, 0, 10, 10)])
        scene.add_shapes([_line(20, 20, 30, 30)])
        assert len(scene.shapes) == 2
        scene.undo()
        assert len(scene.shapes) == 1

    def test_undo_multi_shape_drag(self):
        """One drag may produce multiple shapes - one undo reverts all of them."""
        scene = Scene()
        scene.add_shapes([_line(0, 0, 10, 10), _line(5, 5, 15, 15)])
        scene.undo()
        assert len(scene.shapes) == 0

    def test_undo_empty_does_nothing(self):
        scene = Scene()
        assert scene.undo() is False
        assert len(scene.shapes) == 0

    def test_undo_window_replacement(self):
        scene = Scene()
        w1 = Rect(0, 0, 100, 100)
        w2 = Rect(50, 50, 150, 150)
        scene.set_window(w1)
        scene.set_window(w2)
        scene.undo()
        assert scene.clip_window == w1


class TestSceneRedo:
    def test_redo_reapplies_after_undo(self):
        scene = Scene()
        scene.add_shapes([_line()])
        scene.undo()
        assert len(scene.shapes) == 0
        scene.redo()
        assert len(scene.shapes) == 1

    def test_new_action_clears_redo(self):
        scene = Scene()
        scene.add_shapes([_line()])
        scene.undo()
        scene.add_shapes([_line(1, 1, 2, 2)])  # new action
        assert scene.can_redo() is False

    def test_redo_empty_does_nothing(self):
        scene = Scene()
        assert scene.redo() is False


class TestSceneClear:
    def test_clear_resets_scene(self):
        scene = Scene()
        scene.add_shapes([_line()])
        scene.set_window(Rect(0, 0, 100, 100))
        scene.clear()
        assert len(scene.shapes) == 0
        assert scene.clip_window is None

    def test_clear_pushes_undo(self):
        scene = Scene()
        scene.add_shapes([_line()])
        scene.clear()
        scene.undo()
        assert len(scene.shapes) == 1

    def test_clear_empty_does_not_push(self):
        scene = Scene()
        scene.clear()  # already empty
        assert scene.can_undo() is False

    def test_clear_clears_redo(self):
        scene = Scene()
        scene.add_shapes([_line()])
        scene.undo()
        scene.add_shapes([_line()])  # clears redo
        assert scene.can_redo() is False


class TestSceneWindowReplacement:
    def test_window_is_replaced(self):
        scene = Scene()
        w1 = Rect(0, 0, 100, 100)
        w2 = Rect(10, 10, 200, 200)
        scene.set_window(w1)
        scene.set_window(w2)
        assert scene.clip_window == w2


class TestSceneApplyDrag:
    def test_shapes_and_window_are_one_undo_step(self):
        scene = Scene()
        scene.apply_drag([_line()], Rect(0, 0, 100, 100))
        scene.undo()
        assert scene.shapes == ()
        assert scene.clip_window is None
        assert scene.can_undo() is False

    def test_empty_drag_does_not_push(self):
        scene = Scene()
        scene.apply_drag([], None)
        assert scene.can_undo() is False
