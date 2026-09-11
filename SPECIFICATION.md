# Specification — mcp-winaccess

## Protocol
- MCP (Model Context Protocol) via `mcp` Python SDK v2 (`MCPServer`).
- Transport: stdio (local process spawned by OpenCode).

## Architecture
- Adapter pattern (`adapter/`): `base.py` interface, `windows.py` (`pywinauto` + `pyautogui`), `linux.py` (`pyatspi` + `pyautogui`), `macos.py` (`pyautogui` only).
- `server.py` registers `@mcp.tool()` conditionally: unsupported platform functions are hidden.

## Tools

### Always Available
- `screenshot(save_path?)`: Base64 JPEG of full screen.
- `click(x, y)`: Left-click at absolute coordinates.
- `double_click(x?, y?, window_title?, control_identifier?)`: Double-click.
- `right_click(x?, y?, window_title?, control_identifier?)`: Right-click.
- `drag(x_from, y_from, x_to, y_to, duration?)`: Drag mouse.
- `drag_element(window_title, control_identifier, x_to, y_to, duration?)`: Drag UI control to target coordinates.
- `move_mouse(x, y)`: Move cursor without clicking.
- `scroll(direction?, amount?, x?, y?, window_title?, control_identifier?)`: Scroll.
- `type_text(text)`: Type at current keyboard focus.

### Platform-Specific (Windows / Linux)
- `find_window(title?)`: Find visible top-level window (`pywinauto` on Windows, `pyatspi` on Linux).
- `list_windows()`: List windows.
- `click_element(window_title, control_identifier)`: Click control inside window.
- `read_text(window_title, control_identifier)`: Read text from control.
- `manage_window(title?, action?, x?, y?)`: Minimize, maximize, restore, move.
- `wait_for_window(title?, timeout?)`: Wait until window appears.
- `get_text(window_title, control_identifier)`: Full text from control.
- `set_text(window_title, control_identifier, value)`: Set text in edit control.
- `get_all_controls(window_title)`: List all child controls with index-based IDs (`element_0`, `element_1`, etc.), `AutoID`, `Name`, `Class`, `Type`, `Text`, `Handle`. Agents should use the `ID` value (e.g., `element_5`) as `control_identifier` for `click_element`, `set_text`, `read_text`, etc.
- `wait_for_element(window_title, control_identifier, timeout?)`: Wait for control.
- `get_window_state(title?)`: Window state info.
- `switch_to_window(title | handle)`: Restore and activate window by partial title (str) or handle (int).
- `type_in_element(window_title, control_identifier, text)`: Type directly into control.

### Application / System
- `run_app(exe_path?)`: Launch Windows executable (`subprocess.Popen`).
- `kill_app(name?)`: Kill by executable base name (`taskkill` /F /IM).

## Dependencies
- Python 3.10+
- `mcp>=2.0.0`
- `pyautogui>=0.9.54`
- `Pillow>=10.0.0`
- Optional: `windows` extra (`pywinauto>=0.6.8`, `pywin32>=306`)
- Optional: `linux` extra (`pyatspi>=2.46.0`)
- Optional: `mac` extra (none beyond base)

## Agent Instructions
- Every adapter method (`adapter/windows.py`, `adapter/linux.py`, `adapter/macos.py`, `adapter/base.py`) includes an `Agent instruction` docstring.
- `get_all_controls` returns index-based IDs (`element_0`, `element_5`) plus `AutoID`, `Name`, `Class`, `Type`, `Text`, `Handle`.
- Agents should use the `ID` value as `control_identifier` for `click_element`, `set_text`, `read_text`, `wait_for_element`, etc.

## Platform Behavior
- **Windows**: Full UI automation (`pywinauto`) + `pyautogui`. All functions available.
- **Linux**: Partial UI automation (`pyatspi`) + `pyautogui`. `find_window`/`click_element` available if `pyatspi` installed; `manage_window`, `get_all_controls`, `wait_for_element`, `get_window_state`, `type_in_element` return errors.
- **macOS**: Only `pyautogui` (coordinate-based, screenshot, keyboard). Window automation functions (`find_window`, `click_element`, `manage_window`, etc.) are hidden from MCP server.
