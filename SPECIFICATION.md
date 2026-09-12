# Specification — mcp-winaccess

## Protocol
- MCP (Model Context Protocol) via `mcp` Python SDK v2 (`MCPServer`).
- Transport: stdio (local process spawned by OpenCode).

## Architecture
- Adapter pattern (`adapter/`): `base.py` interface, `windows.py` (`pywinauto` + `pyautogui`), `linux.py` (`pyatspi` + `pyautogui`), `macos.py` (`pyautogui` only).
- `server.py` registers `@mcp.tool()` conditionally: unsupported platform functions are hidden from agent view.

## Tools

### Always Available
- `screenshot(save_path?)`: Base64 JPEG of full screen.
- `click(x, y)`: Left-click at absolute coordinates.
- `double_click(x=0, y=0)`: Double-click at absolute coordinates (coordinate mode only).
- `double_click_element(value, control_identifier="", x=0, y=0)`: Double-click a control inside a window. `value`: partial title (`str`) or handle (`int`). `control_identifier`: index-based `ID` (`element_0`, `element_5`) or `AutoID`/`Name` from `get_all_controls`.
- `right_click(x=0, y=0)`: Right-click at absolute coordinates.
- `drag(x_from, y_from, x_to, y_to, duration?)`: Drag mouse.
- `drag_element(value, control_identifier, x_to, y_to, duration?)`: Drag UI control to target. `value`: partial title (`str`) or handle (`int`).
- `move_mouse(x, y)`: Move cursor without clicking.
- `scroll(direction="down", amount=3, x=0, y=0)`: Scroll at absolute coordinates (no window/control params).
- `type_text(text)`: Type at current keyboard focus.
- `run_app(exe_path?)`: Launch executable (`subprocess.Popen`).
- `kill_app(name?)`: Kill by executable base name (`taskkill` /F /IM).
- `switch_to_window(value)`: Restore and activate by partial title (`str`) or handle (`int`).

### Platform-Specific (Windows / Linux with `pywinauto` / `pyatspi`)
All window automation tools accept `value` (window identifier) which can be either a partial title (`str`) or a window handle (`int`).

- `find_window(value)`: Find top-level window by partial title (`str`) or handle (`int`). Returns info string.
- `list_windows()`: List visible windows.
- `click_element(value, control_identifier)`: Click control inside window. `control_identifier`: index-based `ID` (`element_0`) or `AutoID`/`Name`.
- `read_text(value, control_identifier)`: Read text from control.
- `manage_window(value, action="maximize", x=0, y=0)`: Manage state (`minimize`/`maximize`/`restore`/`move`).
- `wait_for_window(value, timeout?)`: Wait for window to appear.
- `get_all_controls(value)`: List child controls with index-based IDs (`element_0`, `element_5`), `AutoID`, `Name`, `Class`, `Type`, `Text`, `Handle`. Agents must use the `ID` value (e.g., `element_5`) as `control_identifier`.
- `wait_for_element(value, control_identifier, timeout?)`: Wait for control by `ID`.
- `get_window_state(value)`: Window state info (`str` or `int`).
- `get_text(value, control_identifier)`: Full text from control.
- `set_text(value, control_identifier, value_text)`: Set text in edit control.
- `type_in_element(value, control_identifier, text)`: Type directly into control.

### System
- `read_log(path?)`: Read last 20 lines of log file. (Removed in v1.0.1)
- `build_project()`: Run Unity build automation. (Removed in v1.0.1)

## Agent Instructions
- Every adapter method (`adapter/windows.py`, `adapter/linux.py`, `adapter/macos.py`, `adapter/base.py`) includes `Agent instruction` docstring.
- `get_all_controls` returns index-based IDs (`element_0`, `element_5`) plus `AutoID`, `Name`, `Class`, `Type`, `Text`, `Handle`. Agents should use the `ID` value as `control_identifier` for `click_element`, `set_text`, `read_text`, `wait_for_element`, etc.
- `find_window`, `manage_window`, `wait_for_window`, `switch_to_window`, `get_window_state`, `get_all_controls` all accept `value` which can be a partial window title (`str`) or a window handle (`int`).

## Dependencies
- Python 3.10+
- `mcp>=2.0.0`
- `pyautogui>=0.9.54`
- `Pillow>=10.0.0`
- Optional: `windows` extra (`pywinauto>=0.6.8`, `pywin32>=306`)
- Optional: `linux` extra (`pyatspi>=2.46.0`)
- Optional: `mac` extra (none beyond base)

## Platform Behavior
- **Windows**: Full UI automation (`pywinauto`) + `pyautogui`. All functions available.
- **Linux**: Partial UI automation (`pyatspi`) + `pyautogui`. `find_window`/`click_element` available if `pyatspi` installed; `manage_window`, `get_all_controls`, `wait_for_element`, `get_window_state`, `type_in_element`, `drag_element`, `double_click_element` return errors when `pyatspi` unavailable or not fully implemented.
- **macOS**: Only `pyautogui` (coordinate-based, screenshot, keyboard, drag). Window automation functions are hidden from MCP server. `double_click_element` supports coordinate mode only (`value` and `control_identifier` must be empty for basic mode).
