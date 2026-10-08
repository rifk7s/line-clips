<div align="center">

<h1>Line Clipping App</h1>

<br/>

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=flat&logo=data:image/svg%2Bxml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAxMjggMTI4Ij48bGluZWFyR3JhZGllbnQgaWQ9InB5dGhvbi1vcmlnaW5hbC1hIiBncmFkaWVudFVuaXRzPSJ1c2VyU3BhY2VPblVzZSIgeDE9IjcwLjI1MiIgeTE9IjEyMzcuNDc2IiB4Mj0iMTcwLjY1OSIgeTI9IjExNTEuMDg5IiBncmFkaWVudFRyYW5zZm9ybT0ibWF0cml4KC41NjMgMCAwIC0uNTY4IC0yOS4yMTUgNzA3LjgxNykiPjxzdG9wIG9mZnNldD0iMCIgc3RvcC1jb2xvcj0iIzVBOUZENCIvPjxzdG9wIG9mZnNldD0iMSIgc3RvcC1jb2xvcj0iIzMwNjk5OCIvPjwvbGluZWFyR3JhZGllbnQ+PGxpbmVhckdyYWRpZW50IGlkPSJweXRob24tb3JpZ2luYWwtYiIgZ3JhZGllbnRVbml0cz0idXNlclNwYWNlT25Vc2UiIHgxPSIyMDkuNDc0IiB5MT0iMTA5OC44MTEiIHgyPSIxNzMuNjIiIHkyPSIxMTQ5LjUzNyIgZ3JhZGllbnRUcmFuc2Zvcm09Im1hdHJpeCguNTYzIDAgMCAtLjU2OCAtMjkuMjE1IDcwNy44MTcpIj48c3RvcCBvZmZzZXQ9IjAiIHN0b3AtY29sb3I9IiNGRkQ0M0IiLz48c3RvcCBvZmZzZXQ9IjEiIHN0b3AtY29sb3I9IiNGRkU4NzMiLz48L2xpbmVhckdyYWRpZW50PjxwYXRoIGZpbGw9InVybCgjcHl0aG9uLW9yaWdpbmFsLWEpIiBkPSJNNjMuMzkxIDEuOTg4Yy00LjIyMi4wMi04LjI1Mi4zNzktMTEuOCAxLjAwNy0xMC40NSAxLjg0Ni0xMi4zNDYgNS43MS0xMi4zNDYgMTIuODM3djkuNDExaDI0LjY5M3YzLjEzN0gyOS45NzdjLTcuMTc2IDAtMTMuNDYgNC4zMTMtMTUuNDI2IDEyLjUyMS0yLjI2OCA5LjQwNS0yLjM2OCAxNS4yNzUgMCAyNS4wOTYgMS43NTUgNy4zMTEgNS45NDcgMTIuNTE5IDEzLjEyNCAxMi41MTloOC40OTFWNjcuMjM0YzAtOC4xNTEgNy4wNTEtMTUuMzQgMTUuNDI2LTE1LjM0aDI0LjY2NWM2Ljg2NiAwIDEyLjM0Ni01LjY1NCAxMi4zNDYtMTIuNTQ4VjE1LjgzM2MwLTYuNjkzLTUuNjQ2LTExLjcyLTEyLjM0Ni0xMi44MzctNC4yNDQtLjcwNi04LjY0NS0xLjAyNy0xMi44NjYtMS4wMDh6TTUwLjAzNyA5LjU1N2MyLjU1IDAgNC42MzQgMi4xMTcgNC42MzQgNC43MjEgMCAyLjU5My0yLjA4MyA0LjY5LTQuNjM0IDQuNjktMi41NiAwLTQuNjMzLTIuMDk3LTQuNjMzLTQuNjktLjAwMS0yLjYwNCAyLjA3My00LjcyMSA0LjYzMy00LjcyMXoiIHRyYW5zZm9ybT0idHJhbnNsYXRlKDAgMTAuMjYpIi8+PHBhdGggZmlsbD0idXJsKCNweXRob24tb3JpZ2luYWwtYikiIGQ9Ik05MS42ODIgMjguMzh2MTAuOTY2YzAgOC41LTcuMjA4IDE1LjY1NS0xNS40MjYgMTUuNjU1SDUxLjU5MWMtNi43NTYgMC0xMi4zNDYgNS43ODMtMTIuMzQ2IDEyLjU0OXYyMy41MTVjMCA2LjY5MSA1LjgxOCAxMC42MjggMTIuMzQ2IDEyLjU0NyA3LjgxNiAyLjI5NyAxNS4zMTIgMi43MTMgMjQuNjY1IDAgNi4yMTYtMS44MDEgMTIuMzQ2LTUuNDIzIDEyLjM0Ni0xMi41NDd2LTkuNDEySDYzLjkzOHYtMy4xMzhoMzcuMDEyYzcuMTc2IDAgOS44NTItNS4wMDUgMTIuMzQ4LTEyLjUxOSAyLjU3OC03LjczNSAyLjQ2Ny0xNS4xNzQgMC0yNS4wOTYtMS43NzQtNy4xNDUtNS4xNjEtMTIuNTIxLTEyLjM0OC0xMi41MjFoLTkuMjY4ek03Ny44MDkgODcuOTI3YzIuNTYxIDAgNC42MzQgMi4wOTcgNC42MzQgNC42OTIgMCAyLjYwMi0yLjA3NCA0LjcxOS00LjYzNCA0LjcxOS0yLjU1IDAtNC42MzMtMi4xMTctNC42MzMtNC43MTkgMC0yLjU5NSAyLjA4My00LjY5MiA0LjYzMy00LjY5MnoiIHRyYW5zZm9ybT0idHJhbnNsYXRlKDAgMTAuMjYpIi8+PHJhZGlhbEdyYWRpZW50IGlkPSJweXRob24tb3JpZ2luYWwtYyIgY3g9IjE4MjUuNjc4IiBjeT0iNDQ0LjQ1IiByPSIyNi43NDMiIGdyYWRpZW50VHJhbnNmb3JtPSJtYXRyaXgoMCAtLjI0IC0xLjA1NSAwIDUzMi45NzkgNTU3LjU3NikiIGdyYWRpZW50VW5pdHM9InVzZXJTcGFjZU9uVXNlIj48c3RvcCBvZmZzZXQ9IjAiIHN0b3AtY29sb3I9IiNCOEI4QjgiIHN0b3Atb3BhY2l0eT0iLjQ5OCIvPjxzdG9wIG9mZnNldD0iMSIgc3RvcC1jb2xvcj0iIzdGN0Y3RiIgc3RvcC1vcGFjaXR5PSIwIi8+PC9yYWRpYWxHcmFkaWVudD48cGF0aCBvcGFjaXR5PSIuNDQ0IiBmaWxsPSJ1cmwoI3B5dGhvbi1vcmlnaW5hbC1jKSIgZD0iTTk3LjMwOSAxMTkuNTk3YzAgMy41NDMtMTQuODE2IDYuNDE2LTMzLjA5MSA2LjQxNi0xOC4yNzYgMC0zMy4wOTItMi44NzMtMzMuMDkyLTYuNDE2IDAtMy41NDQgMTQuODE1LTYuNDE3IDMzLjA5Mi02LjQxNyAxOC4yNzUgMCAzMy4wOTEgMi44NzIgMzMuMDkxIDYuNDE3eiIvPjwvc3ZnPgo=)](https://www.python.org/)
[![UI](https://img.shields.io/badge/UI-Tkinter-green?style=flat&logo=data:image/svg%2Bxml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAxMjggMTI4Ij48bGluZWFyR3JhZGllbnQgaWQ9InB5dGhvbi1vcmlnaW5hbC1hIiBncmFkaWVudFVuaXRzPSJ1c2VyU3BhY2VPblVzZSIgeDE9IjcwLjI1MiIgeTE9IjEyMzcuNDc2IiB4Mj0iMTcwLjY1OSIgeTI9IjExNTEuMDg5IiBncmFkaWVudFRyYW5zZm9ybT0ibWF0cml4KC41NjMgMCAwIC0uNTY4IC0yOS4yMTUgNzA3LjgxNykiPjxzdG9wIG9mZnNldD0iMCIgc3RvcC1jb2xvcj0iIzVBOUZENCIvPjxzdG9wIG9mZnNldD0iMSIgc3RvcC1jb2xvcj0iIzMwNjk5OCIvPjwvbGluZWFyR3JhZGllbnQ+PGxpbmVhckdyYWRpZW50IGlkPSJweXRob24tb3JpZ2luYWwtYiIgZ3JhZGllbnRVbml0cz0idXNlclNwYWNlT25Vc2UiIHgxPSIyMDkuNDc0IiB5MT0iMTA5OC44MTEiIHgyPSIxNzMuNjIiIHkyPSIxMTQ5LjUzNyIgZ3JhZGllbnRUcmFuc2Zvcm09Im1hdHJpeCguNTYzIDAgMCAtLjU2OCAtMjkuMjE1IDcwNy44MTcpIj48c3RvcCBvZmZzZXQ9IjAiIHN0b3AtY29sb3I9IiNGRkQ0M0IiLz48c3RvcCBvZmZzZXQ9IjEiIHN0b3AtY29sb3I9IiNGRkU4NzMiLz48L2xpbmVhckdyYWRpZW50PjxwYXRoIGZpbGw9InVybCgjcHl0aG9uLW9yaWdpbmFsLWEpIiBkPSJNNjMuMzkxIDEuOTg4Yy00LjIyMi4wMi04LjI1Mi4zNzktMTEuOCAxLjAwNy0xMC40NSAxLjg0Ni0xMi4zNDYgNS43MS0xMi4zNDYgMTIuODM3djkuNDExaDI0LjY5M3YzLjEzN0gyOS45NzdjLTcuMTc2IDAtMTMuNDYgNC4zMTMtMTUuNDI2IDEyLjUyMS0yLjI2OCA5LjQwNS0yLjM2OCAxNS4yNzUgMCAyNS4wOTYgMS43NTUgNy4zMTEgNS45NDcgMTIuNTE5IDEzLjEyNCAxMi41MTloOC40OTFWNjcuMjM0YzAtOC4xNTEgNy4wNTEtMTUuMzQgMTUuNDI2LTE1LjM0aDI0LjY2NWM2Ljg2NiAwIDEyLjM0Ni01LjY1NCAxMi4zNDYtMTIuNTQ4VjE1LjgzM2MwLTYuNjkzLTUuNjQ2LTExLjcyLTEyLjM0Ni0xMi44MzctNC4yNDQtLjcwNi04LjY0NS0xLjAyNy0xMi44NjYtMS4wMDh6TTUwLjAzNyA5LjU1N2MyLjU1IDAgNC42MzQgMi4xMTcgNC42MzQgNC43MjEgMCAyLjU5My0yLjA4MyA0LjY5LTQuNjM0IDQuNjktMi41NiAwLTQuNjMzLTIuMDk3LTQuNjMzLTQuNjktLjAwMS0yLjYwNCAyLjA3My00LjcyMSA0LjYzMy00LjcyMXoiIHRyYW5zZm9ybT0idHJhbnNsYXRlKDAgMTAuMjYpIi8+PHBhdGggZmlsbD0idXJsKCNweXRob24tb3JpZ2luYWwtYikiIGQ9Ik05MS42ODIgMjguMzh2MTAuOTY2YzAgOC41LTcuMjA4IDE1LjY1NS0xNS40MjYgMTUuNjU1SDUxLjU5MWMtNi43NTYgMC0xMi4zNDYgNS43ODMtMTIuMzQ2IDEyLjU0OXYyMy41MTVjMCA2LjY5MSA1LjgxOCAxMC42MjggMTIuMzQ2IDEyLjU0NyA3LjgxNiAyLjI5NyAxNS4zMTIgMi43MTMgMjQuNjY1IDAgNi4yMTYtMS44MDEgMTIuMzQ2LTUuNDIzIDEyLjM0Ni0xMi41NDd2LTkuNDEySDYzLjkzOHYtMy4xMzhoMzcuMDEyYzcuMTc2IDAgOS44NTItNS4wMDUgMTIuMzQ4LTEyLjUxOSAyLjU3OC03LjczNSAyLjQ2Ny0xNS4xNzQgMC0yNS4wOTYtMS43NzQtNy4xNDUtNS4xNjEtMTIuNTIxLTEyLjM0OC0xMi41MjFoLTkuMjY4ek03Ny44MDkgODcuOTI3YzIuNTYxIDAgNC42MzQgMi4wOTcgNC42MzQgNC42OTIgMCAyLjYwMi0yLjA3NCA0LjcxOS00LjYzNCA0LjcxOS0yLjU1IDAtNC42MzMtMi4xMTctNC42MzMtNC43MTkgMC0yLjU5NSAyLjA4My00LjY5MiA0LjYzMy00LjY5MnoiIHRyYW5zZm9ybT0idHJhbnNsYXRlKDAgMTAuMjYpIi8+PHJhZGlhbEdyYWRpZW50IGlkPSJweXRob24tb3JpZ2luYWwtYyIgY3g9IjE4MjUuNjc4IiBjeT0iNDQ0LjQ1IiByPSIyNi43NDMiIGdyYWRpZW50VHJhbnNmb3JtPSJtYXRyaXgoMCAtLjI0IC0xLjA1NSAwIDUzMi45NzkgNTU3LjU3NikiIGdyYWRpZW50VW5pdHM9InVzZXJTcGFjZU9uVXNlIj48c3RvcCBvZmZzZXQ9IjAiIHN0b3AtY29sb3I9IiNCOEI4QjgiIHN0b3Atb3BhY2l0eT0iLjQ5OCIvPjxzdG9wIG9mZnNldD0iMSIgc3RvcC1jb2xvcj0iIzdGN0Y3RiIgc3RvcC1vcGFjaXR5PSIwIi8+PC9yYWRpYWxHcmFkaWVudD48cGF0aCBvcGFjaXR5PSIuNDQ0IiBmaWxsPSJ1cmwoI3B5dGhvbi1vcmlnaW5hbC1jKSIgZD0iTTk3LjMwOSAxMTkuNTk3YzAgMy41NDMtMTQuODE2IDYuNDE2LTMzLjA5MSA2LjQxNi0xOC4yNzYgMC0zMy4wOTItMi44NzMtMzMuMDkyLTYuNDE2IDAtMy41NDQgMTQuODE1LTYuNDE3IDMzLjA5Mi02LjQxNyAxOC4yNzUgMCAzMy4wOTEgMi44NzIgMzMuMDkxIDYuNDE3eiIvPjwvc3ZnPgo=)](https://docs.python.org/3/library/tkinter.html)
[![Tooling](https://img.shields.io/badge/Tooling-uv-purple?style=flat&logo=data:image/svg%2Bxml;base64,PHN2ZyB3aWR0aD0iNDEiIGhlaWdodD0iNDEiIHZpZXdCb3g9IjAgMCA0MSA0MSIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTS01LjI4NjE5ZS0wNiAwLjE2ODYyOUwwLjA4NDMwOTggMjAuMTY4NUwwLjE1MTc2MiAzNi4xNjgzQzAuMTYxMDc1IDM4LjM3NzQgMS45NTk0NyA0MC4xNjA3IDQuMTY4NTkgNDAuMTUxNEwyMC4xNjg0IDQwLjA4NEwzMC4xNjg0IDQwLjA0MThMMzEuMTg1MiA0MC4wMzc1QzMzLjM4NzcgNDAuMDI4MiAzNS4xNjgzIDM4LjIwMjYgMzUuMTY4MyAzNlYzNkwzNy4wMDAzIDM2TDM3LjAwMDMgMzkuOTk5Mkw0MC4xNjgzIDM5Ljk5OTZMMzkuOTk5NiAtOS45NDY1M2UtMDdMMjEuNTk5OCAwLjA3NzU2ODlMMjEuNjc3NCAxNi4wMTg1TDIxLjY3NzQgMjUuOTk5OEwyMC4wNzc0IDI1Ljk5OThMMTguMzk5OCAyNS45OTk4TDE4LjQ3NzQgMTYuMDMyTDE4LjM5OTggMC4wOTEwNTkzTC01LjI4NjE5ZS0wNiAwLjE2ODYyOVoiIGZpbGw9IiNERTVGRTkiLz4KPC9zdmc+Cg==)](https://github.com/astral-sh/uv)

<br/>

Computer Graphics assignment - draw lines, boxes, and circles on a canvas and clip them using **Cohen-Sutherland** or **Liang-Barsky** algorithms.

</div>

> [!NOTE]
> **No external packages needed.** The app uses only Python's standard library (Tkinter). `pytest` and `ruff` are dev-only tools used for testing and linting - they are **not** required to run the app. `uv` is recommended for development but plain Python works perfectly.

---

## Quick Start - Two Ways to Run

<table width="100%">
<tr>
<td width="50%" valign="top">

### Option A: With `uv` (Recommended)

`uv` is an extremely fast Python package and project manager. If you don't have it installed, [get it here](https://docs.astral.sh/uv/getting-started/installation/).

`uv` manages a virtual environment automatically.

```bash
# 1. Install dev tools (pytest & ruff)
uv sync --group dev

# 2. Run the app
uv run main.py
```

</td>
<td width="50%" valign="top">

### Option B: Plain Python

No `uv` needed. Great for testing on any machine.

```bash
# 1. Setup virtual environment
python -m venv .venv

# 2. Activate the environment
source .venv/bin/activate  # Mac/Linux
# .venv\Scripts\activate   # Windows

# 3. Run the application
python main.py
```

</td>
</tr>
</table>

---

## Dev Commands

The following commands require `uv` and the dev group installed (`uv sync --group dev`):

<table width="100%">
<thead>
<tr>
<th>Command</th>
<th>Description</th>
</tr>
</thead>
<tbody>
<tr><td><code>uv run pytest</code></td><td>Run all tests</td></tr>
<tr><td><code>uv run pytest -v</code></td><td>Run tests with verbose output</td></tr>
<tr><td><code>uv run ruff check .</code></td><td>Lint check (reports issues only)</td></tr>
<tr><td><code>uv run ruff check . --fix</code></td><td>Lint + auto-fix all fixable issues</td></tr>
<tr><td><code>uv run ruff format .</code></td><td>Format code automatically</td></tr>
</tbody>
</table>

---

## How to Use the App

<table width="100%">
<thead>
<tr>
<th>Action</th>
<th>How</th>
</tr>
</thead>
<tbody>
<tr><td><strong>Draw a line</strong></td><td>Check <strong>Garis</strong> in Buat panel, then click-and-drag on the canvas</td></tr>
<tr><td><strong>Define clipping window</strong></td><td>Check <strong>Area Clipping</strong>, then drag a rectangle</td></tr>
<tr><td><strong>Switch algorithm</strong></td><td>Click the <strong>Cohen-Sutherland</strong> or <strong>Liang-Barsky</strong> radio button</td></tr>
<tr><td><strong>Change color / thickness</strong></td><td>Use the <strong>Warna</strong> and <strong>Ketebalan</strong> dropdowns</td></tr>
<tr><td><strong>Undo</strong></td><td><code>Cmd+Z</code> (macOS) / <code>Ctrl+Z</code> (Windows)</td></tr>
<tr><td><strong>Redo</strong></td><td><code>Cmd+Shift+Z</code> (macOS) / <code>Ctrl+Y</code> (Windows)</td></tr>
<tr><td><strong>Clear all</strong></td><td>Edit &rarr; Hapus Semua</td></tr>
<tr><td><strong>Select a shape</strong></td><td>Click a row in either listbox - highlights it on the canvas</td></tr>
</tbody>
</table>

> [!TIP]
> **Multi-Select in "Buat" Panel:** Garis and Area Clipping can both be checked at the same time. Dragging will create a line *and* set the clipping window in one action. Uncheck Garis first if you only want to define the window. The status bar always shows which tools are currently active.

> [!IMPORTANT]
> **Automatic Clipping & History:** Clipping is **automatic** - no button needed. Results update instantly whenever you finish drawing, change the algorithm, undo, or redo. The app supports full **Undo/Redo** history for all shapes drawn and window modifications.

---

## Project Structure

```
line-clips/
├── main.py                  # Entry point - uv run main.py  OR  python main.py
├── pyproject.toml           # Project config + dev dependencies
├── .python-version          # Pins local Python to 3.12 (for uv)
├── uv.lock                  # Lockfile - committed, ensures reproducible installs
├── app/
│   ├── geometry.py          # Point, Segment, Rect - frozen dataclasses
│   ├── shapes.py            # Line, Box, Circle - attrs + to_segments()
│   ├── scene.py             # App state - shapes, clip window, undo/redo stacks
│   ├── clipping/
│   │   ├── __init__.py      # Algorithm enum, ClipResult, clip_shape() entry point
│   │   ├── cohen_sutherland.py
│   │   └── liang_barsky.py
│   └── ui/
│       ├── main_window.py   # Grid layout + thin controller
│       ├── canvas_view.py   # Mouse events, rubber-band preview, redraw()
│       ├── toolbar.py       # Buat / Algoritma / Atribut panels
│       └── panels.py        # Before/after listboxes + scrollbars
└── tests/
    ├── test_geometry.py
    ├── test_algorithms.py   # Edge cases + direction + equivalence (3000 random segs)
    ├── test_shapes.py
    └── test_scene.py
```

---

> [!NOTE]
> **Windows DPI Awareness:** The app automatically sets DPI awareness on Windows (via `ctypes`) before the window opens, so it won't appear blurry on high-DPI screens.
