"""Entry point — works with both `uv run main.py` and `python main.py`."""

from __future__ import annotations

import sys
import tkinter as tk

# Windows high-DPI awareness — must be called BEFORE tk.Tk()
if sys.platform == "win32":
    try:
        import ctypes

        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except OSError:
        pass  # not available on older Windows, safe to ignore


def main() -> None:
    from app.ui.main_window import MainWindow

    root = tk.Tk()
    _app = MainWindow(root)
    root.mainloop()


if __name__ == "__main__":
    main()
