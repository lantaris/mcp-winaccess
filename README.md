# mcp-winaccess

Cross-platform desktop automation via MCP adapter (`adapter/windows.py`, `adapter/linux.py`, `adapter/macos.py`).

## Install

```bash
# Windows
pip install mcp-winaccess[windows]
uv tool install mcp-winaccess[windows]

# Linux
pip install mcp-winaccess[linux]
uv tool install mcp-winaccess[linux]

# macOS
pip install mcp-winaccess
uv tool install mcp-winaccess

# Or base only (no platform extras)
pip install mcp-winaccess
uv pip install mcp-winaccess
```

## Run

```bash
uvx mcp-winaccess
```

Or directly:
```bash
python server.py
```

Or with adapter module:
```bash
python -m adapter
```

## OpenCode Config (`opencode.jsonc`)

```jsonc
{
  "mcp": {
    "winaccess": {
      "type": "local",
      "command": [
        "uvx",
        "mcp-winaccess"
      ],
      "enabled": true
    }
  }
}
```

## Tools

### Always Available
- `screenshot(save_path?)`: Full screen base64 JPEG.
- `click(x, y)`: Left-click at screen coordinates.
- `double_click(x?, y?, window?, control?)`: Double-click.
- `right_click(x?, y?, window?, control?)`: Right-click.
- `drag(x_from, y_from, x_to, y_to, duration?)`: Drag mouse.
- `drag_element(window, control, x_to, y_to)`: Drag control to target.
- `move_mouse(x, y)`: Move cursor without clicking.
- `scroll(direction?, amount?, x?, y?, window?, control?)`: Scroll.
- `type_text(text)`: Type text at keyboard focus.
- `run_app(exe_path?)`: Launch executable.
- `kill_app(name?)`: Kill process.
- `switch_to_window(title | handle)`: Restore and activate window by partial title or handle (`int`).

### Window Automation (Windows / Linux with `pywinauto` / `pyatspi`)
- `find_window(title?)`: Find top-level window.
- `list_windows()`: List visible windows.
- `click_element(window, control)`: Click UI control by index-based `ID` (`element_0`) or `AutoID`/`Name`.
- `read_text(window, control)`: Read control text by `ID`.
- `manage_window(title?, action?, x?, y?)`: Manage window state.
- `wait_for_window(title?, timeout?)`: Wait for window to appear.
- `get_all_controls(window)`: List child controls with index-based IDs (`element_0`, `element_5`), `AutoID`, `Name`, `Class`, `Type`, `Text`, `Handle`. Agents should use the `ID` value for interaction.
- `wait_for_element(window, control, timeout?)`: Wait for control by `ID`.
- `get_window_state(title?)`: Window state info.
- `get_text(window, control)`: Full text from control by `ID`.
- `set_text(window, control, value)`: Set text in control by `ID`.
- `type_in_element(window, control, text)`: Type into control by `ID`.

### System
- `read_log(path?)`: Read last 20 lines of log file. (Removed in v1.0.1)
- `build_project()`: Run Unity build automation. (Removed in v1.0.1)

Unsupported functions are hidden from MCP on each platform.
